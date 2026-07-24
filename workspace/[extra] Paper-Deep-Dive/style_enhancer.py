import re

with open("Presentation_Marp/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/presentation.md", "r", encoding="utf-8") as f:
    content = f.read()

# 1. '→ ' 로 시작하는 결론 문장을 takeaway 박스로 변경
def replace_arrow_with_takeaway(match):
    text = match.group(1).strip()
    return f'<div class="takeaway">\n\n{text}\n\n</div>\n'

# '→ '가 줄 맨 앞에 있거나 단락 첫 부분일 때 매칭
content = re.sub(r'^\s*→\s*(.+)$', replace_arrow_with_takeaway, content, flags=re.MULTILINE)

# 2. '결론:' 또는 '핵심:' 으로 시작하는 문장도 takeaway로 변경
def replace_keyword_with_takeaway(match):
    keyword = match.group(1)
    text = match.group(2).strip()
    return f'<div class="takeaway">\n\n<strong>{keyword}</strong> {text}\n\n</div>\n'

content = re.sub(r'^\s*(결론:|핵심:)\s*(.+)$', replace_keyword_with_takeaway, content, flags=re.MULTILINE)

# 3. 기존에 한 줄로 작성된 takeaway 박스를 여러 줄로 변경 (마크다운 렌더링 수정)
content = re.sub(r'<div class="takeaway">\s*(.*?)\s*</div>', r'<div class="takeaway">\n\n\1\n\n</div>', content)

# 4. 과도하게 빽빽한 슬라이드 (줄 수가 많은 슬라이드)에 <!-- _class: small --> 클래스 자동 삽입
slides = content.split('\n---\n')
for i, slide in enumerate(slides):
    if len(slide.split('\n')) > 18 and '<!-- _class:' not in slide and '# ' not in slide:
        slides[i] = '<!-- _class: small -->\n' + slide

content = '\n---\n'.join(slides)

with open("Presentation_Marp/양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법/presentation.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Agy style enhancements applied successfully.")
