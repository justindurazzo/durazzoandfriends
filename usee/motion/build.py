"""Build motion.html from script.md.

Each spoken line gets a start time. If audio/durations.json exists (one entry per line, in seconds,
written by the voiceover step), real durations are used and the page plays vo.mp3; otherwise lines
are timed at a natural speaking pace so the visuals can be reviewed before the voice exists.
"""
import base64, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
fonts = Path(sys.argv[1])
GAP = 0.45            # breath between lines
WPS = 2.42            # words per second, about 145 wpm

script = (HERE.parent / "script.md").read_text().split("## Notes")[0]
sections, lines = [], []
for block in re.split(r"^## ", script, flags=re.M)[1:]:
    m = re.match(r"\[(\d\d)\] (.+)\n", block)
    sections.append({"id": m.group(1), "title": m.group(2), "first": len(lines)})
    for spk, text in re.findall(r"^([A-Z][A-Z ]*?\d?): (.+)$", block, flags=re.M):
        lines.append({"spk": spk, "text": text.strip(), "sec": m.group(1)})

dur_file = HERE.parent / "audio" / "durations.json"
durs = json.loads(dur_file.read_text()) if dur_file.exists() else None
t = 0.0
for i, l in enumerate(lines):
    l["t"] = round(t, 2)
    d = durs[i] if durs else len(l["text"].split()) / WPS
    # Captions show one sentence at a time, timed by its share of the line's characters.
    sents = [x for x in re.split(r'(?<=[.?!])\s+', l["text"]) if x]
    total_chars, acc, l["chunks"] = sum(len(x) for x in sents), 0, []
    for x in sents:
        l["chunks"].append({"t": round(t + d * acc / total_chars, 2), "text": x})
        acc += len(x)
    t += d + GAP
for s in sections:
    s["t"] = lines[s["first"]]["t"]
    del s["first"]
total = round(t + 1.5, 2)

def b64(name):
    return "data:font/woff2;base64," + base64.b64encode((fonts / name).read_bytes()).decode()

tl = {"total": total, "sections": sections, "lines": lines, "audio": "vo.mp3" if durs else None}
html = (HERE / "motion.src.html").read_text()
html = html.replace("__TIMELINE__", json.dumps(tl, ensure_ascii=False))
for key, name in {"__F_BRIC__": "bricolage-grotesque-latin-standard-normal.woff2",
                  "__F_ATK4__": "atkinson-hyperlegible-latin-400-normal.woff2",
                  "__F_ATK7__": "atkinson-hyperlegible-latin-700-normal.woff2",
                  "__F_ATKI__": "atkinson-hyperlegible-latin-400-italic.woff2",
                  "__F_MONO__": "atkinson-hyperlegible-mono-latin-500-normal.woff2"}.items():
    html = html.replace(key, b64(name))
(HERE / "motion.html").write_text(html)
print(f"{len(lines)} lines, {total/60:.1f} min, audio={'yes' if durs else 'no'}")
for s in sections:
    print(s["id"], f'{int(s["t"]//60)}:{int(s["t"]%60):02d}', s["title"])
