"""실물 전력 수집기 — **이번 사이클에서 실행하지 않았다. 미검증이다.**

## 이 파일의 상태를 먼저 밝힌다

작성 시점에 ChipWhisperer 실장비 환경이 구성되어 있지 않아 **한 번도 실행하지 않았다.**
코드가 맞아 보인다는 이유로 동작한다고 쓰지 않는다. 실기로 확인하기 전까지 이 파일은
**설계 문서에 가깝다.**

실행하면 `NotImplementedError` 대신 아래 `collect()` 가 도는데, 처음 돌릴 때는
소량(수십 장)으로 먼저 확인하고 골든 AES 가 일치하는지부터 본다.

## 무엇을 재사용하는가

장비 제어(연결·클럭·게인·캡처·자동 복구)는 이미 `[extra] SCALib/dataset_collect_lib.py`
에 있고 **실측으로 검증된 코드**다. 12만 장 수집이 세 번 깨졌다가 스스로 회복한 이력이
그 증거다(`recoveries` attr). 그것을 다시 쓰지 않고 새로 짜는 것은 검증된 코드를 버리는
일이므로, 여기서는 경로를 넣어 그대로 import 한다.

**`workspace/lib/cw_bench.py` 로 승격하지 않은 이유**: `Bench._reopen()` 이 SCALib 전용
`_seed_masks()` 를 직접 호출하므로(`dataset_collect_lib.py:845`) 중립 모듈이 되려면
콜백 인자를 추가하는 로직 변경이 필요하다. 그런데 실장비가 없어 **그 변경을 검증할 수
없다.** 검증 없는 하드웨어 리팩터링은 조용히 수천 장을 망가뜨린다.
실기 확인 후 승격한다.

## 이 수집기가 채워야 하는 것 (SCHEMA 1.1)

에뮬레이션 수집기와 달리 물리 측정이므로 다음이 **추가로** 필요하다.

| 필드 | 왜 |
|---|---|
| `bandwidth_hz` | Annex B `[B.01]`·`[B.02]` 판정. 없으면 요건을 **판정할 수 없다** |
| `shunt_ohm`·`shunt_selection_note` | `[B.05]`·`[B.06]` — 동작 가능한 최대 저항을 골랐는지 |
| `exec_time` (레코드별) | §7.3.4 타이밍 분석. **트리거 하이 구간의 샘플 수**(`scope.adc.trig_count`) |
| `preprocessing_average_n` | A.2.5 `shall [A.01]` — Level 3 은 같은 입력 10회 평균을 요구한다 |

**기존 `[extra] SCALib` 데이터셋에는 이 값들이 없다.** 그래서 요건 대조표가 `미기록`
으로 보고한다. 값을 모르면서 지어내면 다음 사람이 그것을 측정값으로 오해한다(SCHEMA §5.3).

> `preprocessing_average_n` 은 수집 방식을 바꾼다 — 트레이스 1장을 얻으려고 같은 입력을
> 10회 실행해 평균 내야 하므로 수집 시간이 10배가 된다. Level 3 을 주장하려면 그 비용을
> 치러야 하고, 치르지 않았다면 대조표에 `미준수` 로 적힌다.
"""

import sys

from .. import paths

# 검증된 장비 제어 코드를 그대로 쓴다. SCALib 프로젝트 경로를 넣어 import 한다.
if str(paths.SCALIB) not in sys.path:
    sys.path.insert(0, str(paths.SCALIB))

STATUS = "미실행 — 실장비 미구성. 이 모듈은 한 번도 실행된 적이 없다."


def collect(spec, out_path, verbose=True):
    """spec 대로 실물 전력 파형을 수집한다.

    **주의: 이 함수는 실행된 적이 없다.** 처음 돌릴 때는 소량으로 확인한다.
    """
    raise NotImplementedError(
        "실물 전력 수집기는 실장비가 필요하고 이번 사이클에서 구현·검증하지 않았다.\n"
        "  현재 상태: %s\n"
        "  실장비가 준비되면 다음 순서로 만든다:\n"
        "   1) dataset_collect_lib 의 connect_all_devices/setup_husky/Bench 로 벤치를 세운다\n"
        "   2) measure_trig_count 로 파형 길이를 실측한다 (상수 금지)\n"
        "   3) Bench.capture() 로 수집하고 레코드마다 trig_count 를 exec_time 에 남긴다\n"
        "   4) bandwidth_hz·shunt_ohm·shunt_selection_note·preprocessing_average_n 을 기록한다\n"
        "      — 이 값들이 없으면 ISO/IEC 17825 Annex B 요건을 판정할 수 없다\n"
        "   5) 소량(수십 장)으로 골든 AES 일치를 먼저 확인한다\n"
        "  자세한 배경은 이 파일의 머리말에 있다." % STATUS)
