import json
import os
import sys

from arxtools.clue import Clue, ClueSet

try:
    output_dir = sys.argv[1]
except:
    print(f"USAGE: python {sys.argv[0]} OUTPUT_DIR", file=sys.stderr)
    sys.exit(1)

clues = json.load(sys.stdin)
tags = {}
sources = {}

os.makedirs(os.path.join(output_dir, "Clue"))
for clue in [Clue.from_dict(c) for c in clues]:
    path = os.path.join(output_dir, "Clue", clue.name + '.md')
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

os.makedirs(os.path.join(output_dir, "Tag"))
for tag in tags.values():
    path = os.path.join(output_dir, 'Tag', tag.name + '.md')
    with open(path, 'w') as f:
        print(tag.markdown, file=f)

os.makedirs(os.path.join(output_dir, "Source"))
for source in sources.values():
    path = os.path.join(output_dir, 'Source', source.name + '.md')
    with open(path, 'w') as f:
        print(source.markdown, file=f)
