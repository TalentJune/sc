import scipy
import numpy as np
import networkx as nx

def create_ymatrix(net):

    Y0 = create_ymatrix_zero(net)
    Y1 = create_ymatrix_postive(net)
    Y2 = create_ymatrix_nagative(net)

    return [Y0, Y1, Y2]

def create_ymatrix_postive(net):
    '''
    :param net:
    input a sysnet

    :return:
    return the postive sequnence matrix of the system
    '''

    # create an empty matrix
    num_nodes = net.number_of_nodes()
    y_matrix = np.zeros((num_nodes,num_nodes),dtype='cfloat')

    # mutual admittance
    for edge_tuple in net.edges:
        col = edge_tuple[0]
        row = edge_tuple[1]
        y_matrix[col-1][row-1] = -1*net[col][row]['y1']
        y_matrix[row-1][col-1] = -1*net[col][row]['y1']

    # self admittance
    sum_row = y_matrix.sum(axis=0)
    for node in net.nodes:
        sumi_row = sum_row[node-1]
        y_matrix[node-1][node-1] = net.nodes[node]['y1']-sumi_row

    return y_matrix

def create_ymatrix_nagative(net):
    '''
    :param net:
    input a sysnet

    :return:
    return the nagative sequnence matrix of the system
    '''

    # create an empty matrix
    num_nodes = net.number_of_nodes()
    y_matrix = np.zeros((num_nodes,num_nodes),dtype='cfloat')

    # mutual admittance
    for edge_tuple in net.edges:
        col = edge_tuple[0]
        row = edge_tuple[1]
        y_matrix[col-1][row-1] = -1*net[col][row]['y1']
        y_matrix[row-1][col-1] = -1*net[col][row]['y1']

    # self admittance
    sum_row = y_matrix.sum(axis=0)
    for node in net.nodes:
        sumi_row = sum_row[node-1]
        y_matrix[node-1][node-1] = net.nodes[node]['y2']-sumi_row

    return y_matrix


def create_ymatrix_zero(net):
    '''
     :param net:
     input a sysnet

     :return:
     return the zero sequnence matrix of the system
     '''

    # create an empty matrix
    num_nodes = net.number_of_nodes()
    y_matrix = np.zeros((num_nodes, num_nodes), dtype='cfloat')

    # mutual admittance
    for edge_tuple in net.edges:
        col = edge_tuple[0]
        row = edge_tuple[1]
        # YNyn and transmisson line are the same cases
        if net.edges[edge_tuple]['type'] != 3:
            y_matrix[col - 1][row - 1] = -1 * net[col][row]['y0']
            y_matrix[row - 1][col - 1] = -1 * net[col][row]['y0']
        else:
            y_matrix[col - 1][row - 1] = 0
            y_matrix[row - 1][col - 1] = 0
            if net.nodes[col]['gen'] == False:
                y_matrix[col-1][col-1] += net[col][row]['y0']

    # self admittance
    sum_row = y_matrix.sum(axis=0)
    for node in net.nodes:
        sumi_row = sum_row[node - 1]
        y_matrix[node - 1][node - 1] = - sumi_row

    return y_matrix


