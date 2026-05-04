import csv
import os
import random
from config import *

def make_TC():
    random.seed(1)

    test_VirIN = [0x0 for _ in range(BUFFER_BLOCK * BUFFER_NUM)]
    ctr = 0
    test_VirIN[0:64] = [ random.randint(0, 255) for _ in range(64) ]

    with open(log_vir_in_file, 'w', newline='') as file:
        wr = csv.writer(file)
        wr.writerow([ctr] + test_VirIN)

if __name__ == '__main__':
    make_TC()