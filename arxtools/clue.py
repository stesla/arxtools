import re
from bs4 import BeautifulSoup

class Clue:
    def __init__(self, id, title, text, tags, source, share_note):
        self.id = int(id)
        self.title = title
        self.text = text
        self.tags = tags
        self.source = source
        self.share_note = share_note

    def __repr__(self):
        return f'<Clue {self.id} "{self.title}" {self.tags}>'

def parse_clue(html):
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.select('td')

    id = int(tds[0].string)
    title = tds[1].string
    text = tds[2].contents[0].strip()
    hastags = tds[2].find('strong')
    if hastags:
        tags = hastags.next_sibling.string.strip().split(', ')
    else:
        tags = []

    source = None
    share_note = None
    shinfo = tds[2].find(string=re.compile('This clue was'))
    if shinfo:
        m = re.search('This clue was shared with you by ([a-zA-Z]+)', shinfo)
        source = m.group(1)
        m = re.search('who noted: (.*)', shinfo)
        if m:
            share_note = m.group(1).strip()
    elif tds[2].find(string=re.compile('Your investigation')):
        source = 'investigation'

    return Clue(id, title, text, tags, source, share_note)
