# F&F Pizzeria — "The best thing since sliced bread"

A social post for the Pullman loaf, drawn from 1920s–50s American newspaper
bread advertising (Old Home Jumbo, Holmes' Milk-Made, Wonder, Nissen's).

Two colourways, same layout:

| | |
| --- | --- |
| **Two-colour** | Press black `#211D18` + F&F blue `#194887` on newsprint `#E7E0CC` |
| **One-colour** | F&F blue only, on a slightly cooler newsprint `#EAE5D5` — values carried by screens, the way a single-ink press run works |

## Files

| File | What it is |
| --- | --- |
| `ff-pullman-post.png` | Two-colour, 1080 × 1350 — ready to post |
| `ff-pullman-post@2x.png` | Two-colour, 2160 × 2700 — retina / print |
| `ff-pullman-post-blue.png` | One-colour blue, 1080 × 1350 |
| `ff-pullman-post-blue@2x.png` | One-colour blue, 2160 × 2700 |
| `ff-pullman-post*.html` | Self-contained sources. Fonts, halftone and mark all inlined; open offline. |
| `assets/ff-mark.svg` | The F&F script mark, from the master artwork. Fills with `currentColor`. |
| `assets/ff-script-logo.pdf` | The master logo file (navy / black / white artboards). |
| `assets/loaf-halftone.png` | The loaf as a 45° halftone screen, alpha only — tint with CSS `mask-image`. |
| `assets/loaf-halftone-dense.png` | A denser screen. Blue ink carries less optical weight than black, so the one-colour version uses this. |

## Design

Type is Ultra (hero), Oswald (caps and slabs), Pinyon Script (the connective
word, echoing the script mark) and Libre Baskerville (column copy). In the
two-colour version the blue plate on "since" is deliberately mis-registered by
3px, as a two-colour press would; in the one-colour version that becomes a
light tint of the single ink, reading as ink spread rather than mis-register.

The loaf is the Pullman from the F&F feed, keyed off its blue backdrop and
screened at 45° so it reads as period newsprint.

## Re-rendering

Edit copy or layout in `tools/post.tpl.html` — one template drives both
colourways; the palettes live in `tools/build.py`.

```sh
cd tools
python3 build.py duo  ../ff-pullman-post.html
python3 build.py blue ../ff-pullman-post-blue.html
python3 shot.py ../ff-pullman-post.html out@2x.png preview.png
```

`halftone.py LO HI GAMMA CELL FLATTEN` regenerates the screen from a source
photo — lower `LO` for a denser loaf, smaller `CELL` for a finer screen.

## Copy worth checking before it goes out

- "Pan-baked daily" — swap if the bake isn't every day.
- "Baked in house" — the oval callout.
- The two body paragraphs are written to the photo, not from a spec sheet.
