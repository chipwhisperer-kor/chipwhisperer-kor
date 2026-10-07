"""문체 검사기. 사람이 읽는 글에서 저장소 문체 규칙(GLOSSARY.md §1.4)에 어긋나는 표현을 센다.

사용법
    python3 style_check.py                # git 추적 파일 전체(벤더 트리 제외)
    python3 style_check.py README.md "workspace/1. SCA and FA/1.0.SCA_main.ipynb"

검사 범위는 산문 영역이다. Markdown은 코드 블록을 뺀 본문, 노트북은 Markdown 셀과
코드 셀의 한국어가 든 줄(주석·docstring·메시지), 파이썬은 주석·문자열, C·Verilog는 주석,
그 밖의 파일(YAML·셸·Tcl·Makefile·Dockerfile)은 파일 전체를 본다.

세는 항목은 다섯 가지다. em-dash(—), 합니다체 종결, 이모지, 굵은 라벨 불릿
(`- **라벨** —` 또는 `- **라벨**:`), 그리고 GLOSSARY.md §1.4의 어휘 대응표에 있는
쓰지 않는 단어다. 출력은 파일별로 몇 개가 잡혔는지와 그 합계이며, 판정은 하지 않는다. 남은 것이
의도한 보존인지(영문 정의 안의 "—", 표의 기호, 인용 출력)는 사람이 확인한다.

제외하는 것은 `workspace/base/`·`workspace/iut/`(벤더 원본), 생성 보고서
`[extra] Physical-AI-SCA/demo/*_Report.md`, `[extra] Physical-AI-SCA/runs/`이다.
이 스크립트 자신도 뺀다. 패턴 표에 쓰지 않는 단어가 그대로 적혀 있기 때문이다. 같은 이유로
`GLOSSARY.md`는 §1.4의 어휘 대응표에 적힌 만큼 잡힌다.
외부 의존성은 없고 표준 라이브러리만 쓴다. 파일을 수정하지 않는다.
"""
import collections
import json
import re
import subprocess
import sys

PATTERNS = {
    "emdash": r"—",
    "hapnida": r"(?<!아)(?:합니다|입니다|하세요|하십시오|됩니다|습니다|세요)",
    "emoji": r"[\U0001F300-\U0001FAFF☀-➿⭐✅❌]",
    "boldlabel": r"^\s*(?:[-*]|\d+\.)\s*\*\*[^*]+\*\*\s*[—:]",
    "vocab": (
        r"규약|정본|단일 진실|되읽|배관|사다리|벽돌|먹통|조용히|지어내|꾸며 넣|재노출|승격|"
        r"하네스|함정|장치다|되짚|셈이다|셈이| 꼴|못박|폭발|다음 사람|배선|핵심|"
        r"^즉,|\s즉,|^따라서|\s따라서|보장한|필수적|직관적|건수"
    ),
}
EXCLUDE = ("workspace/base/", "workspace/iut/", "/runs/", "_Report.md", "style_check.py")
EXTS = (".md", ".py", ".ipynb", ".c", ".h", ".v", ".sh", ".tcl", ".yaml", ".yml", ".txt")
HANGUL = re.compile("[가-힣]")


def prose(path, text):
    """파일 종류에 따라 산문 영역만 돌려준다."""
    if path.endswith(".ipynb"):
        parts = []
        for cell in json.loads(text)["cells"]:
            src = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                parts.append(re.sub(r"```.*?```", "", src, flags=re.S))
            else:
                parts.append("\n".join(l for l in src.split("\n") if HANGUL.search(l)))
        return "\n".join(parts)
    if path.endswith(".md"):
        return re.sub(r"```.*?```", "", text, flags=re.S)
    if path.endswith(".py"):
        comments = [l[l.index("#"):] for l in text.split("\n") if "#" in l]
        strings = re.findall(
            r'"""(.*?)"""|\'\'\'(.*?)\'\'\'|"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', text, flags=re.S)
        return "\n".join(comments + ["".join(s) for s in strings])
    if path.endswith((".c", ".h", ".v")):
        return "\n".join(re.findall(r"//.*|/\*.*?\*/|#.*", text, flags=re.S))
    return text


def default_files():
    out = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
    return [f for f in out
            if (f.endswith(EXTS) or f.endswith(("Dockerfile", "Makefile")))
            and not any(x in f for x in EXCLUDE)]


def main(files):
    total = collections.Counter()
    rows = []
    for f in files:
        try:
            text = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError) as e:
            print("SKIP", f, e)
            continue
        body = prose(f, text)
        row = {k: len(re.findall(p, body, flags=re.M)) for k, p in PATTERNS.items()}
        if any(row.values()):
            rows.append((f, row))
            total.update(row)
    for f, row in sorted(rows, key=lambda r: -sum(r[1].values())):
        print("  ".join(f"{k}={v}" for k, v in row.items() if v).ljust(60), f)
    print("TOTAL", dict(total))


if __name__ == "__main__":
    main(sys.argv[1:] or default_files())
