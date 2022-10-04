from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome_screen():
    return "<p>Hot chicken rankings!</p>"

@app.route('/leaderboard')
def projects():
    return 'The best of the hot chickens'

@app.route('/bounties')
def about():
    return 'My most wanted chickens'

@app.route('/judge')
def projects():
    return 'Time to rank some hot chickens'

@app.route('/suggest')
def about():
    return 'Leave me a suggestion of who to eat next'
