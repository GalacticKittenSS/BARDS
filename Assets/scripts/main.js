function ResizeTextAreas() {
    textList = document.getElementsByTagName('TEXTAREA');
    for (let element of textList) {
        element.style.height = ""; 
        element.style.height = element.scrollHeight + "px";
        element.oninput = ResizeTextArea;
    }
}