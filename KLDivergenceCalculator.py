from itertools import product
import numpy as np



class Calculator:
    def  __init__(self,SD_subset,QID_subset,matrix,finalDataset):
        self.SD_subset = SD_subset
        self.QID_subset = QID_subset
        self.matrix = matrix
        self.finalDataset = finalDataset
        self.total_sd_in_table = 0
        self.KL_Divergence = 0
        self.Cells = list()


    def calculateAct(self, cell, sd):
        counter = 0
        for j in range(len(self.matrix)):
            t = self.matrix[j, :]
            # Considering every row in the matrix
            diverso = False
            for k in range(len(self.QID_subset)):
                if t[int(self.QID_subset[k])] != self.Cells[cell][k]:
                    #Verify if each QID is equal to cell
                    diverso = True

            if not diverso and t[sd] == 1:
                #If all QID are equals and also SD is present increment counter
                counter += 1

        return counter / self.total_sd_in_table


    def calculateEst(self, cell, sd):
        data_reconstruction  = 0
        for j in range(len(self.finalDataset)):
            g = self.finalDataset[j]
            # Considering all groups
            b = 0
            # b represents the transactions number inside group equal to cell
            a = 0
            # a represents the transactions number inside group with sd different from 0
            for t in g:
                diverso = False
                for k in range(len(self.QID_subset)):
                    if t[int(self.QID_subset[k])] != self.Cells[cell][k]:
                        # Verify if each QID is equal to cell
                        diverso = True

                if not diverso:
                    b += 1
                    
                if t[sd] == 1:
                        a += 1

            data_reconstruction += a * b / len(g)

        return data_reconstruction / self.total_sd_in_table


    def calculateKL_Divergence(self):

        occurences = self.matrix.sum(axis=0)
        self.Cells = list(product([0, 1], repeat=len(self.QID_subset)))
        # Cells contains all possible combination of QID, considering that each one can assume only 0 and 1 values.

        for sd in self.SD_subset:
        # For each sd in subset, calculate ACT and EST

            self.total_sd_in_table = occurences[sd]

            for cell in range(len(self.Cells)):
                Act = self.calculateAct(cell, sd)
                Est = self.calculateEst(cell, sd)
                if Est != 0 and Act != 0:
                    self.KL_Divergence += Act * np.log2(Act / Est)

        return self.KL_Divergence
