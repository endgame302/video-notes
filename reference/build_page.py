"""Build the P-Stack study notes page from the doc's Markdown export.

Usage: python build_page.py <doc.md> <quiz_key.txt> <img_src_dir> <out_dir>
"""
import html
import os
import re
import shutil
import sys

import markdown

doc_path, key_path, img_src, out_dir = sys.argv[1:5]
os.makedirs(os.path.join(out_dir, "img"), exist_ok=True)

IMAGES = [
    ("Jan's commits", "k01_commits"), ("P-Stack overview", "k02_overview"),
    ("The feature playbook", "k04_feature"), ("The principle-fix", "k05_fixroot"),
    ('"From goal', "k06_workflow"), ("Shortlist's Products", "k07_products"),
    ("Fetch Data", "k09_flow"), ("Decodo's four", "k10_endpoints"),
    ("Search result JSON", "k11_searchjson"), ("Decodo's CLI", "k12_cli"),
    ("The Decodo MCP", "k14_mcpjson"), ("pstack README", "k15_pstackinstall"),
    ("The default model", "k17_topology"), ("setup-pstack asking", "k16_setupq"),
    ("Jan's preferred", "k18_preferred"), ('"Verification enables', "k20_verifyloop"),
    ("The create-verification", "k21_createprompt"), ("How agents use", "k22_verifycmds"),
    ("Decodo's Target", "k24_templates"), ("The product bugs", "k25_bugs"),
    ("The proposed plan", "k29_plan2"), ('Decodo\'s "Get code"', "k30_codeexample"),
    ("Preview after", "k32_preview"), ("The mouse comparison", "k35_micerec"),
    ("The monitor comparison", "k36_monitorrec"), ("From the agent's handoff", "k33_proscons"),
]
DIAGRAMS = {"video map": "map", "how one prompt": "e2e", "model roles": "models", "comparison feature": "flow"}
PART_KIND = {"1": "pstack", "2": "web", "3": "ai", "4": "verify", "5": "result"}

src = html.unescape(open(doc_path, encoding="utf-8").read())

# Title and byline become the hero; the editor's thumbnail link becomes the hero's watch link.
src = re.sub(r"\A# .*?\n\n.*?\n", "", src, count=1)
src = re.sub(r"^\[\[image: YouTube thumbnail.*?\n", "", src, flags=re.M)


def image(m):
    alt = m.group(1)
    for prefix, name in IMAGES:
        if alt.startswith(prefix):
            shutil.copy(os.path.join(img_src, name + ".jpg"), os.path.join(out_dir, "img", name + ".jpg"))
            a = html.escape(alt, quote=True)
            return (f'\n<figure class="shot"><button class="zoom" type="button" aria-label="Enlarge screenshot">'
                    f'<img src="img/{name}.jpg" alt="{a}" loading="lazy"></button>'
                    f"<figcaption>{html.escape(alt)}</figcaption></figure>\n")
    raise SystemExit(f"no image for: {alt}")


def diagram(m):
    cap = m.group(1)
    for prefix, kind in DIAGRAMS.items():
        if cap.startswith(prefix):
            return f'\n<figure class="diagram" data-diagram="{kind}"></figure>\n'
    raise SystemExit(f"no diagram for: {cap}")


src = re.sub(r"\[image: (.*?)\\?\]", image, src)
src = re.sub(r"\[embedded content: (.*?)\\?\]", diagram, src)

# Answers from the independent quiz key, in the same order as the checklists.
answers = {}
for block in re.split(r"\n\s*\n", open(key_path, encoding="utf-8").read().strip()):
    m = re.match(r"(\d+)\.\s*\[([^\]]*)\]\s*(.*)", block.strip(), re.S)
    if m:
        answers[int(m.group(1))] = (m.group(2), " ".join(m.group(3).split()))

body = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists"])

# Part headings become colored banners; every h2/h3 gets an id for the contents list.
toc, used = [], set()


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<.*?>", "", text).lower()).strip("-")[:48] or "section"
    base, i = s, 2
    while s in used:
        s, i = f"{base}-{i}", i + 1
    used.add(s)
    return s


def heading(m):
    level, inner = m.group(1), m.group(2)
    plain = re.sub(r"<.*?>", "", inner)
    stamp = re.search(r'\(<a href="([^"]+)">([\d:]+)</a>\)\s*$', inner)
    title = re.sub(r'\s*\(<a href="[^"]+">[\d:]+</a>\)\s*$', "", inner)
    hid = slug(plain)
    badge = f'<a class="stamp" href="{stamp.group(1)}" target="_blank" rel="noopener">&#9654; {stamp.group(2)}</a>' if stamp else ""
    part = re.match(r"Part (\d): (.*)", re.sub(r"<.*?>", "", title))
    if level == "2":
        toc.append((2, hid, part.group(2) if part else re.sub(r"<.*?>", "", title), part.group(1) if part else None))
    elif not plain.startswith("Test yourself"):
        toc.append((3, hid, re.sub(r"<.*?>", "", title), None))
    if part:
        n, name = part.groups()
        return (f'<header class="part" id="{hid}" data-kind="{PART_KIND[n]}"><span class="part-no">Part {n}</span>'
                f"<h2>{name}</h2>{badge}</header>")
    cls = ' class="quiz-title"' if plain.startswith("Test yourself") else ""
    return f'<h{level} id="{hid}"{cls}>{title}{badge}</h{level}>'


body = re.sub(r"<h([23])>(.*?)</h\1>", heading, body)

# Blockquotes: the 30-second summaries and the lesson callouts.
body = re.sub(r"<blockquote>\s*<p><strong>In 30 seconds</strong></p>",
              '<aside class="tldr"><p class="tldr-label">In 30 seconds</p>', body)
body = re.sub(r'(<aside class="tldr">.*?)</blockquote>', r"\1</aside>", body, flags=re.S)
body = body.replace("<blockquote>", '<aside class="callout">').replace("</blockquote>", "</aside>")

# Checklists become self-test cards with a revealable answer.
qn = 0


def quiz_item(m):
    global qn
    qn += 1
    when, ans = answers.get(qn, ("", "Answer not found."))
    when = re.sub(r"\s*,\s*", ", ", when)
    return (f'<li class="q"><label><input type="checkbox" id="q{qn}" data-q="{qn}">'
            f'<span>{m.group(1)}</span></label>'
            f'<details><summary>Show answer</summary><p>{html.escape(ans)}</p>'
            f'<p class="when">From the video at {html.escape(when)}</p></details></li>')


body = re.sub(r"<li>\[ \] (.*?)</li>", quiz_item, body)
body = body.replace('<ul>\n<li class="q">', '<ul class="quiz">\n<li class="q">')
body = re.sub(r"<table>", '<div class="table-wrap"><table>', body).replace("</table>", "</table></div>")

toc_html = []
for level, hid, text, part in toc:
    if level == 2:
        dot = f'<span class="dot" data-kind="{PART_KIND[part]}"></span>' if part else '<span class="dot"></span>'
        label = f"Part {part}: {text}" if part else text
        toc_html.append(f'<li class="toc-h2"><a href="#{hid}">{dot}{html.escape(label)}</a></li>')
    else:
        toc_html.append(f'<li class="toc-h3"><a href="#{hid}">{html.escape(text)}</a></li>')

page = open(os.path.join(os.path.dirname(__file__), "page_template.html"), encoding="utf-8").read()
page = page.replace("{{TOC}}", "\n".join(toc_html)).replace("{{BODY}}", body).replace("{{QCOUNT}}", str(qn))
open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
print(f"built: {len(toc)} headings, {qn} questions, {len(os.listdir(os.path.join(out_dir, 'img')))} images")
