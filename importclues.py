import os

from dotenv import load_dotenv
from requests_html import HTMLSession
from arxtools.clue import parse_clue

# Get credentials from environment
load_dotenv()
username = os.getenv('ARX_USERNAME')
password = os.getenv('ARX_PASSWORD')

s = HTMLSession()

# First we request the login form so we can get the needed CSRF token for the
# login form.
r = s.get('https://play.arxmush.org/accounts/login?next=/')
csrf = r.html.find('[name="csrfmiddlewaretoken"]')[0].attrs.get('value') 

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

r = s.get(clues_url)
for html in r.html:
    rows = html.find('tr')
    for row in rows:
        # The table doesn't have a thead section with the header, it just has a row
        # that has this class on it.
        cls = row.attrs.get('class', [])
        if 'danger' in cls:
            continue
        clue = parse_clue(row.html)
        print(clue)
