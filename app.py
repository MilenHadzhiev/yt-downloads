"""This module starts the flask web server"""

from backend.setup import create_app


app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
