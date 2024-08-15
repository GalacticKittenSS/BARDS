import os

from src.Server import Server, RequestHandler
import src.Article as Article

# Web Server Details
hostName = "localhost"
serverPort = 3000
redirect_uri = f'http://{hostName}:{serverPort}'

class Handler(RequestHandler):
    def do_GET(self):
        path = self._get_path()
        
        content_type = 'text/html'
        content = self.DefaultContent

        # Article Page
        article_path = f'Articles/{path}.json'
        if os.path.exists(article_path):
            content, content_type = self.GetArticlePage(article_path)
        
        # Home
        elif path == "":
            content, content_type = self.GetHomePage()

        # Resources
        else:
            self._send_resource(path)
            return

        self._send_headers(200, content_type)
        self._send_content(content)

    def Redirect(self, url : str) -> str:
        return f'<html><meta http-equiv="refresh" content="0; url={url}"/></html>'
    
    def GetHomePage(self) -> tuple[str, str]:
        with open('Assets/pages/templates/home.html', 'r') as f:
            html = f.read()
        
        article_list = "<div class='article_list'>"

        articles = os.listdir('Articles')
        for i, article in enumerate(articles):
            articleInfo = Article.GetArticleFromFile(f"Articles/{article}")
            article_list += f"""\n<div class='article' id='article-{i}'>
                <a class="link" href='/{article.removesuffix('.json')}'>
                    <img src='{articleInfo.ImagePath}'/>
                    <div class='article-text'>
                        <h3>{articleInfo.Title}</h3>
                        <p>{articleInfo.Description[0:150]}...</p>
                    </div>
                </a>
            </div>
            """

        article_list += "</div>"
        content = html.replace('{Articles}', article_list)
        return content, 'text/html'

    def GetArticlePage(self, article_path : str) -> tuple[str, str]:
        article = Article.GetArticleFromFile(article_path)
        content = article.ConvertToHTML('Assets/pages/templates/article.html')
        return content, 'text/html'
        

# Run Web Server
print(f'Please open your browser to {redirect_uri}')
server = Server(hostName, serverPort, Handler)
server.RunAlways()