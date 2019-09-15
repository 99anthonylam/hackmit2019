from flask import Flask, render_template, request, redirect, url_for
import jinja2
from collections import defaultdict
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__, static_url_path='', static_folder='static')

class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        register = BooleanField('I am a new user registering.')
        submit = SubmitField('Sign In/Register')


class User:
        def __init__(self):
                self.users = {}

        def add_user(self, username, password):
                if username not in self.users:
                        self.users[username] = password

        def change_pwd(self, username, old_pwd, new_pwd):
                if username in self.users and self.users[username] == old_pwd:
                        self.users[username] = new_pwd

        def del_user(self, username, password):
                if username in self.users and self.users[username] == password:
                        self.users.pop(username)

        def user_exists(self, username, password):
                return username in self.users and self.users[username] == password

class Entry:
        def __init__(self, user, ide):
                self.user = user
                self.created_at = datetime.now()
                self.last_modified = self.created_at
                self.content = ''
                self.id = ide

        def update_entry(self, content):
                self.last_modified = datetime.now()
                self.content = content

        def printentry(self):
            print('{} {}'.format(self.id, self.content))

user_db = User()
journals = defaultdict(list)  # contains all journal entries

curr_user = None
validated = False
curr_entry = None
error = None

# create a new journal entry // display old journal entries
@app.route('/', methods = ['GET'])
def home():
        global curr_entry
        global curr_user
        global journals

        #curr_entry = len(journals.get(curr_user, []))
        curr_entry = Entry(curr_user, len(journals.get(curr_user, [])))
        return render_template('home.html', entries=journals[curr_user])

# check that a user is logged in before allowing them to access other pages
@app.before_request
def check_user():
        global validated

        if not validated and request.endpoint != 'login' and request.endpoint != 'static' and request.endpoint != 'validate_login':
                return render_template('login.html', title='Sign In/Register', form=LoginForm(), error=error)


# login page
@app.route('/login', methods=['GET'])
def login():
        return render_template('login.html', title='Sign In/Register', form=LoginForm())


# validates login information, sends user to home or login page if error
@app.route('/login', methods=['POST'])
def validate_login():
        global validated
        global curr_user
        global journals
        global user_db
        global error

        new_user = request.form.get('register', False)
        username = request.form['username']
        password = request.form['password']

        # register new user
        if new_user:
                print('new')
                if request.form['username'] in user_db.users:
                        error='Sorry, that username has been taken. Please choose another one.'
                        return render_template('login.html', title='Sign In/Register', form=LoginForm(), error=error)
                else:
                        user_db.add_user(request.form['username'], request.form['password'])
                        curr_user = username
                        validated = True
                        #return render_template('home.html', entries=journals[curr_user])
                        return home()

        # login existing user
        else:
                print('login')
                if user_db.user_exists(username, password):
                        curr_user = username
                        validated = True
                        print('aa')
                        #return render_template('home.html', entries=journals[curr_user])
                        return home()
                else:
                        error='Sorry, your username and/or password is incorrect.'
                        return render_template('login.html', title='Sign In/Register', form=LoginForm(), error=error)


# logout page
@app.route('/logout')
def logout():
        global curr_user
        global validated
        global error
        global curr_entry

        curr_user = None
        validated = False
        error = None
        curr_entry = 0
        return render_template('login.html', title='Register/Sign In', form=LoginForm())





# save the current journal entry
@app.route('/save', methods = ['POST'])
def save_journal_entry():
        global curr_entry
        global curr_user
        global journals

        text = str(request.form['curr_text'])
        #if len(journals[curr_user]) == curr_entry:
        #        journals[curr_user].append(text)
        #else:
        #        journals[curr_user][curr_entry] = text
        curr_entry.update_entry(text)
        
        if len(journals[curr_user]) == curr_entry.id:
                journals[curr_user].append(curr_entry)
        else:
                journals[curr_user][curr_entry.id] = curr_entry
                
        for entry in journals[curr_user]:
            entry.printentry()
        
        return render_template('home.html', entries=journals[curr_user])




# complete the current journal entry
@app.route('/', methods = ['POST'])
def complete_journal_entry():
        global curr_entry
        global curr_user
        global journals

        # TO DO: some sort of alert/verification that the post has been saved
        text = str(request.form['journal-entry'])
        
        curr_entry.update_entry(text)
        
        if len(journals[curr_user]) == curr_entry.id:
                journals[curr_user].append(curr_entry)
        else:
                journals[curr_user][curr_entry.id] = curr_entry
        
        #curr_entry += 1
        curr_entry = Entry(curr_user, len(journals.get(curr_user, [])))
        
        
        
        
        return render_template('home.html', entries=journals[curr_user])


@app.route('/past', methods = ['POST'])
def past_journal_entry():
    global curr_entry
    global curr_user
    global journals
    
    ide = int(request.form['past-entry-num'])
    curr_entry = journals[curr_user][ide]
    
    return render_template('home.html', entries=journals[curr_user])

if __name__ == '__main__':
        app.secret_key = 'TEMP_KEY!'
        app.run('localhost', 8888, debug=True)

