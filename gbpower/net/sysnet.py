## typing "#%%" will create code cell

import numpy as np
import pandas as pd
import networkx as nx

def create_sysnet(branchs, gens, num_node):

    '''
    :param branchs:
    two dimensions ndarray [[branch's type, from node, to node, x_1, x_0], ...]
    branch's type:
    1: transmission line
    2: YNyn transformer
    3: YNd transformer

    :param gens:
    two dimensions nadarry [[gen's node number, xd'', x_2]]

    :param num_node:
    the number of total nodes

    :return:  a Graph whose nodes are sorted by tiny-1
    '''

    net = nx.Graph()


    # create buses
    for i in range(1, num_node+1):
        net.add_node(i)


    # create branches
    type_branch = branchs[:, 0]
    nodes_branch = branchs[:, 1:3]
    x1_branch = branchs[:, 3]
    x0_branch = branchs[:, 4]

    type_branch = type_branch.astype(int)
    nodes_branch = nodes_branch.astype(int)

    for t, n, x1, x0 in zip(type_branch, nodes_branch, x1_branch, x0_branch):
        net.add_edge(*n)
        net.edges[n]['type'] = t
        net.edges[n]['y1'] = round(1./(1j*x1), 4)
        net.edges[n]['y0'] = round(1./(1j*x0), 4)


    # connect gens to system
    node_gens = gens[:, 0]
    x1_gens = gens[:, 1]
    x2_gens = gens[:, 2]

    node_gens = node_gens.astype(int)

    for n, x1, x2 in zip(node_gens, x1_gens, x2_gens):
        net.nodes[n]['y1'] = round(1./(1j*x1), 4)
        net.nodes[n]['y2'] = round(1./(1j*x2), 4)

    # nodes number optimization --tiny-1
    #net = nx.convert_node_labels_to_integers(net, 1, 'increasing degree')

    return net
