"""반복 에뮬레이션의 CSV·디스어셈블리 산출물을 바이너리 단위로 비교한다.

최초 로그 디렉터리를 기준으로 나머지 디렉터리의 파일을 비교하며 파일을 변경하지
않는다. 접미사와 일치하는 파일이 없거나 둘 이상이면 비교 실패로 보고한다.
"""

import os
import glob

def get_file_path_by_suffix(folder, suffix):
    """폴더에서 접미사와 일치하는 파일이 하나일 때만 그 경로를 반환한다."""
    # 폴더 내의 모든 파일을 검색하여 suffix로 끝나는지 확인
    search_pattern = os.path.join(folder, "*" + suffix)
    found_files = glob.glob(search_pattern)
    
    if len(found_files) == 1:
        return found_files[0]
    else:
        print(f"[오류] '{folder}' 안에 '{suffix}' 파일이 없거나 여러 개입니다.")
        return None

def compare_files_binary(file_a, file_b):
    """두 파일의 바이트열을 비교하여 같으면 `True`를 반환한다.

    파일 I/O가 실패하면 오류를 출력하고 `False`를 반환하며 파일은 변경하지 않는다.
    """
    try:
        with open(file_a, 'rb') as fa:
            data_a = fa.read()  # 파일 A 전체 읽기
        
        with open(file_b, 'rb') as fb:
            data_b = fb.read()  # 파일 B 전체 읽기
            
        return data_a == data_b
        
    except Exception as e:
        print(f"[오류] 파일 읽기 실패: {e}")
        return False

def main():
    """반복 실행 로그와 디스어셈블을 기준 실행에 바이트 단위로 대조한다.

    `./log/*tiny-AES_rand` 중 첫 폴더를 기준으로 세 CSV를 비교하고, 마지막에
    `disassembly_v3.1.txt`와 `disassembly.txt`를 비교한다. 파일을 변경하지 않고 결과를
    stdout에 출력한다. 폴더가 둘 미만이면 안내 후 반환하며 종료 코드를 별도로 설정하지 않는다.
    """
    base_pattern = "./log/*tiny-AES_rand"
    
    # 모든 폴더 목록 가져오기 (시간 순 정렬)
    folders = sorted(glob.glob(base_pattern))
    
    if len(folders) < 2:
        print("비교할 폴더가 2개 미만입니다.")
        return

    # 2. 비교할 기준이 되는 첫 번째 폴더 (disassembly)
    ref_folder = folders[0]
    print(f"기준 폴더: {ref_folder}\n" + "-"*60)

    # 3. 비교할 파일 종류 (파일명의 뒷부분)
    target_suffixes = ["LogReg.csv", "LogVirIN.csv", "LogVirOUT.csv"]
    
    all_matched = True

    # 4. 나머지 모든 폴더를 기준 폴더와 비교
    for target_folder in folders[1:]:
        print(f"비교 대상: {target_folder}")
        
        for suffix in target_suffixes:
            # 기준 파일과 대상 파일 찾기
            ref_file = get_file_path_by_suffix(ref_folder, suffix)
            tgt_file = get_file_path_by_suffix(target_folder, suffix)
            
            if ref_file and tgt_file:
                # 바이너리 비교 수행
                is_same = compare_files_binary(ref_file, tgt_file)
                
                if is_same:
                    print(f"  [일치] {suffix}")
                else:
                    print(f"  [불일치!] {suffix} 파일이 서로 다릅니다.")
                    all_matched = False
            else:
                all_matched = False
        print("-" * 30)

    print("=" * 60)

    is_same = compare_files_binary("./disassembly_v3.1.txt", "./disassembly.txt")

    if is_same:
        print(f"  [일치] disassembly.txt")
    else:
        print(f"  [불일치!] disassembly.txt 파일이 서로 다릅니다.")
        all_matched = False

    print("=" * 60)
    if all_matched:
        print("결과: 모든 폴더의 파일 내용이 완벽하게 동일합니다.")
    else:
        print("결과: 일부 파일이 다르거나 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
