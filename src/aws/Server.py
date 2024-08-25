from urllib.parse import urlparse, parse_qs

import json
import base64
from . import FileUtils as file


class RequestHandler:
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

    def __init__(self, path : str, headers : dict, body : str):
        self.path = path
        self.headers = headers
        self.body = body

        self.response : dict = { "isBase64Encoded": False }

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
    
    def _get_body(self) -> str:
        return self.body
    
    def _get_queries_post(self) -> dict[str, list[str]]:
        post_body = self._get_body()
        return parse_qs(post_body)
    
    def _get_json_body(self) -> dict:
        if self.headers.get('Content-Type') != 'application/json':
            return {}
        
        post_body = self._get_body()
        return json.loads(post_body)
    
    def _get_cookies(self) -> dict | None:
        return self.headers.get('Cookie')
    
    def _get_cookie(self, cookies : dict, name : str) -> str | None:
        cookie = cookies.get(name)
        if not cookie:
            return None
        
        return cookie
    
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
        self.response['statusCode'] = status

        self.response['headers'] = {}
        self.response['headers']['content-type'] = content_type

    def _send_content_bytes(self, content : bytes):
        content_b64 = base64.b64encode(content)
        self.response['body'] = content_b64
        self.response['isBase64Encoded'] = True

    def _send_content(self, content : str):
        self._send_content_bytes(content.encode('utf-8'))
    
    def _send_resource(self, resource_path : str):
        if not file.Exists(resource_path):
            print(f"[/{resource_path}] File {resource_path} does not exist")
            self._send_headers(404, 'text/html')
            self._send_content(self.DefaultContent)
            return
        
        content = file.ReadBytes(resource_path)
        content_type = self._get_content_type_from_path(resource_path)
        
        if not content_type:
            self._send_headers(404, '')
            return

        print(f"Sending resource: {resource_path}")
        self._send_headers(200, content_type)
        self._send_content_bytes(content)

class Server:
    def __init__(self, hostName : str, serverPort : int, requestHandlerClass : type[RequestHandler]):
        self.RequestHandlerClass = requestHandlerClass

    def StopServer(self):
        pass

    def RunOnce(self, event : dict, context : object):
        path : str = event.get('rawPath') or '/'
        headers : dict = event.get('headers') or {}
        body : str = event.get('body') or ''
        handler = self.RequestHandlerClass(path, headers, body)
        
        print(f"Received request with path {path}")

        http_method = event.get('httpMethod') or 'GET'
        method_name = 'do_' + http_method
        if hasattr(handler, method_name):
            method = getattr(handler, method_name)
            method()

        return handler.response

    def RunAlways(self, event : dict = {}, context : object = None):
        # AWS Lambda relaunches the script for every request 
        # and, therefore, can only run once.
        return self.RunOnce(event, context)