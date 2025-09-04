from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to sys.path so we can import passWordPhrase
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from passWordPhrase import LoadDictionaryFile

app = Flask(__name__)

# Initialize dictionary loader
generator = LoadDictionaryFile()
generator.LoadFile()

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json(force=False)
    count = int(data.get('count', 4))
    insertNumbers = bool(data.get('insertNumbers', False))
    insertSpecial = bool(data.get('insertSpecial', False))
    insertChars = bool(data.get('insertChars', False))
    insertUpper = bool(data.get('insertUpper', False))
    repeat = int(data.get('repeat', 1))
    passwords = [
        generator.PassWord(
            count=count,
            insertNumbers=insertNumbers,
            insertSpecial=insertSpecial,
            insertChars=insertChars,
            insertUpper=insertUpper
        )
        for _ in range(repeat)
    ]
    return jsonify({'passwords': passwords})

@app.route('/api/generate', methods=['GET'])
def api_generateGet():
    passwords = [
        generator.PassWord(
            count=4,
            insertNumbers=False,
            insertSpecial=False,
            insertChars=False,
            insertUpper=False
        )
        # for _ in range(1
    ]
    return jsonify({'passwords': passwords})



if __name__ == '__main__':
    app.run(debug=True, port=5100)