"""Build motion.html from script.md: time every sentence, embed fonts, inject the timeline."""
import base64, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
TOTAL = 720.0  # seconds, 12:00
fonts_dir = Path(sys.argv[1])

script = (HERE.parent / "script.md").read_text()
body = script.split("## Details")[0]
parts = re.split(r"^## \[(\d\d)\] (.+?) \(.*?\)\n", body, flags=re.M)

scenes = []
for i in range(1, len(parts), 3):
    text = parts[i + 2].replace("---", "")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    sents = []
    for p in paras:
        sents += [s.strip() for s in re.split(r'(?<=[.?!])\s+(?=[A-Z"])', p) if s.strip()]
    scenes.append({"id": parts[i], "title": parts[i + 1], "sentences": [{"text": s, "w": len(s.split())} for s in sents]})

total_words = sum(s["w"] for sc in scenes for s in sc["sentences"])
t = 0.0
for sc in scenes:
    words = sum(s["w"] for s in sc["sentences"])
    sc["t"] = round(t, 2)
    sc["dur"] = round(words / total_words * TOTAL, 2)
    st = t
    for s in sc["sentences"]:
        s["t"] = round(st, 2)
        st += s["w"] / words * sc["dur"]
        del s["w"]
    t += sc["dur"]

def b64(name):
    return "data:font/woff2;base64," + base64.b64encode((fonts_dir / name).read_bytes()).decode()

html = (HERE / "motion.src.html").read_text()
html = html.replace("__TIMELINE__", json.dumps({"total": TOTAL, "scenes": scenes}, ensure_ascii=False))
html = html.replace("__FONT_ARCHIVO__", b64("archivo-latin-standard-normal.woff2"))
html = html.replace("__FONT_NEWS__", b64("newsreader-latin-400-italic.woff2"))
html = html.replace("__FONT_MONO__", b64("jetbrains-mono-latin-500-normal.woff2"))
(HERE / "motion.html").write_text(html)
for sc in scenes:
    print(sc["id"], f'{int(sc["t"]//60)}:{int(sc["t"]%60):02d}', len(sc["sentences"]))
