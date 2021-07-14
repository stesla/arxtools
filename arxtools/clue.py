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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'tags': self.tags,
            'source': self.source,
            'share_note': self.share_note,
        }

def parse_clue(html):
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.select('td')

    id = int(tds[0].string)

    title = tds[1].string

    text = ''
    for child in tds[2].children:
        if 'br' == child.name:
            text += '\n'
        elif 'div' == child.name:
            pass
        else:
            text += child.string.strip()

    hastags = tds[2].find('strong')
    if hastags:
        tags = [s.strip() for s in hastags.next_sibling.string.split(', ')]
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
