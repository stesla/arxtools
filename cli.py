import click
import configparser
import json
import sys

from arxtools import export_clues, fetch_clues
from arxtools.clue import Clue

@click.group()
def cli():
    pass

def get_character_info(name):
    config = configparser.ConfigParser()
    config.read('arxtools.ini') 
    try:
        return config[name.lower()]
    except KeyError:
        click.echo(f'No character named "{name}" found.', err=True)
        sys.exit(1)

@cli.command("import")
@click.argument('name')
def import(name):
    info = get_character_info(name)
    username = info['username']
    password = info['password']

    click.echo(f'Fetching clues for {username}.', err=True)
    clues = fetch_clues(username, password)
    click.echo(json.dumps(clues))

@cli.command("export")
@click.argument('name')
def export(name):
    info = get_character_info(name)
    directory = info['directory']

    click.echo("Exporting to markdown in " + directory)
    clues = [Clue.from_dict(c) for c in json.load(sys.stdin)]
    export_clues(clues, directory)

if __name__ == '__main__':
    cli()
