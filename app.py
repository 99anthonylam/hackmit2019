from flask import Flask, render_template, request
import jinja2
from collections import defaultdict
import datetime

# class User:
# 	def __init

# class Users:
# 	def __init__(self):
# 		self.users = {}

# 	def add_user(self, username, password):
# 		if username not in self.users:
# 			self.users[username] = password

# 	def change_pwd(self, username, old_pwd, new_pwd):
# 		if username in self.users and self.users[username] == old_pwd:
# 			self.users[username] = new_pwd

# 	def del_user(self, username, password):
# 		if username in self.users and self.users[username] == password:
# 			self.users.pop(username)


# class Journals:



# class Entry:
# 	def __init__(self, user):
#         self.user = user
#         self.created_at = datetime.now()
#         self.last_modified = self.created_at
#         self.content = ''

#     def update_entry(self, content):
#     	self.last_modified = datetime.now()
#     	self.content = content





app = Flask(__name__, static_url_path='', static_folder='static')
db = defaultdict(str)
curr = 0

# create a new journal entry // display old journal entries
@app.route('/', methods = ['GET'])
def home():
	# TO DO: bootstrap grid on html page to display all old entried in db
	return render_template('home.html', variable='hello!!')

# save the current journal entry
@app.route('/save', methods = ['POST'])
def save_journal_entry():
	global curr
	text = request.form['curr_text']
	db[curr] = str(text)
	print(db)

	return render_template('home.html')

# complete the current journal entry
@app.route('/', methods = ['POST'])
def complete_journal_entry():
	# TO DO: some sort of alert/verification that the post has been saved
	global curr
	text = request.form['journal-entry']
	db[curr] = str(text)
	curr += 1
	return render_template('home.html')


if __name__ == '__main__':
	app.run('localhost', 8888, debug=True)