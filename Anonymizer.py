import numpy as np

def getAllKeys(item, dictionary):
    listOfItems = dictionary.items()
    allKey = list()
    for i in listOfItems:
        if item in i[1]:
            allKey.append(i[0])
    return allKey

def sort(list1, list2):
    # reorders rows according to their position in the band matrix,
    # consequently the closest rows will have by construction the greatest number of QIDs in common
    newlist = []
    a1 = len(list1)
    a2 = len(list2)

    for i in range(max(a1, a2)):
        if i < a1:
            newlist.append(list1[i])
        if i < a2:
            newlist.append(list2[i])

    return newlist



def getKeysByValue(dictOfElements, valueToFind):
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if np.array_equal(valueToFind, item[1]):
            return item[0]

class CAHD:
    def __init__(self,band_matrix, p, SD_correspondence, alpha):
        self.band_matrix = band_matrix
        self.p = p
        self.SD_correspondence = SD_correspondence
        self.alpha = alpha
        self.allGroups = list()
        self.allSDinG = list()
        self.T = band_matrix.copy()
        self.finalDataset = list()

    def getcandidates(self, transaction):
        # this function returns candidate rows to join the group by checking the alpha * p preceding and following
        # non-conflicting transactions
        down = list()
        up = list()
        for i in range(transaction + 1, min(transaction + self.alpha * self.p, self.T.shape[0])):
            to_append = True
            if self.T[i, 0] == -1:
                # row already part of a group
                continue
            for sensitive_row in self.SD_correspondence.values():
                if i in sensitive_row:
                    #conflicting row
                    to_append = False
                    break
            if to_append:
                up.append(i)

        for i in range(max(transaction - self.alpha * self.p, 0), transaction):
            to_append = True
            if self.T[i, 0] == -1:
                continue
            for sensitive_row in self.SD_correspondence.values():
                if i in sensitive_row:
                    to_append = False
                    break
            if to_append:
                down.append(i)
        return sort(down, up)


    def create_groups(self):
        for i in self.SD_correspondence.keys():  # (while), choose a SD in band matrix
            for t in self.SD_correspondence[i]:  # select t with the correspondent SD
                if self.T[t, 0] == -1:  # check that t has not already been taken
                    continue
                local = self.SD_correspondence.copy()
                # Create a local copy of the value so that I can manipulate it without changing the global state

                CL = []
                # Candidate list, first step to joining the group

                P = list()
                # We initialize P so that at the beginning it contains all rows containing that SD
                for g in self.SD_correspondence.values():
                    if t in g:
                        P.append(getKeysByValue(self.SD_correspondence, g))

                remaining = len(self.T) - self.p * len(self.allGroups)
                # Counts the lines that are not part of the group so that this can be validated
                # guaranteeing satisfactory anonymity standards

                CL = self.getcandidates(t)
                # Selecting rows with the highest QID in common, the reconstruction error will be minimized
                if len(CL) == 0:
                    continue
                # creation of the groups
                G = CL[: self.p - 1]

                G.append(t) #Creo primo gruppo
                remaining -= len(G)
                condition = True
                for k in local.keys(): 
                    # scroll through all the SDs
                    if len(local[k]) * self.p > remaining: 
                        # Verify that the eventual creation of the group does not prevent to reach anonymity standards (probability equal to 1 / p)
                        # If there are not enough rows left outside the group, the group will not be validated
                        condition = False
                        remaining += len(G)
                        break
                if condition:
                    # if I can guarantee the privacy degree = p valid the group and remove the selected lines
                    for z in range(len(G)):
                        for k in local.keys():
                            index = np.argwhere(local[k] == G[z])
                            local[k] = np.delete(local[k], index)
                        self.T[G[z], 0] = -1
                    self.SD_correspondence = local.copy()
                    self.allGroups.append(G)
                    self.allSDinG.append(P)


        # Finally, create the last group by inserting all the lines that are not already part of one
        G = []
        for b in range(len(self.T)):
            if self.T[b, 0] != -1:
                G.append(b)

        if G:
            P = []
            for k in G:
                allKeyEle = getAllKeys(k, self.SD_correspondence)
                P += allKeyEle

            self.allGroups.append(G)
            self.allSDinG.append(P)

        return self.allGroups, self.allSDinG

    def print_results_on_file(self,filename):

        f = open(filename, "w")

        finalDataset = list()
        g = list()

        count = 0
        for i in self.allGroups:
            g = []
            sd = set(self.allSDinG[count])
            if len(sd) > 0:
                f.write(f"Sensitive Data in this group: {sd}\n")
            else:
                f.write("No more sensitive data in last group\n")
            count += 1
            for item in i:
                t = []
                for j in range(len(self.band_matrix)):
                    t.append(self.band_matrix[item, j])
                    if j in sd:
                        f.write("X ")
                    else:
                        f.write(f"{self.band_matrix[item, j]} ")
                g.append(t)
                f.write("\n")
            finalDataset.append(g)
            f.write("\n")
        self.finalDataset = finalDataset
        f.close()