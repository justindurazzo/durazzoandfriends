# F&F Pizzeria — "The best thing since sliced bread"

A social post for the Pullman loaf, drawn from 1920s–50s American newspaper
bread advertising (Old Home Jumbo, Holmes' Milk-Made, Wonder, Nissen's).

## Files

| File | What it is |
| --- | --- |
| `ff-pullman-post.png` | 1080 × 1350 — ready to post (Instagram portrait) |
| `ff-pullman-post@2x.png` | 2160 × 2700 — retina / print |
| `ff-pullman-post.html` | Self-contained source. Fonts, halftone and mark are all inlined; opens offline. |
| `assets/ff-mark.svg` | The F&F signature mark, vectorised. Reusable anywhere. |
| `assets/loaf-halftone.png` | The loaf as a 45° halftone screen, alpha only — tint it with CSS `mask-image`. |

## Design

Set as a two-colour letterpress job: press black `#211D18` and F&F navy
`#1B2A5E` on newsprint `#E7E0CC`. Type is Ultra (hero), Oswald (caps and
slabs), Pinyon Script (the connective word, echoing the signature mark) and
Libre Baskerville (column copy). The navy plate on "since" is deliberately
mis-registered by 3px, as a two-colour press would.

The mark was traced from the F&F profile mark; the loaf is the Pullman from
the F&F feed, screened at 45° so it reads as period newsprint.

## Re-rendering

Edit copy or layout in `tools/post.tpl.html`, then:

```sh
cd tools
python3 build.py   # inlines fonts + halftone + mark -> ff-pullman-post.html
python3 shot.py    # renders the PNG at 2x via headless Chromium
```

`tools/halftone.py LO HI GAMMA CELL FLATTEN` regenerates the halftone screen
from a source photo — lower `LO` for a darker loaf, smaller `CELL` for a
finer screen.

## Copy worth checking before it goes out

- "Pan-baked daily" — swap if the bake isn't every day.
- "Baked in house" — the oval callout.
- The two body paragraphs are written to the photo, not from a spec sheet.
