from flask import render_template

from project import create_app

app = create_app()


@app.route("/")
def hello():
    return render_template('index.html')
