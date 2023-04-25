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

    print('I0:{}, I1:{}, I2:{}'.format(I0_f,I1_f,I2_f))






