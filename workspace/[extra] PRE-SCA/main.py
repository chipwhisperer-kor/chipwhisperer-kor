import sys
import make_TC
import emul

def main():
    """
    Main Entry Point
    
    1. 테스트 케이스(입력 벡터)를 생성합니다.
    2. 에뮬레이션 코어를 실행하여 시뮬레이션을 수행합니다.
    """
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
