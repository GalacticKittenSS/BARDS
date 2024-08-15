from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from http.cookies import SimpleCookie

import os
import json

class RequestHandler(BaseHTTPRequestHandler):
    DefaultContent = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog</title>
</head>
<body>
    <h2>Page Not Found<h2>
</body>
</html>
"""

    def _get_query(self, queries : dict[str, list[str]], name : str) -> str | None:
        query : list[str] | None = queries.get(name)
        if query:
            return query[0]
        return None

    def _get_path(self) -> str:
        path = urlparse(self.path)
        # First character is always '/'
        return path.path[1:]
    
    def _get_queries(self) -> dict[str, list[str]]:
        path = urlparse(self.path)
        return parse_qs(path.query)
    
    def _get_body_bytes(self) -> bytes:
        headers = self.headers.get('Content-Length')
        if headers is None:
            return bytes(0)
        
        content_len = int(headers)
        post_body = self.rfile.read(content_len)
        return post_body
    
    def _get_body(self) -> str:
        post_body = self._get_body_bytes()
        return post_body.decode('utf-8')
    
    def _get_queries_post(self) -> dict[str, list[str]]:
        post_body = self._get_body()
        return parse_qs(post_body)
    
    def _get_json_body(self) -> dict:
        if self.headers.get('Content-Type') != 'application/json':
            return {}
        
        post_body = self._get_body()
        return json.loads(post_body)
    
    def _get_cookies(self) -> SimpleCookie:
        return SimpleCookie(self.headers.get('Cookie'))
    
    def _get_cookie(self, cookies : SimpleCookie, name : str) -> str | None:
        cookie = cookies.get(name)
        if not cookie:
            return None
        
        return cookie.value
    
    def _get_content_type_from_path(self, path : str):
        extension = path.split('.')[-1]
        
        # TODO: Add more
        match extension:
            case "html":
                return "text/html"
            case "css": 
                return "text/css"
            case "js":
                return "text/javascript"
            case "png":
                return "image/png"
            case "jpg":
                return "image/jpeg"
            case "gif":
                return "image/gif"
                

    def _send_headers(self, status : int, content_type : str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def _send_content(self, content : str) -> int:
        return self.wfile.write(content.encode('utf-8'))

    def _send_content_bytes(self, content : bytes) -> int:
        return self.wfile.write(content)
    
    def _send_resource(self, resource_path : str):
        if not os.path.exists(resource_path):
            print(f"[/{resource_path}] File {resource_path} does not exist")
            self._send_headers(404, 'text/html')
            self._send_content(self.DefaultContent)
            return
        
        with open(resource_path, 'rb') as f:
            content = f.read()

        content_type = self._get_content_type_from_path(resource_path)
        if not content_type:
            self._send_headers(404, '')
            return

        self._send_headers(200, content_type)
        self._send_content_bytes(content)
            

class Server:
    def __init__(self, hostName : str, serverPort : int, requestHandlerClass : type[RequestHandler]):
        self.HTTPServer = HTTPServer((hostName, serverPort), requestHandlerClass)
        self.Running = False
        
    def StopServer(self):
        self.Running = False

    def RunAlways(self):
        self.Running = True

        while self.Running:
            self.HTTPServer.handle_request()
        
        self.HTTPServer.server_close()