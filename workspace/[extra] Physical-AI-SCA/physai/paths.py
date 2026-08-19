"""저장소 안에서 이 서브프로젝트가 쓰는 경로를 한곳에서 푼다.

경로는 **이 파일 위치를 기준으로 한 상대경로**로만 계산한다. 절대경로를 박으면
다른 사람이 클론한 저장소에서 깨지고, cwd 에 의존하면 어디서 실행했느냐에 따라
다른 파일을 집는다.

여기서 `workspace/lib` 를 sys.path 에 넣으므로, 이 패키지의 다른 모듈은
`import sca_schema` / `import aes_ref` / `import elfParser` 를 그냥 쓰면 된다.
"""

import sys
from pathlib import Path

# physai/paths.py → physai/ → [extra] Physical-AI-SCA/ → workspace/
PROJECT = Path(__file__).resolve().parent.parent
WORKSPACE = PROJECT.parent

LIB = WORKSPACE / "lib"                     # 저장소 공용 파이썬 정의
IUT = WORKSPACE / "iut"                     # IUT(테스트 대상 구현) 암호 라이브러리
SCALIB = WORKSPACE / "[extra] SCALib"       # 실측 Dataset·수집 라이브러리

HARNESS = PROJECT / "emul_harness"
HARNESS_BUILD = HARNESS / "build"
CONTRACTS = PROJECT / "contracts"
EXP = PROJECT / "exp"
RUNS = PROJECT / "runs"
TRACES = PROJECT / "traces"

# 공용 라이브러리는 앞에 둔다 — 이 저장소의 정의가 우선이어야 한다.
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))



def harness_elf(iut_name):
    """IUT 이름에 대응하는 에뮬레이션 ELF의 절대 `Path`를 반환한다.

    파일을 변경하지 않는다. 빌드 산출물이 없으면 실행 가능한 빌드 명령을 포함한
    `FileNotFoundError`가 발생한다.
    """
    p = HARNESS_BUILD / ("%s.elf" % iut_name)
    if not p.is_file():
        raise FileNotFoundError(
            "에뮬레이션 ELF 가 없다: %s\n"
            "먼저 빌드한다:  make -C emul_harness IUT=%s" % (p, iut_name))
    return p


def run_dir(run_id, create=False):
    """`runs/<run_id>/`의 절대 `Path`를 반환한다.

    `create=True`일 때만 부모 디렉터리까지 생성한다. 생성 실패 시 운영체제 예외가
    호출자에게 전파되며 기존 파일은 덮어쓰지 않는다.
    """
    p = RUNS / run_id
    if create:
        p.mkdir(parents=True, exist_ok=True)
    return p
