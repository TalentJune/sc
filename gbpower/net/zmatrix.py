import numpy as np

def get_zmatrix(y_matrix):
    '''
    :param y_matrix:
    [Y0, Y1, Y2]

    :return:
    [Z0, Z1, Z2]
    '''
    Y0 = y_matrix[0]
    Y1 = y_matrix[1]
    Y2 = y_matrix[2]

    Z0 = np.linalg.pinv(Y0)

    I = np.eye(Y1.shape[0])
    Z1 = np.linalg.solve(Y1, I)
    Z2 = np.linalg.solve(Y2, I)

    return [Z0, Z1, Z2]