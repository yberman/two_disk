#!/usr/bin/env python3

import connect
import composition
import graph
import quad_disk
import sys


primary_disks = quad_disk.load_primary_disks()
def DisksWithTransversals(size):
    """List all disks with transversals of a specific size.

    Requires that the disk has one vertex on the boundary of degree 2. This
    requirement is generalized by using both connect.fuse and connect.connect.
    """
    for pd in primary_disks:
        if pd.size > size:
            continue
        for counts in composition.non_negative((size - pd.size) // 2, pd.size // 2):
            yield quad_disk.DWT(pd, counts)



known_graphs = graph.GraphBag()
bandits = graph.make_target("outlaws.txt")
i = 0
for disk_size in list(range(4, 18, 2)):
    print("D disk_size =", disk_size, "cases examined =", i)
    for dwt1 in DisksWithTransversals(disk_size):
        for dwt2 in DisksWithTransversals(disk_size):
            for rotation in range(disk_size):
                for op in [connect.connect, connect.fuse]:
                    g = op(dwt1, dwt2, rotation)
                    i += 1
                    if g is None:
                        continue
                    # if the graph is new, print everything we would want to
                    # print everything we would want to know about the graph.
                    if g not in known_graphs:
                        known_graphs.add(g)
                        print("G", known_graphs.size, g.adj_mat(),
                              dwt1, dwt2, rotation,
                              "connect" if op == connect.connect else "fuse")
                        # if it is a bandit, quit in excitement
                        if g in bandits:
                            print("!")
                            quit()
                    if len(known_graphs.members) == 137:
                        print("cases examined", i)
                        quit()
