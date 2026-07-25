# Papers_pdf 하위 참고문헌 묶음 (수집 메모)

대상 논문 루트 PDF와 **같은 stem의 하위 폴더**에 1-deep 참고문헌 PDF를 둔다.  
**변환·리서치 갭 입력은 `*.pdf`만** 사용한다. 이 파일은 사람용 메모이며 모델 컨텍스트에 넣지 않는다.

## 공통 규칙

- 경로: `Papers_pdf/<대상 논문명>/<파일>.pdf`
- 파일명 예: `[참고문헌 번호] 논문 제목.pdf`
- 미러 변환 출력: `Papers_md/<대상 논문명>/<동일 stem>.md`
- 큐 확인: `python3 kit/tools/list_pdf_queue.py`

## Public Coefficient Matters… (PCM-DFA)

- 대상: `Papers_pdf/Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE.pdf`
- 하위 폴더: 동명 디렉터리
- 참고문헌 약 37항 중 PDF 대상 약 35편 수집 (웹·소프트웨어 항 제외)
- 번호 공백 예: `[8]`, `[35]` 등 비PDF 항목은 폴더에 두지 않음

## 양자 내성 암호 HAETAE… (HAETAE-FIA)

- 대상: `Papers_pdf/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf`
- 하위 폴더: 동명 디렉터리
- 참고문헌 24개 PDF 수집 기록

수집 상세 CSV가 패키지에 없으면 카탈로그·이 메모·파일 목록으로 충분하다. 외부 매니페스트 경로에 의존하지 않는다.
