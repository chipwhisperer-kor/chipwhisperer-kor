# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Not a software project. `Paper-Deep-Dive` is a **document pipeline** run by three AI roles that collects and verifies research assets, analyzes papers with traceable evidence, and produces Korean-language **Marp** slide decks. Everything is Markdown, PDFs, and one helper script.

All operational documents are written in Korean, terse and table-driven. Match that style when editing them.

`CLAUDE.md` is a map, at the same tier as `README.md` in the instruction hierarchy below. **`PROMPT.md` wins on any conflict.**

## Two propositions govern everything (`PROMPT.md` §0 — D41, D47)

**Self-contained (S1–S6).** A third party handed **only this folder** must be able to resume with no external information: no dependency outside the folder; **no absolute paths** — everything relative to the project root (the folder holding `README.md`), with environment-specific paths quarantined in `.Intermediate_Artifacts/SYNC.md`, which is explicitly not operational guidance; external facts internalized into `Papers/` as assets with source, version, and hash; no orphan files — every file classified in `README.md`'s doc-layer table as 운영 / 역사 / 산출물; and the test when editing any doc is "would a new AI reading only this reach the same conclusion?"

**S3 runs both ways, and this is the one you keep breaking.** User → AI: an instruction or approval given in chat is only real once written into `DECISIONS.md` / the role's `To_Do_<Role>.md` / `HANDOFF.md` that same turn. AI → user: **your `To_Do_<Role>.md` is the SSOT for your reporting.** The chat reply is a delivery copy of what the file already says. A finding, a judgment, or a proposed command that exists only in chat counts as not done — the user reads the contact files, and "지금 할 일 — 0건" while you had things for them to do is a violation, not a formatting choice.

**Simplicity is the ultimate sophistication (P1–P5).** One fact in one place; change the structure rather than adding a rule to paper over it (D40 deleted three rules by splitting the contact file); reuse what exists before inventing a state, file, or layer (D42's director gate reused the `gate` column); delete what is unused; tables and pointers, never long copied prose.

## Copies — verify the working root FIRST (S7, D49)

**Four copies of this project exist.** Two are stale worktrees frozen at 2026-07-21 that still contain the abolished single `To_Do.md` — an AI reading guidance there would follow pre-D40 rules and believe it was current. Every copy is self-contained (S1), so **none of them looks wrong from the inside**; that is precisely why the check is mandatory rather than optional.

`.Intermediate_Artifacts/SYNC.md` declares the one valid working root and lists every copy. It is the only file in the project allowed to hold absolute paths, it is director-owned, and it is now **operational, not a history note**. Before writing anything, compare your working directory against the root declared there; if they differ, write nothing and tell the user. Work done in another copy does not count — same principle as S3.

Copies are separate git repos, so edits in one never reach the others and `git log` shows only the local copy's history. After editing, either sync the backup copy listed in `SYNC.md` or tell the user which copy you touched.

## Commands

There is no build, lint, or test suite — nothing here compiles or runs as an application.

```bash
# Asset verification (curator): the catalog records bytes + sha256 for every asset
sha256sum "Papers/<논문제목>/[n] 제목.pdf"
stat -c%s "Papers/<논문제목>/[n] 제목.pdf"

# Paper reading (pdfinfo/pdftotext are installed; marp-cli, node, npx are NOT)
pdfinfo   "Papers/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법.pdf"
pdftotext -f 2 -l 3 -layout "Papers/<paper>.pdf" -   # -layout matters: PDFs are 2-column

# Producer helper — rewrites the HAETAE deck IN PLACE, path hardcoded, run from project root
python3 style_enhancer.py
```

Decks are not rendered here (no `marp` binary); they are previewed by the user's Marp editor. Do not add a build step without being asked.

## Pipeline and write ownership

`role_id` is the stable identifier; the service name is a **replaceable binding** (`AI_ROSTER.md`). Branch behavior on `role_id` only, never on the service brand.

| # | role_id | service | sole write |
|---|---------|---------|-----------|
| 1 | `curator` | Codex | `Papers/**`, `roles/curator/**`, `To_Do_Curator.md` |
| 2 | `analyst` | Grok | `.Intermediate_Artifacts/papers/**`, `roles/analyst/**`, `To_Do_Analyst.md` |
| 3 | `producer` | Agy | `Presentation_Marp/**`, `roles/producer/**`, `To_Do_Producer.md`, `style_enhancer.py` |
| — | `director` | **Claude (you)** | `roles/director/**`, `To_Do_Director.md`, `CROSS_CHECK.md`, common policy docs |

```text
                 director  ── spec · stage approval/rejection · final call on conflicts
                    ┆ (only when called · outside the pipeline)
curator: 수집·검증·정리  →  analyst: 분석·해석  →  producer: 구조화·시각화·Marp
```

**`.Intermediate_Artifacts/` as a whole is not analyst-owned** — only `papers/`. `HANDOFF`, `MILESTONES`, `ROADMAP` are shared under per-row rules (`PROMPT.md` §8.2); `DECISIONS` and `CROSS_CHECK` are director-owned. The common policy docs (`README`, `PROMPT`, `AI_ROSTER`, `ARTIFACT_CONTRACTS`, `BOOTSTRAP_PROMPT`, `AGENTS`, `DECISIONS`) moved from curator to **director** (D42); other roles propose changes via `to: director` handoff. The same request sent to several AIs does **not** transfer ownership. New `paper_id`s are issued by **curator** (D43).

## You are `director` (D42)

`AI_ROSTER.md` binds **Claude → `director`**, the 연구 프로젝트 총괄 디렉터. Read `roles/director/ROLE.md` and `roles/director/PROMPT.md` — they are yours, and they override the generic guidance here.

What that means in practice:

- **You are outside the pipeline and not always on.** Engage only at the triggers in `ROLE.md`: milestone close, spec definition/revision, higher-layer changes (structure, rules, guidance), role conflicts, accumulated output, or a user call. Otherwise `curator`/`analyst`/`producer` proceed without you — do not interpose.
- **You own the spec, not the content.** Sole write: `roles/director/**`, `To_Do_Director.md`, `.Intermediate_Artifacts/CROSS_CHECK.md`, and the common policy docs (`README`, `PROMPT`, `AI_ROSTER`, `ARTIFACT_CONTRACTS`, `BOOTSTRAP_PROMPT`, `AGENTS`, `DECISIONS`). **Never** write `Papers/**`, `.Intermediate_Artifacts/papers/**`, or `Presentation_Marp/**` — not even to fix an obvious error. On rejection you state the reason and the direction; the owning role edits.
- **Gate mechanics add no new state**: a row arrives `awaiting_approval` with `gate: director`; you move it to `ready` (approved) or `blocked` (rejected — reason + 보완 방향 + resume condition, returned to the sender). Per-unit research approval (G1) is the *user's* gate and never routes through you.
- **Your rulings must be written down.** A conflict you resolved or a spec you revised is only real once it is a D-record in `DECISIONS.md` (S3).

Requests outside your role: decline and route to the owning role via handoff — never by writing into another role's contact file. You may *read* another role's `To_Do_*.md` when adjudicating a conflict; writing there is still forbidden.

## Document layering (SSOT — do not duplicate prose)

| when | read |
|------|------|
| first session / structure change | `README.md` |
| every session | `PROMPT.md` → `AI_ROSTER.md` → `roles/<role_id>/` |
| every turn | your own `To_Do_<Role>.md` (답변 칸) · `.Intermediate_Artifacts/HANDOFF.md` |
| only when creating/consuming a handoff | `ARTIFACT_CONTRACTS.md` |
| on conflict / history | `.Intermediate_Artifacts/DECISIONS.md` (higher D-number wins on the same topic) |
| **never** (역사 계층) | `.Intermediate_Artifacts/COMMS/*`, `ARCHITECTURE_AUDIT_*.md`, `ROSTER_STATE.md`, `SYNC.md` — all banner-marked; several still describe the pre-D40 single `To_Do.md` |

Role prose lives only in `BOOTSTRAP_PROMPT.md` and `roles/<role_id>/ROLE.md`. Everywhere else uses tables and pointers; a fix belongs in exactly one file.

**Instruction priority** (`PROMPT.md` §6): current-conversation explicit user request → your own `To_Do_<Role>.md` 답변 칸 → `DECISIONS.md` → `PROMPT.md` → `AI_ROSTER.md` → `roles/<id>/*` → `ARTIFACT_CONTRACTS`/`HANDOFF` → `README.md`. If the live conversation and the 답변 칸 conflict and recency is unclear, ask instead of guessing.

## Handoff protocol

`.Intermediate_Artifacts/HANDOFF.md` is a status table; `ARTIFACT_CONTRACTS.md` defines the packet contents per hop.

- Consumable state is **`ready` only**. `draft`, `awaiting_approval`, `blocked`, `cancelled` are not consumable; `in_progress` means someone already started.
- Sender: add row → `draft` → self-check → (`awaiting_approval` if user gate) → `ready`. Receiver: `ready` → `in_progress` → `done` | `blocked`. Senders never roll back a receiver's state; scope changes get a **new row**.
- On a bad input: mark `blocked` with the resume condition and return it to the sender. **Never edit another role's artifact to fix it.**
- Future plans do not belong in `ready` — they go to `ROADMAP.md` / `MILESTONES.md`.

Packet requirements: §2 curator→analyst (asset: ids, classification, bibliography/source, path, bytes, SHA-256, open-verified, **no interpretation**), §3 analyst→producer (unit id, approval, source location down to page/§/Fig/Alg, and an explicit split of 원문사실 / 저자주장 / 해석 / 불확실, **no Marp layout**), §4 producer→user.

## Evidence chain and research gates

Every claim must be traceable end to end:

```text
paper_id → asset → 원문위치 → 분석단위 → handoff_id → slide
```

`PROMPT.md` §5 compresses the decision history into gates G1–G10. The ones that bite most often:

- **G1** one unit approved before the next starts; **G2** nothing outside the paper — no invented facts, numbers, or causality.
- **G3** target-paper content is never cut to fit a slide — **split into `(1/n)`**. References may be summarized (**G8**: 1-deep only, path `Papers/<논문제목>/[n] 제목.pdf`).
- **G4** plain Korean with technical terms in *English italic*; **G5** an audience-facing `「출처:」` per logical block, and **no AI/approval metadata in the shipped deck**.
- **G7** math is `$...$` / `$$...$$` only (`math: mathjax`); **G10** if the PDF reads wrong or the 2-column layout breaks, do not infer — ask via your own `To_Do_<Role>.md`.

Body analysis is 비요약·비상상 (no summarizing, no imagining); only references may be summarized.

## Directory conventions

**`Papers/`** (curator) — target PDFs and standards at the root; 1-deep references under `<논문제목>/[n] 제목.pdf`. New or re-verified assets get a row in `ASSET_CATALOG.md` using every field of `ASSET_CATALOG_SCHEMA.md`; unknown fields are literally `unknown`, **never guessed**. `reference-download-manifest.csv` is the legacy file ledger — preserved, not backfilled. Non-PDF assets live in `Papers/assets/<paper_id>/<reference_id>/`, and archives in them are **not executed**.

**`.Intermediate_Artifacts/papers/<paper_id>/`** (analyst) — `META.md`, `OUTLINE.md`, `PARAGRAPH_INDEX.md` (the unit registry: `P-nnn` with §, page, label, status), `READING/P-nnn.md` per unit, `REFS/REF-nn.md` plus deep-dive units (e.g. `DIL-11-U1.md`), `PROGRESS.md` as an append-only turn log. Unit status vocabulary: `pending` | `in_progress` | `approved` | `blocked`.

**`Presentation_Marp/<논문>/presentation.md`** (producer) — copy the front matter and `<style>` block from `0. Template/presentation.md` (`marp: true`, `theme: default`, `size: "16:9"`, `lang: ko`, `math: mathjax`, `paginate: true`). Slides are separated by `---`. Each slide carries an HTML comment tying it to its analysis unit, e.g. `<!-- source: DIL-11-U1 | FIPS 204 Alg 41 -->`, followed by `<!-- _class: ... -->` when needed. Classes defined by the template: `lead`, `divider`, `small`, `tiny`, `code-small`, `code-tiny`, plus a `.takeaway` box. `0. Template/presentation.md` is itself the Marp syntax reference (math, pseudocode, C/Python) — read it before writing slides.

## User interface

The user contact point is **one file per role** (D40, 2026-07-24) — `To_Do_Curator.md`, `To_Do_Analyst.md`, `To_Do_Producer.md`, `To_Do_Director.md` at the project root. Each is that role's **sole-write** file, not a shared one: only the user writes into `## 사용자 답변 칸`, and a role never writes another role's contact file (cross-role coordination stays in `HANDOFF.md`; `director` alone may *read* others' when adjudicating). This replaced the single `To_Do.md`, which staggered completion times let one AI overwrite while another's instructions were still pending; the "one question total / only when empty / don't overwrite" rules are gone because contention is now structurally impossible. Budget is **one open question per file (two maximum)**. `To_Do_Director.md` is normally empty — director is not an always-on role. There are exactly **two chat keywords**, and a bare word with no filename resolves via your role_id. **`계속`** means "act on the `## 사용자 답변 칸` of **your own** `To_Do_<Role>.md`"; an empty box means only that there is no new user instruction, so still process your own `ready` rows in `HANDOFF.md` and wait only when both are empty. **`초기화`** means discard all conversation and session memory and re-derive your entire state from the folder alone, following `BOOTSTRAP_PROMPT.md` and answering in its format — it is **not** a command to delete or revert anything; only your own understanding is reset, never the folder. It doubles as the executable test of self-containment: if re-reading the folder does not reproduce the state the files claim, that gap is the defect, and you report it (S6) rather than papering over it from memory. After re-deriving, update your `지금 상태` and wait — do not resume research work. After acting, clear the box's **contents only** (the fence and the fixed sections are structure — never delete them) and leave a line in `최근 완료`; instructions that change no artifact ("review this", "understand the new logic") still count as acted upon. Fixed sections: `지금 상태` · `지금 할 일 (사용자)` · `다음에 올 일` · `최근 완료` · `사용자 답변 칸`. Reviews and discussion with the user are always in Markdown, not CLI output.

Current position lives in the three `To_Do_*.md` files, `MILESTONES.md`, and `HANDOFF.md` — read them rather than trusting any summary here. Paper order is fixed by G9/D9: `HAETAE-FIA` completely, then `PCM-DFA`.
