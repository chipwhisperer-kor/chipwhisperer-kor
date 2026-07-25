# Research_gaps — 리서치 갭 결과물 층 (프레임워크 계약)

패키지 목표의 **하류 단계**다. 도메인·키워드에 묶이지 않는다.

```text
Papers_pdf → Papers_md (공유) → Research_gaps/themes/<theme_id>/ (의도별)
```

## 역할

| 층 | 경로 | 테마 의존 |
|----|------|-----------|
| 원문 | `../Papers_pdf/` | 아니오 |
| 변환 베이스 | `../Papers_md/**/*.md` (텍스트만; 이미지 없음) | 아니오 |
| **갭 결과** | `themes/<theme_id>/` | **예** |

같은 베이스에 사용자 의도(키워드·질문·범위)만 다른 테마를 **병렬** 추가한다.  
`Papers_md`를 테마 안에 **복사하지 않는다.** 인용 = 상대경로 + source PDF 페이지.  
갭 입력은 **단일 MD**다. 그림 파일·사이드카를 컨텍스트에 넣지 않는다. 캡션·페이지 표기는 MD 텍스트에 있다.

## 레이아웃

```text
Research_gaps/
  README.md                 # 이 계약 (도메인 비종속)
  INDEX.md                  # 테마 레지스트리
  themes/
    _TEMPLATE/              # 새 테마 복사 원본
    <theme_id>/             # worked example 또는 신규 테마
      META.md
      SCOPE.md
      REPORT.md             # 선택·제출 시
      synthesis.md          # 선택
      gaps/Gnnn-*.md
      notes/                # 선택
```

## 새 테마 절차 (프레임워크)

1. `themes/_TEMPLATE/` 를 `themes/<theme_id>/` 로 복사한다.  
   `theme_id` = 의도 슬러그 + 날짜 (도메인 자유).
2. `META.md`에 intent(키워드·한 줄 목적), status, base 고지.
3. `SCOPE.md`에 포함·제외 논문(`Papers_md/...`)·연구 질문. 추상 키워드만이면 구체화 축을 둔다.
4. `gaps/`에 후보 단위 파일 (claim / evidence / status / open questions).
5. 필요 시 `REPORT.md`·`synthesis.md`.
6. `INDEX.md`에 한 줄 등록.

## 규칙

1. 새 의도 = **새 theme_id 폴더** (기존 테마 덮어쓰기 금지).
2. 증거: `Papers_md/...` + **`Papers_pdf/...` 페이지** (MD만으로 확정 금지).
3. 최종 인용 = PDF 페이지 (`kit/PDF_TO_MARKDOWN.md`).
4. 변환 도구(`kit/tools`)는 갭 엔진이 아니다. 갭은 이 폴더 계약으로 수행.
5. 라이선스 unknown 자료 결과의 외부 공개 전 확인.

## 등록된 테마

`INDEX.md` — 목록의 개별 테마는 **예시 실행**일 뿐 필수 구성이 아니다.
