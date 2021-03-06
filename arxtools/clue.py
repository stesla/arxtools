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

    def from_dict(d):
        return Clue(d['id'], d['title'], d['text'], d['tags'], d['source'], d['share_note'])

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'tags': self.tags,
            'source': self.source,
            'share_note': self.share_note,
        }

    @property
    def name(self):
        base = f'{self.id} - {self.title}'
        return re.sub(r'\*|\"|\\|/|<|>|:|\||\?', ' - ', base).replace('#','').strip()

    @property
    def markdown(self):
        if self.source is None:
            source = 'No Source'
        else:
            source = self.source

        if self.share_note is None:
            share_note = 'No Share Note'
        else:
            share_note = self.share_note

        taglist = ', '.join(f'[[{tag}]]' for tag in self.tags)

        return f'''
### Clue {self.id} - {self.title}

{self.text}

Source: [[{source}]]

Share Note: {share_note}

Tags: {taglist}
'''

def parse_clue(html):
    soup = BeautifulSoup(html, 'lxml')
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

    hasmeta = tds[2].find('div')
    if not hasmeta:
        return Clue(id, title, text, [], None, None)

    shinfo = hasmeta.contents[-1]

    hastags = tds[2].find('strong')
    if hastags:
        tags = [s.strip() for s in hastags.next_sibling.string.split(', ')]
        shinfo = _parse_shinfo_with_clue(hasmeta)
    else:
        tags = []
        shinfo = _parse_shinfo_without_clue(hasmeta)

    source = None
    share_note = None
    if shinfo:
        m = re.search('This clue was shared with you by ([a-zA-Z]+)', str(shinfo))
        if m:
            source = m.group(1)
            m = re.search('who noted: (.*)', str(shinfo), re.S)
            if m:
                share_note = m.group(1).strip()

        if tds[2].find(string=re.compile('Your investigation')):
            source = 'investigation'

        if source is None:
            share_note = shinfo.strip()

    return Clue(id, title, text, tags, source, share_note)

def _parse_shinfo(node):
    result = ''
    while node:
        if 'br' == node.name:
            result += '\n'
        else:
            result += str(node.string).strip()
        node = node.next_sibling
    return result

def _parse_shinfo_with_clue(meta):
    node = meta.find('strong').next_sibling.next_sibling
    return _parse_shinfo(node)

def _parse_shinfo_without_clue(meta):
    node = meta.contents[0]
    return _parse_shinfo(node)

class ClueSet:
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        self.clues = []

    def add_clue(self, clue):
        self.clues.append(clue)

    @property
    def markdown(self):
        clues = sorted(self.clues, key=lambda c: c.id)
        clue_links = '\n'.join(f'- [[{clue.name}]]' for clue in clues)
        return f'''
### {self.kind} - {self.name}

{clue_links}
'''
