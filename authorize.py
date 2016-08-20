"""
    authorize.py - Generates access tokens, so 'act.py' can go through each comment
    Copyright (c) 2016 Brendan McGuire (/u/MayorMonty)
"""

# Python 3 print function
from __future__ import print_function
# Webserver to allow callbacks
from flask import Flask, request
# Reddit API Wrapper
import praw
# To Save the access information
import pickle
# To disable Flask logging
import logging
# So I can exit once authorized
import sys

# Set logging level for Flask to ERROR only
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

with open('pickles/app.p','rb') as f:
     app = pickle.load(f)

def go(access_information):
    """Saves the access token to be used later"""
    print("3. Saving access information...", end="")
    data = open("pickles/access.p", "w")
    data.write(
        pickle.dumps(
            access_information
        )
    )
    print("Done (saved to access.p)")
    print("4. Now run the python script 'act.py' (and set it up on a cron job)")
    sys.exit(0)



@app.route('/')
def homepage():
    print("Done")
    print("2. Account Authorizing...", end="")
    text = ""
    link_refresh = r.get_authorize_url('DifferentUniqueKey',
                                       refreshable=True,
                                       scope="edit read submit identity history")
    link_refresh = "<a href=%s>Click Here</a>" % link_refresh
    text += "%s (Grants the application access)" % link_refresh
    return text

@app.route('/authorize_callback')
def authorized():
    print("Done")
    state = request.args.get('state', '')
    code = request.args.get('code', '')
    info = r.get_access_information(code)
    user = r.get_me()
    variables_text = "State=%s, code=%s, info=%s." % (state, code,
                                                      str(info))
    text = 'You are %s and have %u link karma.' % (user.name,
                                                   user.link_karma)
    back_link = "<a href='/'>Try again</a>"
    go(info)
    return variables_text + '</br></br>' + text + '</br></br>' + back_link


if __name__ == '__main__':
    r = praw.Reddit('ImaginedDialogs/v1.0 (made by /u/MayorMonty)')
    r.set_oauth_app_info(app["CLIENT_ID"], app["CLIENT_SECRET"], app["REDIRECT_URI"])
    app.run(debug=False, port=65010, host="0.0.0.0")
    print("0. Server Start...Done (at 0.0.0.0:65010)")
    print("1. Home Page Access...", end="")
