# PicoScope 3418E·ChipWhisperer 3중 파형 비교

이 서브프로젝트는 하나의 STM32F303 타겟이 실행하는 AES-128·SHA-256 복합
연산을 **ChipWhisperer-Lite, ChipWhisperer-Husky, PicoScope 3418E**로 동시에
측정한다. 사용자는 웹 code-server에서
`1.0.Wiretapping4SCA-PicoScope.ipynb`를 열고 **Run All**만 실행하면 장비 점검,
타겟 펌웨어 빌드·플래싱, 3중 수집, 시각·통계 비교를 순서대로 확인할 수
있다.

## 배선

Lite는 타겟 프로그래밍·UART·클럭 공급을 담당한다. Husky와 PicoScope는 통신에
개입하지 않고 같은 연산을 수동 관측한다.

| 신호 | 연결 |
|---|---|
| 타겟 전력/션트 | Lite 내장 측정 경로 + Husky Measure + PicoScope A |
| 타겟 GPIO4/TRIG | Lite 내장 트리거 + Husky USERIO D0 + PicoScope B |
| 타겟 클럭 | Lite HS2→CW308 CLKIN, 같은 신호를 Husky AUX MCX로 분기 |
| USB | Lite·Husky·PicoScope를 privileged `chipwhisperer-kor` 컨테이너에 노출 |

PicoScope B에는 한 트랜잭션당 두 HIGH 펄스가 보인다. 첫 펄스는 AES 키
확장·10라운드, 두 번째는 SHA-256 연산 구간이다. 노트북은 이 펄스를 실제
시간 구간의 정본으로 사용한다.

## 실행 조건과 부수 효과

- `setup/docker-compose.yml`로 실행한 기본 컨테이너와 `/dev/bus/usb` 매핑이
  필요하다.
- 첫 실행은 `pypicosdk`와 Pico native driver를 이 디렉터리의 `.runtime/`에
  받으므로 네트워크가 필요하다. 캐시가 있으면 다음 실행은 다시 받지 않는다.
- Run All은 `simpleserial_main/`에서 펌웨어 산출물을 잠시 만들고 STM32F303을
  덮어쓴 뒤 산출물을 정리한다. 장비 핸들은 성공·실패 시 모두 해제한다.
- 파형은 메모리에만 유지한다. 유사성에 임의 합격선을 적용하거나 Dataset,
  CPA/DPA 결과를 저장하지 않는다.

노트북 설정 셀이 시리얼, 버전, 캡처 횟수, 샘플링 제약의 단일 정본이다.
값을 바꾸려면 README에 복사하지 말고 해당 셀만 수정한다.
