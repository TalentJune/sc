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
    '''
    net
    
    nodes[
    'y1': reciprocal of gens' xd''
    'y2': reciprocal of gens' x2
    'gen' whether to connect to gens
    'u0'
    'u1'
    'u2'
    ]
    
    branchs[
    'type': type of branch
    'y1': reciprocal of transmisson line or transformer x1
    'y0': reciprocal of transmisson line or transformer x0
    'i0'
    'i1'
    'i2'
    ]
    '''


    # create buses
    for i in range(1, num_node+1):
        net.add_node(i)
        net.nodes[i]['y1'] = 0
        net.nodes[i]['y2'] = 0
        net.nodes[i]['gen'] = False


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
        net.edges[n]['y1'] = -1j*round(1./(x1), 4)
        net.edges[n]['y0'] = -1j*round(1./(x0), 4)


    # connect gens to system
    # the y1, y2 of nodes are symbols of gens' y1, y2
    node_gens = gens[:, 0]
    x1_gens = gens[:, 1]
    x2_gens = gens[:, 2]

    node_gens = node_gens.astype(int)

    for n, x1, x2 in zip(node_gens, x1_gens, x2_gens):
        net.nodes[n]['y1'] = -1j*round(1./(x1), 4)
        net.nodes[n]['y2'] = -1j*round(1./(x2), 4)
        net.nodes[n]['gen'] = True

    net = init_net(net)

    # nodes number optimization --tiny-1
    #net = nx.convert_node_labels_to_integers(net, 1, 'increasing degree')

    return net


# initialize U && I
def init_net(net):
    for i in net.nodes():
        net.nodes[i]['u0'] = 1
        net.nodes[i]['u1'] = 1
        net.nodes[i]['u2'] = 1
    for i in net.edges():
        net.edges[i]['i0'] = 0
        net.edges[i]['i1'] = 0
        net.edges[i]['i2'] = 0

    return net
