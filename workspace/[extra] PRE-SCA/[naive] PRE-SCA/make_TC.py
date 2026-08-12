"""재현 가능한 PRE-SCA 입력 벡터 CSV를 생성한다.

난수 시드를 1로 고정해 매 실행에서 같은 입력을 만든다. 기존 파일은 덮어쓰며, 경로·권한
오류는 호출자에게 전파된다.
"""

import csv
import os
import random
from config import *

def make_TC():
    """재현 가능한 가상 입력 한 행을 `log_vir_in_file`에 저장한다.

    전체 길이는 `BUFFER_BLOCK * BUFFER_NUM`이고 앞 64바이트만 seed 1의 난수로 채우며
    나머지는 0이다. 첫 열에는 주입 순서 0을 쓴다. 기존 파일을 덮어쓰고 경로·권한 오류는
    호출자에게 전파되며 반환값은 없다.
    """
    random.seed(1)

    test_VirIN = [0x0 for _ in range(BUFFER_BLOCK * BUFFER_NUM)]
    ctr = 0
    test_VirIN[0:64] = [ random.randint(0, 255) for _ in range(64) ]

    with open(log_vir_in_file, 'w', newline='') as file:
        wr = csv.writer(file)
        wr.writerow([ctr] + test_VirIN)

if __name__ == '__main__':
    make_TC()
