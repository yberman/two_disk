"""
connect.py

Connect two disks with transversal, and return graph which it forms as an immersion.

By connect we mean take two disks, insert edges between corresponding vertices.
"""

import collections
import copy
import logging
import pprint

import graph

VS = collections.namedtuple("VerexSide", "vertex side")
LHE = collections.namedtuple("LabeledHalfEdge", "side base index")
TV = collections.namedtuple("TypeValue", ["type", "value"])

def connect(dwt1, dwt2, twist):
    g = graph.Graph()

    half_edges = []

    assert dwt1.circum == dwt2.circum, "? %s %s" % (dwt1, dwt2)
    if dwt1 == dwt2:
        dwt2 = copy.deepcopy(dwt2)
    assert dwt1 != dwt2

    dwt1.twist = 0
    dwt2.twist = twist
    dwts = {1: dwt1, 2: dwt2}

    for side, dwt in dwts.items():
        for tv in dwt.vertices():
            g.add_node(VS(tv, side))
            for tv2 in dwt.neighbors(tv):
                if tv2.type in ["boundary", "interior"]:
                    if tv.value < tv2.value:
                        g.add_edge(VS(tv, side), VS(tv2, side))
                    if tv.value == tv2.value:
                        g.add_edge(VS(tv, side), VS(tv2, side))
                else:
                    assert tv2.type == "half", "Weird type type = " + repr(tv2.type)
                    half_edges.append(LHE(side, tv, tv2.value))

    # sanity checks 
    unique_half_edges = set((lhe.side, lhe.index) for lhe in half_edges)
    assert len(unique_half_edges) == len(half_edges), "Half edges contain dups."
    del unique_half_edges
    
    while len(half_edges) > 0:
        lhe1 = half_edges.pop()

        side1 = lhe1.side
        side2 = 3 - side1
        tv1 = lhe1.base
        count, i = search(dwts[side1], dwts[side2], lhe1.index)

        # it might be on side1 or side2 based on how many hops.
        match_side = side1
        if count % 2 == 1:
            match_side = side2

        [lhe2] = [l for l in half_edges if l.side == match_side and l.index == i]
        tv2 = lhe2.base
        assert lhe2 in half_edges, "Connects to non-existing half-edge."
        half_edges.remove(lhe2)
        logging.debug(">>> vertex being inserted = " + str((lhe1, lhe2)))
        g.add_edge(VS(tv1, side1), VS(tv2, match_side))

    return g


def search(dwt1, dwt2, i1):
    flag, i2 = dwt2.next(i1)
    if flag == "exit":
        count, result = search(dwt2, dwt1, i2)
        return count+1, result
    if flag.startswith("vertex"):
        return 1, i2
    assert False


def compatible(dwt1, dwt2, twist):
    dwt1.twist = 0
    dwt2.twist = twist
    for i in range(dwt1.circum):
        if dwt1.is_deg2(i) and dwt2.is_deg2(i):
            return False
    return True

def fuse(dwt1, dwt2, twist):
    if not compatible(dwt1, dwt2, twist):
        return None

    g = graph.Graph()

    half_edges = []

    dwt1.twist = 0
    dwt2.twist = twist
    dwts = {1: dwt1, 2: dwt2}

    edges = []
    half_edges = []
    boundary = []

    for side, dwt in dwts.items():
        for j in dwt.pd.interior_vertices:
            v = TV("interior", j)
            for w in dwt.i_neighbors(v):
                if w.type == "interior":
                    if v < w:
                        g.add_edge(VS(v, side), VS(w, side))
                elif w.type == "half":
                    half_edges.append(LHE(side, v, w.value))
                else:
                    assert False

    for i in range(dwt1.circum):
        for side, dwt in dwts.items():
            if dwt.is_deg2(i):
                boundary.append(i)
                half_edges.append(LHE(side, TV("boundary", i), i))

    assert len(set(boundary)) == len(boundary)

    # walk around the fused boundary.
    for i in range(len(boundary)):
        i1 = boundary[i]
        i2 = boundary[(i+1) % len(boundary)]
        g.add_edge(VS(TV("boundary", i1), -1), VS(TV("boundary", i2), -1))


    total_hops = 0
    while len(half_edges) > 0:
        lhe1 = half_edges.pop()

        side1 = lhe1.side
        side2 = 3 - side1
        tv1 = lhe1.base
        count, i = search(dwts[side1], dwts[side2], lhe1.index)

        total_hops += count

        # it might be on side1 or side2 based on how many hops.
        match_side = side1
        if count % 2 == 1:
            match_side = side2
        if len([l for l in half_edges if l.index == i]) != 1:
            print("he", half_edges)
            print([l for l in half_edges if l.index == i])
            quit()

        [lhe2] = [l for l in half_edges if l.index == i]
        tv2 = lhe2.base
        assert lhe2 in half_edges, "Connects to non-existing half-edge."
        half_edges.remove(lhe2)
        logging.debug(">>> vertex being inserted = " + str((lhe1, lhe2)))

        if tv1.type == "boundary":
            side1 = -1
        if tv2.type == "boundary":
            match_side = -1
        g.add_edge(VS(tv1, side1), VS(tv2, match_side))
 
    return g


