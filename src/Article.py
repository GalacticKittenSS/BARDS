import string
import random
import JsonUtils as json

class ArticleElement:
    def __init__(self, elementInfo : dict):
        self.ID = self._get_or_create_id(elementInfo)
        self.Type = json.GetString(elementInfo, "Type")
        self.Value = json.GetString(elementInfo, "Value")

    def __str__(self):
        return f"ArticleElement({self.Type=}, {self.Value=})"

    def _get_or_create_id(self, file : dict) -> str:
        id = file.get("ID")
        if id:
            return id
        
        choices = string.ascii_uppercase + string.ascii_lowercase + string.digits

        new_id : str = ''
        for i in range(16):
            new_id += random.choice(choices)

        return new_id
    
    def ConvertToHTML(self):
        elementHTML : str = ""
        
        match self.Type:
            case "Text":
                paragraphs = self.Value.split('\n')
                for p in paragraphs:
                    elementHTML += f"\n   <p>{p}</p>"
            case "Image":
                elementHTML = f"<img src='{self.Value}'/>"
            
        return f"""<div id='{self.ID}' class='element {self.Type}'>
            {elementHTML}
        </div>"""
    
    def GetDict(self):
        return {
            'ID': self.ID,
            'Type': self.Type,
            'Value': self.Value
        }


class Article:
    def __init__(self, articleInfo : dict):
        self.Name = json.GetString(articleInfo, "PageName")
        self.Title = json.GetString(articleInfo, "Title")
        self.ImagePath = json.GetString(articleInfo, "BannerImage")
        self.Description = json.GetString(articleInfo, "Description")
        self.Elements : list[ArticleElement] = []

        elements : list[dict] = json.GetList(articleInfo, "Elements")
        for element in elements:
            self.Elements.append(ArticleElement(element))
        

    def __str__(self):
        return f"Article({self.Name=}, {self.Title=}, {self.Description=})"

    def ConvertToHTML(self, templatePath : str):
        with open(templatePath, 'r') as f:
            html : str = f.read()

        html = html.replace('{PageName}', self.Name)
        html = html.replace('{Title}', self.Title)
        html = html.replace('{Image}', self.ImagePath)
        html = html.replace('{Description}', self.Description)
        
        elements = ""
        for element in self.Elements:
            elements += element.ConvertToHTML()
        html = html.replace('{Elements}', elements)
        
        return html
    
    def GetDict(self):
        return {
            "PageName": self.Name,
            "Title": self.Title,
            "Description": self.Description,
            "BannerImage": self.ImagePath,
            "Elements": [element.GetDict() for element in self.Elements]
        }

    def Serialize(self, file_path : str):
        article = self.GetDict()
        json.SaveToPath(article, file_path)
    

def GetArticleFromFile(path : str) -> Article:
    file = json.LoadFromPath(path)
    return Article(file)

# Test
if __name__ == "__main__":
    file = json.LoadFromPath("Articles/example.json")
    article = Article(file)
    html = article.ConvertToHTML('Assets/pages/templates/article.html')

    with open('example.html', 'w+') as f:
        f.write(html)