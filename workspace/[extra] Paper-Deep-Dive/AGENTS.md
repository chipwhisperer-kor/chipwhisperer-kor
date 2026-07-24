# Agent entry

**필수 속성: 자기완결성(Self-contained).** 이 폴더만 받은 제3의 AI가 외부 정보 없이 이어받을 수 있어야 한다. 경로는 루트 기준 상대경로, 대화로 정한 것은 그 턴에 폴더 안 문서로. → `PROMPT.md` §0

0. **제일 먼저 — 작업 루트 확인.** `pwd`가 `.Intermediate_Artifacts/SYNC.md`의 작업 루트와 다르면 **쓰지 말고** 사용자에게 알린다. 사본은 모두 자기완결적이라 겉으로 구별되지 않는다 (S7)
1. 최초/구조 변경 시 `README.md`
2. 매 세션 `PROMPT.md` · `AI_ROSTER.md` · 자기 `roles/<role_id>/`
3. 매 턴 자기 `To_Do_<Role>.md` · `.Intermediate_Artifacts/HANDOFF.md`
   - 채팅 **`계속`**(파일명 없어도 동일) = **자기** `To_Do_<Role>.md`의 `## 사용자 답변 칸`. 비어 있으면 자기 대상 `ready` handoff를 처리하고, 그것도 없으면 대기
   - 채팅 **`초기화`** = 이전 기억을 버리고 폴더만으로 재부트스트랩 후 보고 (`BOOTSTRAP_PROMPT.md`). **파일을 지우는 명령이 아니다** — AI 인식만 초기화
   - 처리 후 답변 칸은 **내용만** 비운다 (코드 펜스·섹션 유지) + `최근 완료` 한 줄
4. handoff 생성·소비 전에만 `ARTIFACT_CONTRACTS.md`
5. 같은 요청을 여러 AI가 받아도 쓰기 소유는 바뀌지 않음
