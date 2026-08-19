"""부채널 시험 알고리즘 계약.

수집기와 분석기는 알고리즘 이름을 조건문으로 비교하지 않고 이 계약을 사용한다. 새
알고리즘은 폭·골든 연산·DPA 분할을 구현하고 ``REGISTRY``에 명시적으로 등록해야 한다.
CPA나 soundness를 제공하지 않으면 해당 필드를 ``None``으로 두며 도구는 적용 불가로
보고한다.
"""

from . import aes128


REGISTRY = {aes128.ID: aes128}


def get(algorithm_id):
    """등록된 알고리즘 모듈을 반환하고, 미등록 ID는 설명 가능한 오류로 거부한다."""
    try:
        return REGISTRY[algorithm_id]
    except KeyError as exc:
        raise ValueError("지원하지 않는 algorithm: %s (등록: %s)"
                         % (algorithm_id, ", ".join(sorted(REGISTRY)))) from exc
