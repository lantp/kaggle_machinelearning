#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random as rand

def mER(n, p=0.0, r=True):
    """
    Modified algorithm ER
        Input: Number of nodes n; Probability p; Random model boolean.
        Output: A random digraph g = (V,E) where g ∈ G(n,p).
    """
    if r is True:
        p = rand()

    try:
        n = int(n)
        p = float(p)
    except ValueError:
        n = 0
        p = 0.0
    except TypeError:
        n = 0
        p = 0.0

    if n <= 0:
        raise ValueError("nodes should be a positive integer")

    # nodes = set([i for i in range(n)])
    # graph = {node: set([]) for node in nodes}
    nodes = set()
    for i in range(n):
        nodes.add(i)
    graph = {}
    for i in nodes:
        graph[i] = set()

    for i in nodes:
        for j in nodes:
            if i != j:
                a = rand()
                if a < p:
                    graph[i].add(j)
    return graph


if __name__ == '__main__':
    from moduleOne import in_degree_distribution as idd
    import matplotlib.pyplot as plt

    def buildDis(p):
        x = []
        y = []
        distribution = idd(mER(2000, p, False))
        print("in-degree distribution is : ", distribution)
        if 0 in distribution.keys():
            distribution.pop(0)
        for k, v in distribution.items():
            x.append(k)
            y.append(v)
        return x, y

    x0, y0 = buildDis(0.49)
    x1, y1 = buildDis(0.50)
    x2, y2 = buildDis(0.51)
    x3, y3 = buildDis(0.505)

    plt.title("random distribution with 2000 nodes")
    plt.xlabel("cited, based on 10")
    plt.ylabel("normalized distribution, based on 10")
    plt.text(1, 1, "probability range (0.49,0.51)")
    plt.loglog(x0, y0, "ro", color="yellow")
    plt.loglog(x1, y1, "ro", color="red")
    plt.loglog(x2, y2, "ro", color="blue")
    plt.loglog(x3, y3, "ro", color="green")
    plt.show()
