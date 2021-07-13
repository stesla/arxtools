import re

class Clue:
    def __init__(self, id, title, text, tags, source):
        self.id = int(id)
        self.title = title
        self.text = text
        self.tags = tags
        self.source = source

    def __repr__(self):
        return f'<Clue {self.id} "{self.title}" {self.tags}>'

def parse_clue(row):
    tds = row.find('td')
    id = tds[0].text
    title = tds[1].text
    text = tds[2].text
    tags = []
    source = None
    meta = tds[2].find('div.well')
    if meta:
        text = text.split(meta[0].text)[0].strip()
        parts = meta[0].text.split('\n')
        m = re.match('Clue Tags: (.*)', parts[0])
        if m:
            tags = m.group(1).split(', ')
            if len(parts) > 1:
                source = parts[-1]
        else:
            source = parts[0]
    return Clue(id, title, text, tags, source)
