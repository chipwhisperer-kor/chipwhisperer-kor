# `workspace/iut/` — Implementation under test / IUT(테스트 대상 구현)

이 디렉터리는 저장소가 부채널 분석 대상으로 삼는 암호 라이브러리를 모아 둔 곳이다.
IUT는 비침습 방식으로 시험하는 구현이며, Dataset Metadata의 `iut_algorithm`·
`iut_implementation`·`iut_countermeasure`가 알고리즘·구현·대책을 각각 식별한다.

| 라이브러리 | 알고리즘 | 대책 | 출처 |
|---|---|---|---|
| `tiny-AES-c/` | AES-128 ECB/CTR/CBC | 없음 | <https://github.com/kokke/tiny-AES-c> (Unlicense / public domain) |
| `masked-aes-c/` | AES-128 ECB/CTR/CBC | 1차 부울 마스킹 (`CipherMasked` 구간만) | <https://github.com/CENSUS/masked-aes-c> (MELITY PoC, Unlicense / public domain) |

---

## 1. 왜 서브프로젝트 밖에 있는가

**같은 소스를 컴파일해야 서로 다른 관측을 나란히 놓을 수 있기 때문이다.**

이 저장소는 한 구현을 **세 가지 방식**으로 관측한다.

| 관측 | 무엇을 보나 | 쓰는 곳 |
|---|---|---|
| 실물 전력 트레이스 | 실제 칩에서 물리적으로 새는가 | `[extra] SCALib/simpleserial_{tiny-AES-c,masked-aes-c}/` |
| 디버그 트레이스 | 실행 흐름이 데이터에 의존하는가 | `[extra] Physical-AI-SCA/` (실장비 필요) |
| 에뮬레이션 | 이론이 끊어 놓은 누설 고리를 구현이 되살렸는가 | `[extra] Physical-AI-SCA/emul_harness/` |

셋이 서로 다른 빌드의 서로 다른 소스를 보면, "에뮬레이션에서 찾은 결함이 실측 타겟에도
있다"고 말할 근거가 사라진다. 그래서 라이브러리를 **저장소에 한 벌만** 두고 모든 빌드가
이 파일들을 직접 컴파일한다. 사본을 만들지 않는다 (`AGENTS.md` 원칙 1-2).

이전에는 `[extra] SCALib/` 안에 있었으나, 두 번째 소비자(에뮬 하네스)가 생기면서
공용 트리로 올렸다.

### 이 라이브러리를 쓰는 곳

| 참조하는 곳 | 방식 |
|---|---|
| `[extra] SCALib/simpleserial_tiny-AES-c/makefile` | `VPATH += ../../iut/tiny-AES-c` |
| `[extra] SCALib/simpleserial_masked-aes-c/makefile` | `VPATH += ../../iut/masked-aes-c` (`-DMASKED=1`) |
| `[extra] Physical-AI-SCA/emul_harness/Makefile` | `../../iut/<lib>/aes.c` 직접 컴파일 |

**경로를 옮기면 위 세 곳을 함께 고치고 `clean` 재빌드한다.** 빌드 산출물
(`objdir-*/*.lst`, `.elf`)에 소스 경로가 문자열로 박히기 때문에, 재빌드하지 않으면
낡은 경로를 가진 바이너리가 남는다.

---

## 2. `masked-aes-c` 에 가한 패치 — 3건

벤더 원본은 **마스크가 스택 지역변수**라 외부에서 읽을 수 없고, 매 블록 `srand(time(NULL))`
를 호출하며, 난수 생성에 명백한 실수가 있다. 연구 목적의 최소 수정 세 가지를 가했다.
**암호·마스킹 공식 자체는 바꾸지 않았다.**

| # | 위치 | 수정 | 왜 |
|---|---|---|---|
| 1 | `AES_get_last_masks()`·`last_masks` | 마지막 마스크 10바이트를 읽는 연구용 API 추가 | 마스크를 밖에서 읽을 수 있어야 **연구자 관점** 분석(마스크를 아는 상태의 진단)이 가능하다. 공격자 관점 분석은 이 값을 쓰지 않는다 |
| 2 | `CipherMasked()`의 `srand(time(NULL))` 호출 | 암호화마다 하던 시간 기반 재시드 제거 | STM32F303 에는 TRNG 가 없고 임베디드에서 `time(NULL)` 은 의미가 없다. 매 블록 재시드는 엔트로피를 오히려 해친다. **시드는 호스트가 `0x81 's'` 로 준다** |
| 3 | `random_uint8()` | `rand() % 0xFF` → **`rand() & 0xFF`** | 원본은 0–254만 내놓아 `0xFF`가 절대 나오지 않는다. 수정은 전체 바이트 범위를 허용하지만, `rand()` 하위 비트의 균일성이나 암호학적 안전성을 보장하지는 않는다 |

3번은 소스 식으로 확인되는 벤더 원본의 범위 결함을 고친다. 수정 전 식은 결과가 최대
254이고, 수정 후 식은 255도 결과로 허용한다. 이는 값의 범위에 관한 설명일 뿐 실제
난수 분포를 측정했다거나 `rand()`가 CSPRNG라는 뜻은 아니다.

### 마스크 레이아웃 (`AES_get_last_masks` 출력 10바이트)

```
[ M1  M2  M3  M4  M'  M  M1' M2' M3' M4' ]
   난수 6바이트         MixColumns 유도 4바이트
```

구현에서 유도한 마스킹된 중간값:

```
SubBytes 입력 레지스터 = p ^ k ^ mask[4]
SubBytes 출력 레지스터 = SBOX[p ^ k] ^ mask[5]
```

### 보호 범위 — 반드시 알고 있어야 할 한계

`masked-aes-c` 는 **`CipherMasked` 안만 보호한다.** `KeyExpansion` 은 벤더 원본 그대로
비마스킹이다. 그런데 이 저장소의 펌웨어는 키 스케줄을 트리거 **안**에서 수행하므로,
트레이스 앞부분은 마스킹 여부와 무관하게 무방비다.

**이것은 마스킹의 실패가 아니라 이 PoC 의 설계된 보호 범위 밖이다.** 분석에서 두 타겟을
전 구간으로 비교하면 이 공통 누설이 마스킹 효과를 완전히 가린다. 비교는 암호화 구간에서만
한다 — 근거와 절차는 `[extra] SCALib/README.md` §3 에 있다.

---

## 3. `tiny-AES-c` — 무수정

벤더 원본 그대로다. 펌웨어 빌드에서 `-DCBC=0 -DCTR=0` 으로 ECB 경로만 남긴다
(코드 크기 축소, 교육용 경로 단일화). 소스에는 손대지 않는다.

이 라이브러리는 비교의 **기준선(baseline)** 이자 누설 검출기의 **양성 대조군**이다.
같은 실행 조건에서 기대한 반응이 없으면 Dataset, 라벨, 표본 수, 누설 모델과 검출기 설정을
함께 점검해야 한다. 어느 한 원인으로 단정할 수 없으며, 대조군이 유효하게 반응하기 전의
음성 결과는 안전성 근거로 쓰지 않는다.

---

## 4. 라이선스

두 라이브러리 모두 **Unlicense**(public domain)이며 각 디렉터리의 `unlicense.txt` 가 원문이다.
이 저장소의 패치도 같은 조건으로 둔다.
