# parse.py -- parse input formats

import re

def read_disk(fn):
    return [l for l in [l.strip() for l in open(fn)] if l]

def parse_transposition(s):
    assert re.match("^(\([0-9]+ [0-9]+\))*$", s), repr(s)
    l = re.findall("\([0-9]+ [0-9]+\)", s)
    l = [s.replace("(", "").replace(")", "").split() for s in l]
    tr = {}
    for a, b in l:
        tr[int(a)] = int(b)
        tr[int(b)] = int(a)
    return tr

e = lambda v, w: frozenset([v, w])

def parse_edge(s):
    return e(*sorted(re.findall("[1-3A-C]", s)))

def parse_edges(s):
    if not re.search("\[[1-3A-C], ?[1-3A-C]\]", s):
        return []
    edges = re.findall("\[[1-3A-C], ?[1-3A-C]\]", s)
    return [parse_edge(ed) for ed in edges]


