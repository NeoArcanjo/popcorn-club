from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run()
