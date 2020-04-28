"""
quad_disk.py

Library for representing primary quadrangulated disks, as well as
quadrangulated disks with transversals. Depends on `disk_data.json`.
"""

import collections
import json
import os

# vertices have type (interior or boundary) and value
TV = collections.namedtuple("TypeValue", ["type", "value"])

class PrimaryDisk(object):
    """
    One of the nine primitive disks.
    """
    def __init__(self, s):
        self.json = json.loads(s)
        d = self.json
        self.name = d["Filename"]
        self.sigma = d["EnterExitTrans"]
        self.interior_vertices = d["InteriorVertices"]
        self.interior_vertices.sort()
        self.interior_edges = d["InteriorEdges"]
        self.inwards = d["BoundaryInteriorEdge"]
        self.size = len(self.sigma)

        # boundary vertices of degree 2
        self.deg2 = [i for (i, x) in enumerate(self.inwards) if x == ""]

    def __repr__(self):
        return "PrimaryDisk(%s, %s, %s, %s)" % (self.name, self.sigma,
                (self.interior_vertices, self.interior_edges), self.inwards)


class DWT(object):
    """
    Disk with transversals. The number of transversal counts should
    be half the size of the boundary of the primary disk.
    """
    def __init__(self, primary_disk, counts):
        self.pd = primary_disk
        assert 2*len(counts) == self.pd.size, "%s %s" % (counts, primary_disk)

        counts = list(counts)
        tc = []
        for i in range(self.pd.size):
            if self.pd.sigma[i] > i:
                tc.append(counts.pop())
            else:
                tc.append(tc[self.pd.sigma[i]])

        self.tc = tc
        self.twist = 0

        # build map between index and bpc
        self.to_index = {}
        self.to_bpc = {}
        i = 0
        for e in range(primary_disk.size):
            for j in range(tc[e]+1):
                self.to_index[e, j] = i
                self.to_bpc[i] = e, j
                i = i + 1

        self.circum = i

    def bcp(self, i):
        """
        Boundary code pair.
        """
        i = (i - self.twist) % self.circum
        if i not in self.to_bpc:
            print(self, i)
            quit()
        return self.to_bpc[i]

    def boundary_index(self, e, j):
        """
        BCP to position on boundary.
        """
        #str(">>>", self, e, j)
        if (e, j) not in self.to_index:
            print(self)
            print(self.to_index)
            print("e, j", e, j)
        i = self.to_index[e, j]
        i = (i + self.twist) % self.circum
        assert self.bcp(i) == (e, j)
        return i


    def vertices(self):
        for v in self.pd.interior_vertices:
            yield TV("interior", v)
        for e in self.pd.deg2:
            yield TV("boundary", self.boundary_index(e, 0))


    def next(self, i):
        """
        When you enter the dwt on the boundary vertex i, do you exit out the
        other side, or do you hit a vertex?
        """

        e, j = self.bcp(i)
        # you hit a vertex originally on the primary disk.
        if j == 0:
            if self.pd.inwards[e] == "":
                return "vertex2", i
            return "vertex", i
        e_ = self.pd.sigma[e]
        j_ = self.tc[e] + 1 - j
        i_ = self.boundary_index(e_, j_)
        return "exit", i_

    def __str__(self):
        return "DWT(primary_disk: %s, transveral_counts: %s, twist: %s)" % (self.pd, self.tc, self.twist)

    def neighbors(self, tv):
        if tv.type == "interior":
            for w in self.i_neighbors(tv):
                yield w
        else:
            assert tv.type == "boundary"
            for w in self.b_neighbors(tv):
                yield w

    def i_neighbors(self, tv):
        """
        Neighbors of a point on the interior.
        """
        t, v = tv
        assert v in self.pd.interior_vertices
        for edge in self.pd.interior_edges:
            if v in edge:
                [w] = [x for x in edge if x != v]
                yield TV("interior", w)
        for w in range(self.pd.size):
            if self.pd.inwards[w] == v:
                yield TV("half", self.boundary_index(w, 0))

    def b_neighbors(self, tv):
        """
        Neighbors of a point on the boundary.
        """
        t, v = tv
        assert t == "boundary"
        assert v in range(self.circum), "Vertex not on boundary."
        e, j = self.bcp(v)
        assert j == 0
        assert e in self.pd.deg2, "vertex not cubic"
        yield TV("half", v)
        if len(self.pd.deg2) == 1:
            yield tv
        else:
            j = self.pd.deg2.index(e)
            i1 = self.pd.deg2[(j - 1) % len(self.pd.deg2)]
            i2 = self.pd.deg2[(j + 1) % len(self.pd.deg2)]
            yield TV("boundary", self.boundary_index(i1, 0))
            yield TV("boundary", self.boundary_index(i2, 0))

    def is_deg2(self, i):
        flag, _ = self.next(i)
        return flag == "vertex2"


def load_primary_disks():
    filename = "disk_data.json"
    primary_disks = [PrimaryDisk(line) for line in open(filename)]
    primary_disks.sort(key=lambda pd: pd.name)
    return primary_disks
