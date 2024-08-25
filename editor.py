"""
http.server for creating, editing and deleting articles (to be used for development purposes only).
"""

# Import from src without specify parent directory in module,
# which will be important for AWS that starts in the src directory.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import datetime
import jwt
import random
import string
import json
import hashlib
from http.cookies import SimpleCookie

from src import Article
from src import JsonUtils

# Editor does not support AWS and can only use http.server module
from src.http_server import Server, RequestHandler
from src.http_server import FileUtils as file

from dotenv import load_dotenv
load_dotenv()

def GenerateKey(count : int) -> str:
    choices = string.ascii_uppercase + string.ascii_lowercase + string.digits

    key = ''
    for i in range(count):
        key += random.choice(choices)
    return key

secret_key = ''#GenerateKey(32)

class Editor(RequestHandler):
    def GetQueryOrDefault(self, queries : dict[str, list[str]], query_name : str, default_value : str) -> str:
        query = self._get_query(queries, query_name)
        if not query:
            return default_value
        return query
    
    def GetCookieOrDefault(self, cookies : SimpleCookie, cookie_name : str, default_value : str) -> str:
        query = self._get_cookie(cookies, cookie_name)
        if not query:
            return default_value
        return query

    def do_POST(self):
        path = self._get_path()
        
        status_code = 500
        content_type = 'application/json'
        content = json.dumps({ 'error': 'Unexpected server error' })

        try:

            if path == "login":
                queries = self._get_queries_post()
                username = self.GetQueryOrDefault(queries, 'username', '')
                password = self.GetQueryOrDefault(queries, 'password', '')
                successfulLogin = self.Login(username, password)
                
                content_type = 'application/json'
                if successfulLogin:
                    token = self.GenerateJWT(username, password)
                    expiration = datetime.datetime.now() + datetime.timedelta(hours=2)
                    
                    status_code = 200
                    content = json.dumps({ "token": token, "expiration": expiration.timestamp() })
                else:
                    status_code = 404
                    content = json.dumps({ 'error': 'Unable to login' })

            elif "upload/image/" in path:
                filename_start = path.find("upload/image/") + len("upload/image/")
                filename = path[filename_start:]
                
                imgData = self._get_body_bytes()
                imagePath = f"Assets/images/{filename}"
                
                with open(imagePath, 'wb') as f:
                    f.write(imgData)
                
                status_code = 200
                content_type = 'application/json'
                content = json.dumps({ 'image': imagePath })

            else:
                status_code = 400
                content = json.dumps({ 'error': 'Invalid endpoint or method specified' })

        except Exception as e:
            print(f"[/{path}] Encountered error: {e}")

        self._send_headers(status_code, content_type)
        self._send_content(content)

    def do_PUT(self):
        path = self._get_path()
        #queries = self._get_queries_post()
        body = self._get_json_body()
        cookies = self._get_cookies()

        status_code = 500
        content_type = 'application/json'
        content = json.dumps({ 'error': 'Unexpected server error' })
        
        try:
            token = self.GetCookieOrDefault(cookies, 'token', '')
            successfulLogin = self.VerifyJWT(token)

            if not successfulLogin:
                status_code = 400
                content = json.dumps({ 'error': 'Invalid token specified, unable to login' })
                content_type = 'application/json'

            elif "api/edit/" in path:
                article_path_start = path.find("api/edit/") + len("api/edit/")
                article_path = f'Articles/{path[article_path_start:]}.json'
                status_code, content, content_type = self.EditArticle(article_path, body)

            elif "api/create/" in path and successfulLogin:
                article_path_start = path.find("api/create/") + len("api/create/")
                article_path = f'Articles/{path[article_path_start:]}.json'
                status_code, content, content_type = self.CreateArticle(article_path, body)

            else:
                status_code = 400
                content = json.dumps({ 'error': 'Invalid endpoint or method specified' })

        except Exception as e:
            print(f"[/{path}] Encountered error: {e}")

        self._send_headers(status_code, content_type)
        self._send_content(content)

    def do_DELETE(self):
        path = self._get_path()
        cookies = self._get_cookies()

        status_code = 500
        content_type = 'application/json'
        content = json.dumps({ 'error': 'Unexpected server error' })

        token = self.GetCookieOrDefault(cookies, 'token', '')
        successfulLogin = self.VerifyJWT(token)

        try:

            if "api/delete/" in path and successfulLogin:
                article_path_start = path.find("api/delete/") + len("api/delete/")
                article_path = f'Articles/{path[article_path_start:]}.json'

                if file.Exists(article_path):
                    file.Remove(article_path)
                    status_code = 200 
                    content = '{}'
                else:
                    status_code = 400
                    content = json.dumps({ 'error': 'Requested article does not exist or has already been deleted'})

            else:
                status_code = 400
                content = json.dumps({ 'error': 'Invalid endpoint or method specified' })

        except Exception as e:
            print(f"[/{path}] Encountered error: {e}")

        self._send_headers(status_code, content_type)
        self._send_content(content)
    
    def do_GET(self):
        path = self._get_path()
        cookies = self._get_cookies()
        
        token = self.GetCookieOrDefault(cookies, 'token', '')
        successfulLogin = self.VerifyJWT(token)

        content_type = 'text/html'
        content = self.DefaultContent

        article_path = f'Articles/{path}.json'
        
        # Login
        if not file.Exists(path) and not successfulLogin:
            content, content_type = self.GetLoginPage()
        
        # Home
        elif path == "":
            content, content_type = self.GetHomePage(token)

        # Article Page
        elif file.Exists(article_path):
            edit_mode : bool = self._get_query(self._get_queries(), 'mode') == "edit"
            content, content_type = self.GetArticlePage(article_path, path, edit_mode)
            
        # Get Resource
        else:
            self._send_resource(path)
            return
            
        self._send_headers(200, content_type)
        self._send_content(content)

    def Redirect(self, url : str) -> tuple[str, str]:
        return f'<html><meta http-equiv="refresh" content="0; url={url}"/></html>', 'text/html'
    
    def GetHomePage(self, token : str) -> tuple[str, str]:
        with open('Assets/pages/editor/home.html', 'r') as f:
            html = f.read()
        
        article_list = "<div class='article_list'>"

        article_directories = file.ListDirectory('Articles')
        articles = [(article, Article.GetArticleFromFile(f"Articles/{article}")) for article in article_directories]
        articles.sort(key=lambda article : -article[1].PublishDate.timestamp())
        
        for i, (article, articleInfo) in enumerate(articles):
            article_path = article.removesuffix('.json')
            article_list += f"""\n<div class='article' id='article-{i}'>
                <a class="link" href='/{article_path}'>
                    <div class='article-image'>
                        <img src='{articleInfo.ImagePath}'/>
                    </div>
                    <div class='article-text'>
                        <h3>{articleInfo.Title}</h3>
                        <p>{articleInfo.Description[0:150]}...</p>
                    </div>
                </a>
                <div class='article-icon'>
                    <a href='/{article_path}?mode=edit'>
                        <img class='article-edit' src='Assets/icons/edit-icon.png'/>
                    </a>
                    <img class='article-toggle-private' onclick='TogglePublic("{article_path}", this)' src='Assets/icons/{'public' if articleInfo.Public else 'private'}-icon.png'/>
                    <img class='article-delete' onclick='OpenDeletePopup("{article_path}")' src='Assets/icons/delete-icon.png'/>
                </div>
            </div>
            """

        article_list += "</div>"
        content = html.replace('{Articles}', article_list)
        return content, 'text/html'
    
    def GetArticlePage(self, article_path : str, path : str, edit_mode : bool) -> tuple[str, str]:
        templatePath = 'Assets/pages/editor/article.html' if edit_mode else 'Assets/pages/templates/article.html'
        article = Article.GetArticleFromFile(article_path)
        article.Serialize(article_path) # Any generated ID's will be saved

        content = article.ConvertToHTML(templatePath, edit_mode)
        return content, 'text/html'
    
    def GetLoginPage(self):
        with open('Assets/pages/editor/login.html', 'r') as f:
            content = f.read()

        return content, 'text/html'
    
    def QueriesToArticle(self, article : Article.Article, queries : dict[str, str]):
        article.Name = JsonUtils.GetString(queries, 'Name', article.Name)
        article.Title = JsonUtils.GetString(queries, 'Title', article.Title)
        article.Description = JsonUtils.GetString(queries, 'Description', article.Description)
        article.ImagePath = JsonUtils.GetString(queries, 'Image', article.ImagePath)
        article.Public = JsonUtils.GetBool(queries, 'Public', article.Public)
        article.Elements = []

        for name, value in queries.items():
            if name in ['Name', 'Title', 'Description', 'Image', 'Public']: # Not an element
                continue

            split_values = value.split(':')
            type = split_values[0]
            value = split_values[1]

            element = { 'ID': name, 'Type': type, 'Value': value }
            article.Elements.append(Article.ArticleElement(element))
    
    def CreateArticle(self, article_path : str, queries : dict[str, str]) -> tuple[int, str, str]:
        if file.Exists(article_path):
            return 400, json.dumps({ 'error' : 'Requested article name already exists' }), 'application/json'

        article = Article.Article({ 'Name': 'New Article', 'Title': 'New Article'})
        self.QueriesToArticle(article, queries)
        article.Serialize(article_path)

        return 200, json.dumps({ "article": article.GetDict() }), 'application/json'
    
    def EditArticle(self, article_path : str, queries : dict[str, str]) -> tuple[int, str, str]:
        if not file.Exists(article_path):
            return 400, json.dumps({ 'error' : 'Requested article does not exist' }), 'application/json'
        
        article = Article.GetArticleFromFile(article_path)
        self.QueriesToArticle(article, queries)
        article.Serialize(article_path)
        
        return 200, json.dumps({ "article": article.GetDict() }), 'application/json'
    
    def Login(self, username : str | None, password : str | None) -> bool:
        if not username or not password:
            return False
        
        editor_username = os.getenv('EDITOR_USERNAME') or ''
        editor_password = os.getenv('EDITOR_PASSWORD') or ''
        editor_password = hashlib.sha256(editor_password.encode('utf-8')).hexdigest()
        return username == editor_username and password == editor_password
    
    def GenerateJWT(self, username : str, password : str) -> str:
        payload = {
            'username': username,
            'password': password
        }

        return jwt.encode(payload, secret_key)
    
    def VerifyJWT(self, token : str | None) -> bool:
        if not token:
            return False

        try:
            header_data = jwt.get_unverified_header(token)
            payload = jwt.decode(token, secret_key, algorithms=[header_data['alg'],])
            return self.Login(payload['username'], payload['password'])
        except Exception as e:
            print(f"[/{self._get_path()}] Could not verify token {token} due to error: {e}")
            return False

# Running from terminal (Create Web Server)
if __name__ == "__main__":
    # Web Server Details
    hostName = "localhost"
    serverPort = 3000
    redirect_uri = f'http://{hostName}:{serverPort}'
    
    # Run Web Server
    print(f'Please open your browser to {redirect_uri}')
    server = Server(hostName, serverPort, Editor)
    server.RunAlways()
