function ResizeTextArea() {
    this.style.height = ""; 
    this.style.height = this.scrollHeight + "px";
}

function DeleteElement() {
    this.parentNode.remove()
}

function AddImageEventListener(element) {
    let input = element.children[0];
    let label = element.children[1];
    let image = label.children[0];
    input.addEventListener('change', (event) => {
        const files = event.target.files;
        image.src = URL.createObjectURL(files[0]);
    });
}

function AddBasicElement() {
    element = document.createElement('div');
    element.className = "element-parent";
    
    img = document.createElement('img');
    img.className = "delete-element";
    img.onclick = DeleteElement;
    img.src = 'Assets/icons/delete-icon.png';
    element.appendChild(img);
    
    parentElement = document.getElementsByClassName('main')[0];
    childElement = document.getElementsByClassName('add-element')[0];
    parentElement.insertBefore(element, childElement);
    
    return element;
}

function AddTextElement() {
    div = document.createElement('div');
    div.className = "Text";

    textarea = document.createElement('textarea')
    textarea.id = GenerateRandomString(16);
    textarea.oninput = ResizeTextArea;
    textarea.className = "element";
    textarea.name = textarea.id;
    div.appendChild(textarea);

    element = AddBasicElement()
    element.appendChild(div);
}

function AddImageElement() {
    div = document.createElement('div');
    div.className = "element Image"

    input = document.createElement('input')
    input.id = GenerateRandomString(16);
    input.name = input.id;
    input.type = "file";
    input.accept = "image/*";
    div.appendChild(input);
    
    label = document.createElement('label');
    label.htmlFor = input.id;
    label.class = "button";
    label.innerHTML = "Upload File"
    div.appendChild(label);

    img = document.createElement('img');
    label.appendChild(img);
    
    element = AddBasicElement()
    element.appendChild(div);

    AddImageEventListener(div);
}

function AddCodeElement() {
    div = document.createElement('div');
    div.className = "Code";

    textarea = document.createElement('textarea')
    textarea.id = GenerateRandomString(16);
    textarea.oninput = ResizeTextArea;
    textarea.className = "element";
    textarea.name = textarea.id;
    div.appendChild(textarea);

    element = AddBasicElement()
    element.appendChild(div);
}

async function UploadFile(element, image) {
    const file = element.files[0];
    
    if (file) {
        const response = await FetchJson('upload/image/' + file.name, "POST", "image/png", file);
        return response['image'];                        
    }
    
    const url = window.location.protocol + "//" + window.location.host + "/";
    return image.src.replace(url, '');
}

async function SaveArticle(form) {
    const formData = new FormData(form);
    
    let banner = document.getElementsByName('Image')[0];
    const bannerValue = await UploadFile(banner, document.getElementById('BannerImage'));
    formData.set('Image', bannerValue);
    
    for (let [key, value] of formData.entries()) {
        const properties = ['Name', 'Title', 'Description', 'Image'];
        if (properties.includes(key))
            continue;

        let element = document.getElementById(key);
        let type = element.parentElement.className.replace('element ', '');
        
        if (type == "Image")
            value = await UploadFile(element, element.parentNode.children[1].children[0]);

        formData.set(key, type + ":" + value);
    }

    EditArticle(window.location.pathname, Object.fromEntries(formData));
}

function Submit(e) {
    e.preventDefault();
    SaveArticle(e.target);
}

function OnKeyDown(e) {
    if(!e.ctrlKey || e.keyCode != 'S'.charCodeAt(0))
        return;
    
    e.preventDefault();
    const form = document.getElementById('edit-form');
    SaveArticle(form);
}

function OnImageChange(event) {
    const bannerImage = document.getElementById('BannerImage');
    const files = event.target.files;
    bannerImage.src = URL.createObjectURL(files[0]);
}