import numpy as np
import matplotlib.pyplot as plot
import sys
import os
import time
import warnings
import random
from matplotlib.colors import ListedColormap

from Anonymizer import CAHD
from KLDivergenceCalculator import Calculator
from Reverse_Cuthill_McKee import RCM

warnings.filterwarnings("ignore")



if __name__ == "__main__":
    p = int(sys.argv[1])
    QID_subset = int(sys.argv[2])
    SD_subset = int(sys.argv[3])
    dataset = sys.argv[4]
    alpha = 3

    # Parse Dataset file in a matrix
    if os.path.exists(dataset):
        with open(dataset) as f:
            count = sum(1 for _ in f)
            A = np.zeros((count, count), dtype=int)
            f.seek(0)
            c = 0
            for x in f:
                items = x.split(" ")
                temp = 0
                for i in items:
                    if i == "\n" or i == "":
                        continue
                    if int(i) > 0:
                        A[c, temp] = 1
                    temp += 1
                c += 1
        f.close()


    else:
        print("Wrong path, Insert a corrected one")
        exit()






    start_time = time.time()
    converter = RCM(A,p)
    converted = converter.calculate_RCM()
    conversion_end_time = time.time() - start_time

    if(QID_subset>len(converter.linkedQID)):
        print(f"Wrong QID_subset value, inserted: {QID_subset} but total QIDs = {len(converter.linkedQID)}")
        exit()
    if (SD_subset > len(converter.linkedSD)):
        print(f"Wrong QID_subset value, inserted: {SD_subset} but total QIDs = {len(converter.linkedSD)}")
        exit()


    band_matrix = converted[0].copy()
    start_time = time.time()
    anonimizer = CAHD(converted[0], p, converted[1], alpha)
    ris = anonimizer.create_groups()
    output_filename = "./AnonymizedDataset.txt"
    anonymization_end_time = time.time() - start_time
    anonimizer.print_results_on_file(output_filename)


    work_time = anonymization_end_time + conversion_end_time
    print("Computed time: ", work_time)


    q = random.sample(converter.linkedQID.keys(), QID_subset)
    mSD = random.sample(converter.linkedSD.keys(), SD_subset)
    s = random.choice(mSD)
    qRCM = list()
    for qid in q:
        qRCM.append(converter.linkedQID.get(qid)[0])

    sRCM = converter.linkedSD[s][0]
    calculator = Calculator(mSD, qRCM, band_matrix, anonimizer.finalDataset)
    # KL Divergence
    print("RCM -> KL_divergence: ", calculator.calculateKL_Divergence())


    fig,axs = plot.subplots(1,2)
    cmap = ListedColormap(['r', 'black'])

    axs[0].imshow(A,cmap)
    axs[0].set_title("Original Matrix")
    axs[1].imshow(converted[0],cmap)
    axs[1].set_title("Band Matrix")


    plot.show()