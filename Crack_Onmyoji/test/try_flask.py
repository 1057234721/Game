from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/baidu')
def baidu():
    return redirect('http://www.baidu.com')


if __name__ == '__main__':
    app.run(debug=True)
