#!/usr/bin/python3
# data.py -- compare Lowell's and my encoding. This is bad code.

import os
import re
from parse import *

dir1 = "lowell"
dir2 = "yosef"

assert os.listdir(dir1) == os.listdir(dir2)

e = lambda v, w: frozenset([v, w])

for fn in sorted(os.listdir(dir1)):
    fn1 = os.path.join(dir1, fn)
    fn2 = os.path.join(dir2, fn)

    l1 = read_disk(fn1)
    l2 = read_disk(fn2)

    # confirm transpositions are equal
    t1 = parse_transposition(l1[0])
    t2 = parse_transposition(l2[0])
    assert t1 == t2

    # confirm interiors are equal
    in1 = l1[1].split()
    in2 = l2[1].split()
    assert len(in1) == len(in2)

    m = dict(zip(in1, in2))
    m_inv = dict(zip(in2, in1))
    assert in1 == [m_inv[i] for i in in2]
    assert in2 == [m[i] for i in in1]

    # confirm interior edges are equal 
    ed1 = parse_edges(l1[2])
    ed2 = parse_edges(l2[2])
    assert set(ed1) == set(e(m_inv[v], m_inv[w]) for (v, w) in ed2)
    assert set(ed2) == set(e(m[v], m[w]) for (v, w) in ed1)
