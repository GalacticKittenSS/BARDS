function GenerateRandomString(count) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let string = "";
    for (let i = 0; i < count; i++) {
        string += characters.charAt(Math.floor(Math.random() * characters.length));
    }

    return string;
}

async function FetchJson(url, method, content_type, body) {
    const payload = {
        method: method,
        headers: {
            "Content-Type": content_type,
        },
        body: body,
        isBase64Encoded: false,
        
    };
    
    // TODO: Error Handling
    const response =  await fetch(url, payload);
    return await response.json()
}

async function Login(username, password) {
    body = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password);
    return await FetchJson("login", "POST", "text/plain", body);
}

async function CreateArticle(article_name, data) {
    return await FetchJson("/api/create/" + article_name, "PUT", "application/json", JSON.stringify(data));
}

async function EditArticle(article_name, data) {
    return await FetchJson("/api/edit/" + article_name, "PUT", "application/json", JSON.stringify(data));
}

async function DeleteArticle(article_name) {
    return await FetchJson("/api/delete/" + article_name, "DELETE", "application/json", '{}');
}