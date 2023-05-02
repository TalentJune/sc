import numpy as np
import pandas as pd
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

    #get_excel([Z0,Z1,Z2])


    return [Z0, Z1, Z2]
def get_excel(Z):

    df_Z0 = pd.DataFrame(Z[0])
    df_Z1 = pd.DataFrame(Z[1])
    df_Z2 = pd.DataFrame(Z[2])

    df_Z0.to_excel('Z0', engine='openpyxl', index=False)
    df_Z1.to_excel('Z1', engine='openpyxl',  index=False)
    df_Z2.to_excel('Z2', engine='openpyxl', index=False)