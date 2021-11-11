import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee


class RCM:
    def __init__(self,M,p):
        self.p = p
        temp = M.sum(axis=0)
        SD = np.argwhere((temp < p) & (temp > 0))
        # Every item (column) with less occurences than p is considered SD.
        if len(SD) == 0:
            print("Can't find SD with this value of p, try with smaller p.")
            exit()

        self.SD = SD[:, 0]

        self.linkedSD = dict()
        self.linkedQID = dict()
        #Those dictionaries keeps track of SD and QID position in new band matrix
        for sds in SD:
            self.linkedSD[sds[0]] = []

        for qids in range(len(M)):
            if qids not in SD:
                self.linkedQID[qids] = []

        self.A_sparse = csr_matrix(M)
        # Convert matrix into Compressed Sparse Row Matrix first step for band matrix

        self.gamma = reverse_cuthill_mckee(self.A_sparse, symmetric_mode=False)
        # Returns the permutation array that orders a sparse CSR or CSC matrix in Reverse-Cuthill McKee ordering.
        self.band_matrix = []



    def calculate_RCM(self):
    # create sparse matrix

        for i in range(len(self.gamma)):
            self.A_sparse[:, i] = self.A_sparse[self.gamma, i]
        for i in range(len(self.gamma)):
            self.A_sparse[i, :] = self.A_sparse[i, self.gamma]
        self.band_matrix = self.A_sparse.toarray()


        SD_correspondence = dict()
        for i in self.linkedSD.keys():
            t = np.asscalar(np.where(self.gamma == i)[0])
            self.linkedSD[i].append(t)
            SD_correspondence[t] = np.argwhere(self.band_matrix[:, t] == 1)[:, 0]

        for i in self.linkedQID.keys():
            t = np.asscalar(np.where(self.gamma == i)[0])
            self.linkedQID[i].append(t)

        return self.band_matrix, SD_correspondence
        # Returns the band matrix -> self.band_matrix
        # and SD_correspondence -> dictionary with value = column index where SD is in the band matrix,
        # key = row containing SD always of the band matrix

