import datetime
import string
import random

import JsonUtils as json
from Platform import FileUtils

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
    
    def ConvertToHTML(self, edit_mode : bool = False):
        html : str = ""
        
        if edit_mode:
            elementHtml = ""

            match self.Type:
                case "Text":
                    elementHtml = f"""
                    <div class='{self.Type}'>
                        <textarea id={self.ID} class='element {self.Type}' name='{self.ID}'>{self.Value}</textarea>
                    </div>"""
                case "Image":
                    elementHtml = f"""
                    <div class="element {self.Type}">
                        <input id={self.ID} type="file" name="{self.ID}"/>
                        <label for="{self.ID}" class="button">
                            Upload File
                            <img src="{self.Value}"/>
                        </label>
                    </div>"""
                case "Code":
                    elementHtml = f"""
                    <div class='{self.Type}'>
                        <textarea id={self.ID} class='element {self.Type}' name='{self.ID}'>{self.Value}</textarea>
                    </div>"""

                    

            html += f"""\n
            <div class="element-parent">
                {elementHtml}
                <img class="delete-element" onclick='this.parentNode.remove()' src='https://static-00.iconduck.com/assets.00/delete-icon-467x512-g85gm4kg.png'/>
            </div>
            """
        else:
            html += f"<div id='{self.ID}' class='element {self.Type}'>"
            
            match self.Type:
                case "Text":
                    paragraphs = self.Value.split('\n')
                    for p in paragraphs:
                        html += f"\n   <p>{p}</p>"
                case "Image":
                    html += f"<img src='{self.Value}'/>"
                case "Code":
                    html += f"<textarea id={self.ID} class='{self.Type}' name='{self.ID}' readonly>{self.Value}</textarea>"
            
            html += "\n</div>"
        
        return html
    
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
        self.Public = json.GetBool(articleInfo, "Public", False)
        self.CreateDate = json.GetDate(articleInfo, "Created", "%Y-%m-%d %H:%M:%S", datetime.datetime.now())
        self.PublishDate = json.GetDate(articleInfo, "Published", "%Y-%m-%d %H:%M:%S", self.CreateDate)
        self.Elements : list[ArticleElement] = []

        elements : list[dict] = json.GetList(articleInfo, "Elements")
        for element in elements:
            self.Elements.append(ArticleElement(element))
        

    def __str__(self):
        return f"Article({self.Name=}, {self.Title=}, {self.Description=})"

    def ConvertToHTML(self, templatePath : str, edit_mode : bool = False):
        html : str = FileUtils.Read(templatePath)
        html = html.replace('{PageName}', self.Name)
        html = html.replace('{Title}', self.Title)
        html = html.replace('{Image}', self.ImagePath)
        html = html.replace('{Description}', self.Description)
        
        elements = ""
        for element in self.Elements:
            elements += element.ConvertToHTML(edit_mode)
        html = html.replace('{Elements}', elements)
        
        return html
    
    def GetDict(self):
        dictionary = {
            "PageName": self.Name,
            "Title": self.Title,
            "Description": self.Description,
            "BannerImage": self.ImagePath,
            "Public": self.Public,
            "Elements": [element.GetDict() for element in self.Elements],
            "Created": self.CreateDate.strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.Public:
            dictionary["Published"] = self.PublishDate.strftime("%Y-%m-%d %H:%M:%S")

        return dictionary


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