from flask import render_template, request

from project import create_app

app = create_app()

@app.route("/")
def index():
    return render_template('index.html')