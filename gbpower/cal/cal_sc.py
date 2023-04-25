from gbpower.net import *
def calculate_sc_current(data, f_node, type):
    '''
    :param data:
    data = [branches, gens, num_nodes]

    :param f_node:
    short-circuited node

    :param type:
    short-circuited type
    '1ph'
    '2ph'
    '2f'
    '3ph'

    :return:
    pass
    '''

    #this part of the code could be optimizing to reduce memory usage
    net = create_sysnet(data[0], data[1], data[2])

    Y0, Y1, Y2 = create_ymatrix(net)
    Z0, Z1, Z2 = get_zmatrix([Y0, Y1, Y2])

    I0_f = 0.
    I1_f = 0.
    I2_f = 0.

    f_node = f_node - 1


    if type == '3ph':
        I1_f = 1./Z1[f_node][f_node]
        I0_f = 0.
        I2_f = 0.

    elif type == '1ph':
        I0_f = 1./(Z0[f_node][f_node]+Z1[f_node][f_node]+Z2[f_node][f_node])
        I1_f = I0_f
        I2_f = I0_f

    elif type == '2ph':
        I1_f = 1./(Z1[f_node][f_node]+Z2[f_node][f_node])
        I2_f = -I1_f
        I0_f = 0.

    elif type == '2f':
        I1_f = 1./(Z1[f_node][f_node]+(Z2[f_node][f_node]*Z0[f_node][f_node]/(Z2[f_node][f_node]+Z0[f_node][f_node])))
        I2_f = -I1_f*(Z0[f_node][f_node]/(Z2[f_node][f_node]+Z0[f_node][f_node]))
        I0_f = -I1_f*(Z2[f_node][f_node]/(Z2[f_node][f_node]+Z0[f_node][f_node]))

    # print('I0:{}, I1:{}, I2:{}'.format(I0_f,I1_f,I2_f))
    for node in net.nodes():
        net.nodes[node]['U1'] += -I1_f*Z1[node-1][f_node]
        net.nodes[node]['U2'] += -I2_f*Z2[node-1][f_node]
        net.nodes[node]['U0'] += -I0_f*Z0[node-1][f_node]

    for edge in net.edges:
        ad1_node = edge[0]
        ad2_node = edge[1]
        net.edges[edge]['I0'] += (net.nodes[ad1_node]['U0']-net.nodes[ad2_node]['U0'])/(1./net.edges[edge]['y0'])
        net.edges[edge]['I1'] += (net.nodes[ad1_node]['U1'] - net.nodes[ad2_node]['U1']) / (1. / net.edges[edge]['y1'])
        net.edges[edge]['I2'] += (net.nodes[ad1_node]['U2'] - net.nodes[ad2_node]['U2']) / (1. / net.edges[edge]['y1'])

    return net











