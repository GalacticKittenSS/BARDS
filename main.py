# Import from src without specify parent directory in module,
# which will be important for AWS that starts in the src directory.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.Platform import Server, RequestHandler
import src.Article as Article

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

        article_directories = os.listdir('Articles')
        articles = [(article, Article.GetArticleFromFile(f"Articles/{article}")) for article in article_directories]
        articles.sort(key=lambda article : -article[1].PublishDate.timestamp())
        
        i = 0
        for article, articleInfo in articles:
            if not articleInfo.Public:
                continue

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

            i += 1

        article_list += "</div>"
        content = html.replace('{Articles}', article_list)
        return content, 'text/html'

    def GetArticlePage(self, article_path : str) -> tuple[str, str]:
        article = Article.GetArticleFromFile(article_path)
        if not article.Public:
            return self.DefaultContent, 'text/html'

        content = article.ConvertToHTML('Assets/pages/templates/article.html')
        return content, 'text/html'
        
if __name__ == "__main__":
    # Web Server Details
    hostName = "localhost"
    serverPort = 3000
    redirect_uri = f'http://{hostName}:{serverPort}'

    # Run Web Server
    print(f'Please open your browser to {redirect_uri}')
    server = Server(hostName, serverPort, Handler)
    server.RunAlways()