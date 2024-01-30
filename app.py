from setup import create_app

"""This module starts the flask web server"""

app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
