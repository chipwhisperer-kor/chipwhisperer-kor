"""디버그 트레이스 수집기 — **이번 사이클에서 실행하지 않았다. 미검증이다.**

## 이 채널의 지위 — 타이밍 분석용 계측 설계

세 수집기 중 디버그 트레이스는 함수 진입·복귀 경계를 직접 표시할 수 있어
ISO/IEC 17825 §7.3.4 타이밍 분석용으로 설계했다. 아직 실장비로 검증하지 않았으므로
정확도나 동작을 확정하지 않는다.

| 채널 | 실행시간을 무엇으로 재나 | 한계 |
|---|---|---|
| `emulated-power` | 관측 구간의 **명령어 수** | 사이클이 아니다. Unicorn 에 사이클 모델이 없어 "같다" 를 증명하지 못한다 |
| `power` | 트리거 하이 구간의 **샘플 수** | 트리거 경계가 함수 경계와 정확히 같지는 않다 |
| **`debug-trace`** | 함수 진입·복귀 이벤트의 **타임스탬프 차** | trace tick 단위다. 함수 경계·클럭 소스·사이클 환산을 실기로 확인해야 한다 |

CoreSight 의 DWT 비교기에 암호화 함수의 진입·복귀 주소를 걸면 그 지점에서 이벤트가
나오도록 설정하고, 두 타임스탬프의 차를 실행 시간 관측값으로 저장한다.
`1.0.TraceWhisperer_main.ipynb`는 `scope.trace.set_isync_matches(addr0, addr1)`로 주소를
등록하고 `capture_once()`의 `times`를 읽는 예를 담고 있다. 그 노트북의 과거 출력이 새
수집기의 정확도나 함수 경계 대응을 검증하는 것은 아니다.

**에뮬레이션이 "명령어 수가 같다"고 해도 constant-time이 확정되지 않는다.** 실장비에서
이 채널의 타임스탬프와 전력 채널의 `trig_count`를 함께 확인해야 사이클 기준 소견을 낼 수 있다.

## 왜 아직 구현하지 않았는가

작성 당시에는 실장비가 없어 검증할 수 없었다. 그리고 **검증하지 않은 스키마를 구현으로
굳히면 나중에 고치기 어렵다.** 그래서 스키마(§3.5·§6.6)와 이 골격만 만들어 두었다.

## 파일을 나누는 이유

`capture_once()`는 전력 Trace와 이벤트 타임스탬프를 **함께** 돌려준다. 그러나
`SCHEMA.md §2` 는 한 파일에 Channel 이 다른 데이터를 섞지 말라고 정한다 — 측정 조건을
파일 단위로 적을 수 없게 되기 때문이다. 그래서 전력은 `channel_type="power"` 파일로,
이벤트는 `channel_type="debug-trace"` 파일로 나누고, **같은 입력 벡터를 쓰므로 행
인덱스로 대응**시킨다.

이벤트 수는 실행마다 다를 수 있으므로 고정 폭 배열에 담을 수 없다. 그래서
`event_time`(가변 길이) + `event_count` + `exec_time`(진입~복귀 차) 로 저장한다.
"""

import sys

from .. import paths

if str(paths.SCALIB) not in sys.path:
    sys.path.insert(0, str(paths.SCALIB))

STATUS = "미실행 — 수집기 미구현. 스키마와 골격만 있다."


def collect(spec, out_path, verbose=True):
    """디버그 트레이스 수집기의 미구현 경계를 명시적으로 알린다.

    `spec`과 `out_path`를 아직 사용하지 않으며 파일이나 장비를 변경하지 않는다. 이 함수는
    실행된 적이 없고 항상 구현·검증 절차를 담은 `NotImplementedError`를 발생시킨다.
    """
    raise NotImplementedError(
        "디버그 트레이스 수집기는 실장비가 필요하며 아직 구현·검증하지 않았다.\n"
        "  현재 상태: %s\n"
        "  실장비가 준비되면 다음 순서로 만든다:\n"
        "   1) 1.0.TraceWhisperer_main.ipynb 의 SWO 설정 절차를 그대로 따른다\n"
        "   2) ELF 에서 암호화 함수의 진입·복귀 주소를 찾아 set_isync_matches 에 건다\n"
        "      (주소는 빌드마다 달라지므로 상수로 박지 않는다)\n"
        "   3) 레코드마다 event_time(가변 길이)·event_count·exec_time 을 저장한다\n"
        "   4) channel_type='debug-trace' 로 **전력 파일과 분리해** 저장한다\n"
        "      — 같은 입력 벡터를 쓰므로 행 인덱스로 대응된다 (SCHEMA.md §2)\n"
        "   5) exec_time_unit='trace_tick' 과 exec_time_epsilon 을 반드시 기록한다\n"
        "      — 단위와 ε 가 없으면 |T1-T2| < ε 판정을 할 수 없다" % STATUS)
