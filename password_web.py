import sys
import os
import json
import secrets
import io
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from typing import Optional
from string import digits, ascii_letters, punctuation, ascii_uppercase

app = FastAPI()

# Set up templates directory (in-memory template below, but FastAPI expects a directory)
templates = Jinja2Templates(directory="templates")

# Load dictionary once
with open("./data/dictionary.json") as fileHandle:
    WEBSTERS_DICTIONARY = json.load(fileHandle)

def additional_separator_characters(insertNumbers=False, insertSpecial=False, insertChars=False, insertUpper=False):
    separatorCharacters = ""
    if insertChars: separatorCharacters += ascii_letters
    if insertUpper: separatorCharacters += ascii_uppercase
    if insertNumbers: separatorCharacters += digits
    if insertSpecial: separatorCharacters += punctuation
    return separatorCharacters

def generate_password(count=2, insertNumbers=False, insertSpecial=False, insertChars=False, insertUpper=False):
    websters = list(WEBSTERS_DICTIONARY.keys())
    myPassword = ""
    separators = additional_separator_characters(insertNumbers, insertSpecial, insertChars, insertUpper)
    for iteration in range(count):
        myPassword += secrets.choice(websters)
        if (count > 1) and (iteration < count-1):
            if separators:
                myPassword += secrets.choice(separators)
    return myPassword

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Password Phrase Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 500px; margin: auto; }
        .result { font-size: 1.2em; color: #2c3e50; margin-top: 20px; }
        textarea { width: 100%; height: 120px; font-size: 1em; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Password Phrase Generator</h2>
        <form method="post">
            <label>Number of Words:
                <input type="number" name="count" value="{{ count }}" min="2" max="10" required>
            </label><br><br>
            <label>Number of Passwords:
                <input type="number" name="repeat" value="{{ repeat }}" min="1" max="20" required>
            </label><br><br>
            <label><input type="checkbox" name="insertNumbers" {% if insertNumbers %}checked{% endif %}> Include Numbers</label><br>
            <label><input type="checkbox" name="insertSpecial" {% if insertSpecial %}checked{% endif %}> Include Special Characters</label><br>
            <label><input type="checkbox" name="insertChars" {% if insertChars %}checked{% endif %}> Include Letters</label><br>
            <label><input type="checkbox" name="insertUpper" {% if insertUpper %}checked{% endif %}> Include Uppercase Letters</label><br><br>
            <button type="submit">Generate</button>
        </form>
        {% if passwords %}
        <div class="result">
            <strong>Generated Password Phrases:</strong><br>
            <textarea readonly>{{ passwords }}</textarea>
            <form method="post" action="/save">
                <input type="hidden" name="passwords" value="{{ passwords|replace('\n', '&#10;') }}">
                <button type="submit">Save to File</button>
            </form>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''


@app.get("/", response_class=HTMLResponse)
async def index_get(request: Request):
    # Render the HTML form with default values
    from jinja2 import Template
    template = Template(HTML)
    html = template.render(
        passwords=None,
        count=4,
        repeat=1,
        insertNumbers=False,
        insertSpecial=False,
        insertChars=False,
        insertUpper=False
    )
    return HTMLResponse(content=html)

@app.post("/", response_class=HTMLResponse)
async def index_post(
    request: Request,
    count: int = Form(4),
    repeat: int = Form(1),
    insertNumbers: Optional[str] = Form(None),
    insertSpecial: Optional[str] = Form(None),
    insertChars: Optional[str] = Form(None),
    insertUpper: Optional[str] = Form(None)
):
    # Checkbox values are present as string if checked, else None
    insertNumbers = insertNumbers is not None
    insertSpecial = insertSpecial is not None
    insertChars = insertChars is not None
    insertUpper = insertUpper is not None

    passwords_list = [
        generate_password(count, insertNumbers, insertSpecial, insertChars, insertUpper)
        for _ in range(repeat)
    ]
    passwords = "\n".join(passwords_list)

    from jinja2 import Template
    template = Template(HTML)
    html = template.render(
        passwords=passwords,
        count=count,
        repeat=repeat,
        insertNumbers=insertNumbers,
        insertSpecial=insertSpecial,
        insertChars=insertChars,
        insertUpper=insertUpper
    )
    return HTMLResponse(content=html)

@app.post("/save")
async def save(passwords: str = Form(...)):
    # Replace HTML line breaks with actual newlines
    passwords = passwords.replace('&#10;', '\n')
    file_stream = io.BytesIO(passwords.encode('utf-8'))
    headers = {
        'Content-Disposition': 'attachment; filename="passwords.txt"'
    }
    return StreamingResponse(file_stream, media_type="text/plain", headers=headers)

@app.post("/api/generate")
async def api_generate(request: Request):
    data = await request.json()
    count = int(data.get('count', 4))
    repeat = int(data.get('repeat', 1))
    insertNumbers = bool(data.get('insertNumbers', False))
    insertSpecial = bool(data.get('insertSpecial', False))
    insertChars = bool(data.get('insertChars', False))
    insertUpper = bool(data.get('insertUpper', False))
    passwords = [
        generate_password(count, insertNumbers, insertSpecial, insertChars, insertUpper)
        for _ in range(repeat)
    ]
    return JSONResponse(content={'passwords': passwords})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("password_web:app", host="127.0.0.1", port=8000, reload=True)