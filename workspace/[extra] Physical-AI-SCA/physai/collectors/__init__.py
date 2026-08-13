"""관측 채널별 수집기 패키지.

`emulation`은 명령어별 누설 모델을, `cw_power`는 ChipWhisperer 실물 전력을 수집한다.
둘 다 `physai.collect`가 명세의 `collector.kind`에 따라 호출한다.
"""
