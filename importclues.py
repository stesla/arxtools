import os
import re

from requests_html import HTMLSession

s = HTMLSession()

# First we request the login form so we can get the needed CSRF token for the
# login form.
r = s.get('https://play.arxmush.org/accounts/login?next=/')
csrf = r.html.find('[name="csrfmiddlewaretoken"]')[0].attrs.get('value') 

# Get credentials from environment
username = os.getenv('ARX_USERNAME')
password = os.getenv('ARX_PASSWORD')

# Now we login
r = s.post('https://play.arxmush.org/accounts/login',
        data = {
            'csrfmiddlewaretoken': csrf,
            'username': username, 
            'password': password,
            'next': '/',
        })

# Scrape the page for the character sheet link
sheet_url = r.html.find('a', containing='Logged in as')[0].absolute_links.pop()

# Scrape that page for the clues URL
r = s.get(sheet_url)
clues_url = r.html.find('a', containing='Clues')[0].absolute_links.pop()

class Clue:
    def __init__(self, id, title, text, tags, source):
        self.id = int(id)
        self.title = title
        self.text = text
        self.tags = tags
        self.source = source

    def __repr__(self):
        return f'<Clue {self.id} "{self.title}" {clue.tags}>'

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

r = s.get(clues_url)
for html in r.html:
    rows = html.find('tr')
    for row in rows:
        # The table doesn't have a thead section with the header, it just has a row
        # that has this class on it.
        cls = row.attrs.get('class', [])
        if 'danger' in cls:
            continue
        clue = parse_clue(row)
        print(clue)
