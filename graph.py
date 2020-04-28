"""
graph.py

An ad-hoc implementation of a graph.

NetworkX was inneficient for what I was trying to do, matching many
small graphs agains a small set of target graphs.
"""
import collections
import itertools

class Graph:
    """
    Undirected graph with loops and parallel edges.
    """
    def __init__(self, vec=None):
        self.m = collections.Counter()
        self.edges = []

    def add_node(self, v):
        self.m[v, v]

    def add_edge(self, v, w):
        self.edges.append((v, w))
        self.m[v, w] += 1
        self.m[w, v] += 1

    def vertices(self):
        """
        The vertices in the graph.
        """
        return list(set(v for v,w in self.m))

    def adj_mat(self, vs=None):
        """
        Adjacency matrix as tuple.

        Basis is chosen wrt ordering vs.
        """
        if vs is None:
            vs = self.vertices()
        m = []
        for v in vs:
            row = []
            for w in vs:
                row.append(self.m[v, w])
            m.append(tuple(row))
        return tuple(m)


class GraphBag(dict):
    def __init__(self):
        super().__init__()
        self.size = 0
        self.members = []

    def add(self, g):
        if g in self:
            return
        self.members.append(g)
        vs = g.vertices()
        for vs_perm in itertools.permutations(vs):
            adj_mat = g.adj_mat(vs_perm)
            super().__setitem__(adj_mat, self.size)
        self.size += 1

    def __getitem__(self, g):
        return super().__getitem__(g.adj_mat())

    def __contains__(self, g):
        return super().__contains__(g.adj_mat())

def make_target(filename):
    """
    Given a file with a list graphs each given by a list of edges, produce a
    dictionary which has as keys all the possible adjacency lists which can
    produce a graph represented by the file.
    """
    targets = GraphBag()
    edges = []
    f = open(filename)
    lines = f.readlines()
    f.close()
    lines.append("")
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) == 0:
            if len(edges) == 0:
                continue
            assert len(edges) == 12, str(edges)
            g = Graph()
            for e in edges:
                [v, w] = [int(x) for x in e.split()]
                g.add_edge(v,w)
            targets.add(g)
            edges = []
        else:
            edges.append(line)
    if edges:
        assert False
    return targets




if __name__ == "__main__":

    g1 = Graph()
    g1.add_edge("1", "2")
    g1.add_edge("3", "2")
    g2 = Graph()
    g2.add_edge("9", "2")
    g2.add_edge("3", "2")
    gb = GraphBag()
    gb.add(g1)
    print(g2 in gb)
