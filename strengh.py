from math import sqrt
from copy import deepcopy
from copy import copy
import subprocess
import random

def compute_strengh(G):
    N = len(G)
    degrees = []
    strengh = 0
    for i in range(N):
        for j in range(len(G[i])):
            strengh += edge_strengh(G, i, G[i][j])
    return strengh # We do the computation twice for each edge
                   # no need to multiply by 2

def compute_path_strengh(nb_edges):
    return nb_edges - 2 + 4*sqrt(2)/3

def edge_strengh(G, i, j):
    return sqrt(len(G[i])*len(G[j]))/(len(G[i]) + len(G[j]))

def compute_tree_bound(nb_edges, nb_odd):
    return nb_edges - nb_odd*(1-2*sqrt(2)/3)

def print_graph(G, filename):
    filegraph = open(filename + ".gv", "w")
    filegraph.write("graph G {\n")
    filegraph.write(" graph [rankdir = LR]\n")
    Gbis = deepcopy(G)
    for i in range(len(Gbis)):
        for j in range(len(Gbis[i])):
            filegraph.write(str(i) + " -- " + str(Gbis[i][j]) + "\n")
            Gbis[Gbis[i][j]].remove(i) #Remove the doubled edge so that it appears only once
    filegraph.write("}")
    filegraph.close()
    subprocess.call("dot -Tpng " + filename + ".gv -o" + filename + ".png", shell = True)

def random_split(G):
    N = len(G)
    rnd_vertex = random.randint(0, N-1)
    G.append([])
    G[rnd_vertex].append(N)
    G[N].append(rnd_vertex)

def deterministic_copy_and_split(G, v):
    if v >= len(G): print("ERROR: CAN NOT SPLIT THIS VERTEX")
    Gbis = []
    for i in range(len(G)):
        Gbis.append([])
        for j in G[i]: Gbis[i].append(j)
    Gbis.append([v])
    Gbis[v].append(len(G))
    return Gbis

def compute_nb_edges(G):
    nb_edges = 0
    for i in range(len(G)):
        nb_edges += len(G[i])
    if (nb_edges % 2 != 0): print("ERROR: BAD NUMBER OF EDGES")
    return nb_edges/2

def compute_nb_odd(G):
    nb_odd = 0
    for i in range(len(G)):
        if (len(G[i]) % 2 != 0):
            nb_odd += 1
    if (nb_odd % 2 != 0): print("ERROR: BAD NUMBER OF ODD VERTICES")
    return nb_odd

# Random tree
def generate_random_tree(n):
    G = [[]]
    for i in range(n-1):
        random_split(G)
    return G

# For testing if adding an edge to a connected graph
# on n vertices necessarily raise the strength of the graph
def possible_edges_to_add(G):
    N = len(G)
    possible_edges = []
    for i in range(N):
        for j in range(i+1, N):
            if not (j in G[i]):
                possible_edges.append([i,j])
    return possible_edges

def add_edge(G, edge):
    Gbis = []
    for i in len(G):
        Gbis.append([])
        for j in G[i]: Gbis[i].append(j)
    i = edge[0]
    j = edge[1]
    if j in G[i]: print("ERROR ON ADDING EDGE: EDGE ALREADY EXISTING")
    Gbis[i].append(j)
    Gbis[j].append(i)
    return Gbis

# Methods to add and remove edges.
def add_edge_without_copy(G,edge):
    i = edge[0]
    j = edge[1]
    if j in G[i]: print("ERROR ON ADDING EDGE: EDGE ALREADY EXISTING")
    G[i].append(j)
    G[j].append(i)

def remove_edge_without_copy(G, edge):
    i = edge[0]
    j = edge[1]
    if not (j in G[i]): print("ERROR ON REMOVING EDGE: EDGE NOT EXISTING")
    G[i].remove(j)
    G[j].remove(i)

def add_all_edges(G, edges):
    Gbis = []
    for i in len(G):
        Gbis.append([])
        for j in G[i]: Gbis[i].append(j)
    i = edge[0]
    j = edge[1]
    if j in G[i]: print("ERROR ON ADDING EDGE: EDGE ALREADY EXISTING")
    Gbis[i].append(j)
    Gbis[j].append(i)
    return Gbis


# Supposed tree bound (invalid for n >= 10)
def valid_tree_bound(G):
    E = compute_nb_edges(G)
    if (E != len(G)-1) : print("ERROR: Invalid number of edges in a tree")
    Tg = compute_nb_odd(G)
    return compute_strengh(G) <= compute_tree_bound(E, Tg)

nb_tree_tested = 0
# Generate all trees of length < 10 and test the bound
def try_all_trees(G):
    global nb_tree_tested
    if len(G) >= 12: return
    if len(G) > 2:
        nb_tree_tested += 1
        if not(valid_tree_bound(G)):
            print_graph(G, "cex_bound_small_tree")
            print("Counter example found")
    for v in range(len(G)):
        Gbis = deterministic_copy_and_split(G, v)
        try_all_trees(Gbis)

# Generate G(n,1/2)
def generate_random_graph(n):
    G = []
    for i in range(n):
        G.append([])
    for i in range(n):
        for j in range(i+1, n):
            if random.random() <= 1/2:
                G[i].append(j)
                G[j].append(i)
    return G

# Build a star graph on n vertices
def build_star(n):
    G = []
    G.append([i for i in range(1,n)])
    for i in range(n-1): G.append([0])
    return G

# Uninon of two star on 2n vertices for counter exemple strength raise
def union_star(n):
    G = build_star(n)
    G.append([i for i in range(n+1, 2*n)])
    for i in range(n-1): G.append([n])
    G[n-1].append(2*n-1)
    G[2*n-1].append(n-1)
    return G


if __name__ == '__main__':


    try_all_trees([[]])
    print(str(nb_tree_tested))

    # Test c-ex lucas.

    # prevstrengh = 0
    # curstrengh = 0
    # star = []
    # star = union_star(10)
    # prevstrengh = compute_strengh(star)
    # print_graph(star, "teststar")
    # print(str(prevstrengh))
    # star = add_edge(star, [0, 10])
    # curstrengh = compute_strengh(star)
    # print_graph(star, "teststabis")
    # print(str(curstrengh))
    # for n in range(2, 10000):
    #     star = union_star(n)
    #     prevstrengh = compute_strengh(star)
    #     star = add_edge(star, [0, n])
    #     curstrengh = compute_strengh(star)
    #     print(str(curstrengh-prevstrengh))
    #     if (curstrengh < prevstrengh): print("Counter exemple found for n = " + str(n))

    # Counter example for the report

    # G = [[1,2,3], [0,8], [0,6], [0,4,5], [3,7], [3,9], [2], [4], [1], [5]]
    # print_graph(G, "lol")
    # print(str(compute_strengh(G)))
    # print(str(compute_tree_bound(9,6)))


    # Test: generate random tree and add edges to see if strength raise

    # for i in range (10000):
    #     for n in range(3,50):
    #         T = generate_random_tree(n)
    #         edges = possible_edges_to_add(T)
    #         S = compute_strengh(T)
    #         for e in edges:
    #             add_edge_without_copy(T,e)
    #             Sg = compute_strengh(T)
    #             if (Sg < S):
    #                 print("FALSE: Strengh is lowering by adding edge " + str(e))
    #                 print_graph(T, "tree_add_edge")
    #                 print_graph(G, "tree_add_edge_2")
    #             remove_edge_without_copy(T,e)

    # for i in range(1000):
    #     T = generate_random_tree(20)
    #     edges = possible_edges_to_add(T)
    #     S = compute_strengh(T)
    #     G = T
    #     Sprev = S
    #     for e in edges:
    #         G = add_edge(G,e)
    #         Sg = compute_strengh(G)
    #         if (Sg < Sprev):
    #             print("FALSE: Strengh is lowering by adding edge " + str(e))
    #             break
    #         Sprev = Sg
    #     if (compute_nb_edges(G) != (20*19)/2): print("BAD FINAL NUMBER OF EDGES")

    # G = [[1,2,3], [0,2,3], [0,1,3], [0,1,2]] #K4
    # G = [[1], [0,2], [1,3], [2]] #P4
    # print(str(compute_path_strengh(4)))
    # G = [[1], [0,2], [1,3,5,8], [2], [5], [2, 4, 6, 9], [5,7], [6], [2], [5]] # 3 crossing paths of length 4
    # print(str(compute_strengh(G)))
    # print(str(compute_tree_bound(9,3)))

    # Random tree for bound comparison

    # G = generate_random_tree(9)
    # number_gen = 1
    # while(valid_tree_bound(G)):
    #    G = generate_random_tree(9)
    #    print("Number generated tree " + str(number_gen) + "\n")
    #    number_gen += 1
    # print_graph(G, "counter_exemple_bound")
    # print(str(compute_strengh(G)))
    # print(str(compute_tree_bound(compute_nb_edges(G), compute_nb_odd(G))))
    # Bound seems valid for n <= 9 : 40889954 tree generated, no counter exampe found

    # Random graph on G(n,1/2)

    # G = generate_random_graph(10)
    # strengh = compute_strengh(G)
    # for i in range(10000000):
    #    G = generate_random_graph(10)
    #    strengh += compute_strengh(G)
    # strengh = strengh/10000000
    # print(str(strengh))
    # Mean strengh 21.97188288669261 for 10 vertices

    #gStrengh = 0
    #for n in range(5,50):
    #    strengh = 0
    #    for i in range(100000):
    #        G = generate_random_graph(n)
    #        E = compute_nb_edges(G)
    #        if E != 0: strengh += compute_strengh(G)/compute_nb_edges(G)
    #    strengh = strengh/100000
    #    print(str(strengh))
    #    gStrengh += strengh
    #print(str(gStrengh))
