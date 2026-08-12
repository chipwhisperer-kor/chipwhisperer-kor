"""단순 PRE-SCA 명령행 진입점.

입력 CSV를 생성한 뒤 정상·오류주입 에뮬레이션을 실행한다. 키보드 중단은 정상
종료 코드 0, 예상하지 못한 예외는 종료 코드 1로 보고한다. CSV·로그 파일 생성이
주요 부작용이다.
"""

import sys
import make_TC
import emul

def main():
    """결정적 입력 CSV를 만든 뒤 정상·오류주입 에뮬레이션을 실행한다.

    CSV·디스어셈블·로그 파일을 생성하거나 덮어쓴다. 키보드 중단은 종료 코드 0, 다른
    예외는 원인을 출력하고 종료 코드 1로 `sys.exit()`한다. 성공하면 반환값은 없다.
    """
    try:
        make_TC.make_TC()

        emul.run()

    except KeyboardInterrupt:
        print("\n[User Abort] Emulation stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Fatal Error] Program terminated unexpectedly: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
