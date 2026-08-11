"""단순 PRE-SCA 명령행 진입점.

입력 CSV를 생성한 뒤 정상·오류주입 에뮬레이션을 실행한다. 키보드 중단은 정상
종료 코드 0, 예상하지 못한 예외는 종료 코드 1로 보고한다. CSV·로그 파일 생성이
주요 부작용이다.
"""

import sys
import make_TC
import emul

def main():
    """입력 벡터를 생성하고 에뮬레이션을 실행한다."""
    try:
        # 1. 테스트 케이스(Input Data) 생성
        make_TC.make_TC()

        # 2. 에뮬레이션 실행 (Normal -> Faulty)
        emul.run()

    except KeyboardInterrupt:
        print("\n[User Abort] Emulation stopped by user.")
        sys.exit(0)
    except Exception as e:
        # 최상위 레벨 에러 핸들링
        print(f"\n[Fatal Error] Program terminated unexpectedly: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
