# passWordPhrase

## Overview
This project provides a password phrase generator using words from a dictionary and optional separator characters. 
The implementation is for reference only and is not to be used in production as flask is known to have known vulnerabilities.

It includes:
- [`passWordPhrase.py`](passWordPhrase.py): Command line support and core logic for password phrase generation. 
- [`password_gui.py`](password_gui.py): Tkinter GUI for generating password phrases.
- [`password_web.py`](password_web.py): Flask web app for password phrase generation.
- [`password_api.py`](password_api.py): Flask REST api for password phrase generation.
- [`pythonTests/test_passWordPhrase.py`](pythonTests/test_passWordPhrase.py): Unit tests for the generator.

## Requirements
- Python 3.7+
- `tkinter` (for GUI)
- `flask` (for web app)

## Usage 
Run from same directory as repo or fully qualify the path to the calling python file.

### Command Line
    1. Run the password generator from the command line for a single password
        python passWordPhrase.py        
    2. Generate 3 passwords 
        python passWordPhrase.py --count 4 --insertNumbers --insertSpecial --repeat 3
    3. For command line query for argument help 
        python passWordPhrase.py --help

### Tkinter based GUI
    1. Start tkinter app
        python password_gui.py
    2. Navigate the UI and enter in the desired parameters.


### Web Server
    1. Start flask web server
        python password_web.py
    2. Access and run the web client via your favorite browser
    You will be able to generate 1 to 20 passwords and save it out to a file.
        http://127.0.0.1:5000/


### API
    Run the generator to generate a password as an API that returns JSON content. Use curl, burpsuite, or web to generate POST.

    Note the Windows Cygwin version 2.934 curl version does not work with these curl commands. You will have to use the Windows WSL with Ubuntu which was test ed with these curl commands. 

    Run server and Submit Command
    1. Run server once
        - python password_api.py
    2. Get password from server
        - one four word password (default) which can be done with GET
            curl -X GET http://localhost:5100/api/generate

        - one four word password with an empty POST
            curl -X POST http://localhost:5100/api/generate -H "Content-Type: application/json" -d '{}'

        - one four word password with fully filled out POST 
            curl -X POST http://localhost:5100/api/generate   -H "Content-Type: application/json"   -d '{"count": 4, "insertNumbers": true, "insertSpecial": false, "insertChars": false, "insertUpper": false, "repeat": 1}'

        - five 3 word passwords with numbers and special characters between. 
            curl -X POST http://localhost:5100/api/generate   -H "Content-Type: application/json"   -d '{"count": 3, "insertNumbers": true, "insertSpecial": true, "insertChars": false, "insertUpper": false, "repeat": 5}'

        - Three 2 word passwords with numbers, special characters, characters, and upper word characters interspersed in between. 
            curl -X POST http://localhost:5100/api/generate   -H "Content-Type: application/json"   -d '{"count": 2, "insertNumbers": true, "insertSpecial": true, "insertChars": true, "insertUpper": true, "repeat": 3}'
