from flask import Flask
from setup import create_app

app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
