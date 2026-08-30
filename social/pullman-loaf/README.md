# F&F Pizzeria — "The Better White Bread"

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
| `assets/loaf-photo.png` | The source photograph — the loaf pictured in the posts. |
| `assets/loaf-halftone.png` | The loaf as a 45° halftone screen, alpha only — tint with CSS `mask-image`. |
| `assets/loaf-halftone-dense.png` | A denser screen. Blue ink carries less optical weight than black, so the one-colour version uses this. |
| `assets/pullman-uncut-photo.png` | The uncut loaf on the cutting board. Not used — kept for reference. |

## Design

One centred column: dateline, headline, the loaf, a four-line specification
panel, the product slab, the signature. No divider rules, nothing flanking the
loaf but the "Baked in House" oval.

Type is Ultra (hero), Oswald (caps, specs and slabs) and Pinyon Script, which
carries the persuading word — "Better" — and echoes the script mark. Libre
Baskerville is still loaded for body copy but the current cut has none. In the
two-colour version the blue plate on "Better" is deliberately mis-registered by
3px, as a two-colour press would; in the one-colour version that becomes a
light tint of the single ink, reading as ink spread rather than mis-register.

## The loaf

The loaf is photographed already cut, so the crumb in the posts is the real
crumb — nothing is constructed. The whole job is keying the loaf off the blue
seamless (`tools/loaf3_build.py`) and screening it at 45°.

The one real adjustment is shadow flattening. The photograph is lit hard from
the right, so the loaf's left flank falls to about a fifth of the brightness of
the cut face. In colour that reads as form; in a single-ink halftone it
collapses into a solid black mass and the loaf loses its shape. The screen
therefore runs a homomorphic flatten at 0.72, which opens the shaded flank
while keeping the local texture that makes the crust and crumb legible.

`tools/loaf2_build.py` is an earlier pipeline for the uncut cutting-board loaf,
which had to construct a cut face and regrade the loaf plane by plane. It is no
longer used — this photograph needs neither — but it is kept in case that loaf
comes back.

## Re-rendering

Edit copy or layout in `tools/post.tpl.html` — one template drives both
colourways; the palettes and titles live in `tools/build.py`.

```sh
cd tools
python3 loaf3_build.py ../assets/loaf-photo.png   # cutout + mask
HT_SRC=loaf3_src.png HT_MSK=loaf3_mask.png HT_OUT=screen.png \
  python3 halftone2.py 0.24 1.00 0.90 11 0.72     # LO HI GAMMA CELL FLATTEN
python3 build.py duo  ../ff-pullman-post.html
python3 build.py blue ../ff-pullman-post-blue.html
python3 shot.py ../ff-pullman-post.html out@2x.png preview.png
```

Lower `LO` for a denser loaf, smaller `CELL` for a finer screen, higher
`FLATTEN` to open the shadow side further.

## Copy worth checking before it goes out

The four specification lines are Justin's own words and are the only body copy
in the post:

    100% Italian semolina
    Naturally leavened
    Shaped by hand
    Baked fresh daily

Only one line is not from him:

- "Baked in house" — the oval callout.

The earlier descriptive paragraphs and the "Cut it thick. Eat it warm." sign-off
were cut when the copy was reduced to these four lines. They are in git history
if either is wanted back.
