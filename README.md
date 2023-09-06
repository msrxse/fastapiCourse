# FastAPI Course

## Create env

`python3 -m venv venv`

## Set default interpreter in vscode

- `CTRL+SHIFT+P` and search `Python:Select interpreter`
Choose the one within the venv folder
Also ensure is activated in console within vscode (reopen console if necessary)
(the prompt should be preceded by `(venv)`)
- Or activate source from within console

``` source venv/bin/activate ```

## Install FastAPI

`pip install fastapi`
`pip install "uvicorn[standard]"`

## Review installed packages

`pip freeze`

- All these packages are within the `venv/lib` folder

## Autoformatter

`pip install black`

ALso set default formatter automatically on save

- (Setting up python Black on Visual Studio Code ) [https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00]

## Start the web server

`uvicorn app.main:app --reload` // app=folder, file=main, name of fastapi instance = app

- You can visit `http://localhost:8000/`
- The docs are at `http://localhost:8000/docs`

## Git

- Generate gitignore with `python` and `venv`

- [visit here to generate gitignore file](https://www.toptal.com/developers/gitignore)

- Afterwards git init commit and push changes to new repo
