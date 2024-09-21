function ResizeTextAreas() {
    textList = document.getElementsByTagName('TEXTAREA');
    for (let element of textList) {
        element.style.height = ""; 
        element.style.height = element.scrollHeight + "px";
        element.oninput = ResizeTextArea;
    }
}

function swapStyleSheet() {
    element = document.getElementById("pagestyle")
    sheet = element.getAttribute("href") == "Assets/styles/dark.css" ? "Assets/styles/light.css" : "Assets/styles/dark.css";
    element.setAttribute("href", sheet);  
}