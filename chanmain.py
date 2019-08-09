#!/usr/bin/python

import time

from apichan import *
from bot import *

BOARD = "/g/"
PAGES = 4
DICTIONARY = hash_file("lamm.txt")

def find_threads():
    """Find all the programming threads on the first four pages."""
    for page in range(PAGES):
        for thread in threads(BOARD, make_soup(URL_BASE + BOARD + str(page))):
            if find("programming", make_soup(thread), content):
                yield thread

def create_response(thread):
    """Return (postno, response) for the wordiest response or None."""
    response = (0, "")
    length = 0
    for post in posts(make_soup(thread)):
        msg = reply(".".join(content(post).split("\n")).lower(), DICTIONARY)
        if msg is None:
            continue
        tmplen = len(msg)
        poster = int(postno(post))
        if poster > response[0] and tmplen > length:
            response = (poster, msg)
            length = tmplen
    return response

def main():
    threads = list(find_threads())
    discussions = dict(zip(threads, [create_response(thread) for thread in threads]))
    while 1:
        for thread in threads:
            response = create_response(thread)
            if response[0] > discussions[thread][0]:
                discussions[thread] = response
                print "In response to {0} in {1}:\n\n{2}".format(response[0], thread, response[1])
        time.sleep(20)

if __name__ == "__main__":
    main()
