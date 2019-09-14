from flask import Flask, render_template, request
import jinja2

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def home():
	# page with a text editor that will 'save' the typed text
    return render_template('home.html')

if __name__ == '__main__':
	app.run('localhost', 8888, debug=True)