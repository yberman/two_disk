#!/usr/bin/python3
"""
to_json.py

Parse our ad-hoc graph format.
"""

import pathlib
import os
from parse import *
import json

def parse_file(fn):
    l = read_disk(fn)
    tr = parse_transposition(l[0])
    adj = l[1].split()
    adj = [x if x != "0" else "" for x in adj]
    ed = parse_edges(l[2])
    tr_l = [0] * len(tr)
    for k, v in tr.items():
        tr_l[k-1] = v-1
    interior =list(sorted(set(x for x in adj if x)))
    ed = [tuple(sorted(x)) for x in ed]
    r = {
            "Filename": os.path.basename(fn),
            "EnterExitTrans": tr_l,
            "InteriorVertices": interior,
            "BoundaryInteriorEdge": adj,
            "InteriorEdges": ed,
        }
    return r


lowell = pathlib.Path(__file__).parent.absolute().joinpath('lowell')
for fn in sorted(lowell.glob("*")):
    print(json.dumps(parse_file(str(fn))))
