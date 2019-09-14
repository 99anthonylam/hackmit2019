from flask import Flask, render_template, request
import jinja2
from collections import defaultdict

app = Flask(__name__, static_url_path='', static_folder='static')
db = defaultdict(str)
curr = 0

# create a new journal entry // display old journal entries
@app.route('/')
def home():
	# TO DO: bootstrap grid on html page to display all old entried in db
	return render_template('home.html')

# save the current journal entry
@app.route('/save', methods = ['POST'])
def save_journal_entry():
	global curr
	text = request.form['curr_text']
	db[curr] = str(text)
	print(db)

	return render_template('home.html')

# complete the current journal entry
@app.route('/complete', methods = ['POST'])
def complete_journal_entry():
	# TO DO: some sort of alert/verification that the post has been saved
	global curr
	text = request.form['journal-entry']
	db[curr] = str(text)
	curr += 1
	return render_template('home.html')


if __name__ == '__main__':
	app.run('localhost', 8888, debug=True)