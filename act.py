"""
    act.py - Actually performs the action requested by /u/SurprisedPotato, to go through the logged in user's comments, edit them, and make a post in /r/ImaginedDialogs
    Copyright (c) 2016 Brendan McGuire (/u/MayorMonty)
"""

# Python 3 print function
from __future__ import print_function
# Reddit API Wrapper
import praw
# Check for file existence
import os
# Loading the saved access information
import pickle
# So I can exit
import sys

print("0. Importing access information...", end="")
# Import access information
if os.path.isfile("pickles/access.p"):
    with open('pickles/access.p','rb') as f:
         access_information = pickle.load(f)
else:
    print("Error!\nError: The file 'pickles/access.p' doesn't exist. Did you run 'authorize.py'?")
    sys.exit(1)
if os.path.isfile("pickles/app.p"):
    with open('pickles/app.p','rb') as f:
         app = pickle.load(f)
else:
    print("Error!\nError: The file 'pickles/app.p' doesn't exist. Did you run 'config.py'?")
print("Done")



print("1. Initalizing PRAW...", end="")
r = praw.Reddit('ImaginedDialogs/v1.0 (made by /u/MayorMonty)')
r.set_oauth_app_info(app["CLIENT_ID"], app["CLIENT_SECRET"], app["REDIRECT_URI"])
r.set_access_credentials(**access_information)
print("Done")



print("2. Retriving comments...")
comments = list(r.get_me().get_comments())
i = 1
for comment in comments:
    if comment.id == app["LATEST"]:
        print("   All comments have been handled\nDone")
        break
    print("   2.%s. %s " % (i, comment.id))
    i+=1
    print("          2.%s.1 Making the post..." % i, end="")
    title = comment.body.split("\n")[0]
    r.get_subreddit("ImaginedDialog").submit(title = "Imagined Dialog: %s" % title, url = comment.permalink)
    print("Done")
    print("          2.%s.2 Editing the original comment..." % i, end="")
    comment.edit("%s\n****\nSee more of my wild imaginings at /r/ImaginedDialogue" % comment.body)
    print("Done")
app["LATEST"] = comments[0].id



print("3. Updating comment log...",end="")
pickle.dump(app, open("pickles/app.p", "w"))
print("Done")
