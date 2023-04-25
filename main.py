# %%
import numpy as np
import networkx as nx
import pandas as pd

import gbpower as gbp


if __name__ == '__main__':
    # %%

    #data processing
    branchs = pd.read_excel('data/branchs.xls', header=None)
    branchs = np.array(branchs)
    branchs = branchs[:, 1:]
    gens = pd.read_excel('data/gens.xls', header=None)
    gens = np.array(gens)
    data = [branchs, gens, 39]

    net = gbp.cal.calculate_sc_current(data, 11, '2f')
    # net = gbp.net.create_sysnet(branchs, gens, 39)
    # Y = gbp.net.create_ymatrix(net)
    # Z = gbp.net.get_zmatrix(Y)









