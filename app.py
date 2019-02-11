from flask import Flask, render_template, redirect, url_for, request
import praw
from datetime import datetime
from psaw import PushshiftAPI
import configparser




app = Flask(__name__)
config = configparser.ConfigParser()
config.read('auth.ini')
reddit = praw.Reddit(client_id=config.get('reddit', 'client_id'),
                     client_secret=config.get('reddit', 'client_secret'),
                     user_agent='Comments in reverse')
api = PushshiftAPI(reddit)



@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return (user())
    else:
        return render_template('index.html')

@app.route('/user', methods = ['GET', 'POST'])
def user():
    if request.method == 'POST':
        result = request.form
        gen = api.search_comments(author=str(result['username']))
        new_list = []
        for c in gen:
            new_list.append(c)

        return render_template("user.html", comments = new_list[::-1])
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
