import urllib2
import re
import BeautifulSoup

URL_BASE = "http://boards.4chan.org"
POST_MODE = "post"
NAME_MODE = "name"
TRIP_MODE = "trip"
IMAG_MODE = "image"
SCRP_MODE = "scrape"

def make_soup(url):
    """Create a BeautifulSoup object from the source code for a page at url."""
    return BeautifulSoup.BeautifulSoup(urllib2.urlopen(url).read())

def threads(board, soup):
    """Return the reply link corresponding to each thread on a page."""
    res = re.compile("res/\d+")
    return list(set([URL_BASE + board + t["href"] 
              for t in soup.findAll("a", { "href": res, "class": "replylink" })]))

def posts(soup):
    """Get the the block of HTML corresponding to a user post on a thread."""
    replies = soup.findAll("div", { "class": "post reply" })
    op = soup.findAll("div", { "class": "post op" })
    return op + replies

def name(postsoup):
    """Get the name of the poster from a specific post block."""
    username = postsoup.find("span", { "class": "name" }).contents
    return username[0] if username else ""  # Some people use just a trip.

def trip(postsoup):
    """Get the tripcode of the poster from a post block if one exists."""
    trip = postsoup.find("span", { "class": "postertrip" })
    return trip.contents[0] if trip else ""

def image(postsoup):
    """Get the url for the image the poster used if they used one."""
    img = postsoup.find("a", { "class": "fileThumb" })
    if img is not None:
        return "http:" + img["href"]

def postno(postsoup):
    """Get the post number corresponding to a post."""
    return postsoup.find("div", { "class": "postInfo desktop" })["id"][2:]

def content(postsoup):
    """Get the actual contents of the poster's post."""
    def cjoin(splitter, contents):
        if not contents:
            return u""
        if isinstance(contents[0], BeautifulSoup.Tag):
            return cjoin(splitter, contents[0].contents) + cjoin(splitter, contents[1:])
        return splitter + contents[0].replace("&gt;", ">") + cjoin(splitter, contents[1:])
    return cjoin(u"\n", postsoup.find("blockquote", { "class": "postMessage" }).contents)

def download_image(url, dest):
    """Store the contents of a url in a file."""
    open(dest, "w").write(urllib2.urlopen(url).read())

def find(text, soup, data_func):
    """Check if text can be found in the data pulled from soup using in_func."""
    return [postno(post) for post in posts(soup) if text in data_func(post)]

def scrape(url):
    """Download all the images from a given thread."""
    soup = make_soup(url)
    for post in posts(soup):
        img = image(post)
        if img: download_image(img, img[img.rindex("/") + 1:])
