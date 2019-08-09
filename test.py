#!/usr/bin/python
from bot import *

d = hash_file("lamm.txt")
print "You may begin talking to me, cretin. Say 'I hate you' to quit."
while 1:
    response = raw_input("> ")
    if response == "I hate you":
        break
    elif not response:
        print "I have nothing to say to that"
    else:
        print reply(response.lower(), d)
