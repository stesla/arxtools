import os
from arxtools.clue import Clue, ClueSet

def export_clues(clues, directory):
    tags = {}
    sources = {}
    
    def maybe_make_dir(name):
        try:
            os.makedirs(os.path.join(directory, name))
        except FileExistsError:
            pass
    
    maybe_make_dir("Clue")
    for clue in clues:
        path = os.path.join(directory, "Clue", clue.name + '.md')
        with open(path, 'w') as f:
            print(clue.markdown, file=f)
    
        for t in clue.tags:
            try:
                tag = tags[t]
            except KeyError:
                tag = ClueSet('Tag', t)
                tags[t] = tag
            tag.add_clue(clue)
    
        if clue.source is None:
            s = 'No Source'
        else:
            s = clue.source
        try:
            source = sources[s]
        except KeyError:
            source = ClueSet('Source', s)
            sources[s] = source
        source.add_clue(clue)
    
    maybe_make_dir("Tag")
    for tag in tags.values():
        path = os.path.join(directory, 'Tag', tag.name + '.md')
        with open(path, 'w') as f:
            print(tag.markdown, file=f)
    
    maybe_make_dir("Source")
    for source in sources.values():
        path = os.path.join(directory, 'Source', source.name + '.md')
        with open(path, 'w') as f:
            print(source.markdown, file=f)

