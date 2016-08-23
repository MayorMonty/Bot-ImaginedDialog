"""
    config.py - Generates the app configuration (and stores it in pickles/app.pickle)
    Copyright (c) 2016 Brendan McGuire (/u/MayorMonty)
"""
# Python 3 print function
from __future__ import print_function
# Takng input from STDIN
import fileinput
# Allow pickling of config
import pickle
# Allow the creation/testing of the pickles/ directory
import os


if not os.path.exists("pickles"):
    os.makedirs("pickles")


# Configure the app dict
app = {
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "REDIRECT_URI": "",
    "LATEST": ""
}
prompt = ["CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI"]
i = 0
stdin = fileinput.input()
print("%s: " % prompt[i], end="")
for line in stdin:
    app[prompt[i]] = line.replace("\n", "")
    i+=1
    if len(prompt) - 1 < i:
        break
    print("%s: " % prompt[i], end="")


print(app)
print("OK? (Y/n) ", end="")
for line in stdin:
    if line is "n" or line is "N":
        print("\nNot saving to pickles/app.p")
        sys.exit(1)
    else:
        print("\nSaving to pickles/app.p...",end="")
        pickle.dump(app, open("pickles/app.p", "w"))
        print("Done")
    break
