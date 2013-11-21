#!/usr/bin/python
"""pyTranslate

Usage:
  pyTranslate [--from=<lang>] [--to=<lang>]

Options:
  --from=<lang>    From language [default: auto].
  --to=<lang>      To language [default: en].
"""

import urllib2, urllib
import pynotify
import subprocess
from BeautifulSoup import BeautifulSoup
from docopt import docopt


def show_notification(text):
    pynotify.init("PyTranslate")
    alert = pynotify.Notification("PyTranslate", text)
    alert.set_timeout(pynotify.EXPIRES_NEVER)
    alert.show()

def get_selection():
    selection = subprocess.Popen(["xclip", "-o"], stdout=subprocess.PIPE).communicate()[0]
    return selection

def translate(to_translate, from_language="auto", to_language="auto"):

    headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    params = {'hl': to_language, 'sl': from_language, 'q': to_translate.encode('utf8')}
    query_string = urllib.urlencode(params)

    link = "http://translate.google.com/m?" + query_string
    request = urllib2.Request(link, headers=headers)
    page = urllib2.urlopen(request).read()

    soup = BeautifulSoup(page)
    div = soup.find('div', {'class': 't0'})
    result = div.renderContents()

    result = result.replace('.', '.\n')

    return result

if __name__ == '__main__':
    args = docopt(__doc__, version='pyTranslate 0.1')

    to_translate = get_selection()
    translated_text = translate(to_translate, from_language=args['--from'], to_language=args['--to'])
    show_notification(translated_text)


