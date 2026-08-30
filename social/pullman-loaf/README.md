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
| `tools/post.tpl.html` | The layout. One template drives both colourways. |
| `assets/ff-mark.svg` | The F&F script mark, from the master artwork. Fills with `currentColor`. |
| `assets/ff-script-logo.pdf` | The master logo file (navy / black / white artboards). |
| `assets/loaf-photo.png` | The source photograph — the loaf pictured in the posts. |
| `assets/loaf-halftone.png` | The loaf as a 45° halftone screen, alpha only — tint with CSS `mask-image`. |
| `assets/loaf-halftone-dense.png` | A denser screen. Blue ink carries less optical weight than black, so the one-colour version uses this. |
| `assets/pullman-uncut-photo.png` | The uncut loaf on the cutting board. Not used — kept for reference. |

## Design

One centred column: dateline, headline, the loaf, two lines of specifications,
the product slab, the signature. The only rules left are the dateline rule at
the top and the signature rule at the bottom - the loaf sits on open paper,
with nothing flanking it but the "Baked in House" oval.

Type is Ultra for the headline word, Pinyon Script for "Better" — which carries
the persuasion and echoes the script mark — and Italian Plate No1 Expanded for
every other line in the piece: dateline, oval, specifications, product slab and
signature. Expanded is a far wider face than the condensed Oswald it replaced,
so the tracking came down across the board; the sizes were set from measured
advance widths rather than by eye. In the
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

## The font, and why the HTML is not in this repo

Italian Plate No1 Expanded is a licensed retail family (Zetafonts). This repo
is public, and the build inlines the font as a base64 WOFF2 subset so the page
is self-contained — which means committing the built HTML would publish the
font file itself.

So the OTFs, their subsets, the generated `inline.css` and the two built HTML
files are all gitignored. The PNGs are the
deliverable and are committed; the HTML is a build output. To rebuild, drop the
family's OTFs into `tools/fonts/` first — `tools/build.py` subsets and inlines
them. Only the four weights the copy uses are needed: Regular, Medium,
Demibold, Bold.

The other four faces in the piece (Ultra, Pinyon Script, and previously Oswald
and Libre Baskerville) are SIL Open Font License families and carry no such
restriction.

## Re-rendering

Edit copy or layout in `tools/post.tpl.html` — one template drives both
colourways; the palettes and titles live in `tools/build.py`.

```sh
cd tools
python3 make_fonts.py                             # needs the OTFs in fonts/
python3 loaf3_build.py ../assets/loaf-photo.png   # cutout + mask
HT_SRC=loaf3_src.png HT_MSK=loaf3_mask.png HT_OUT=screen.png \
  python3 halftone2.py 0.24 1.00 0.90 11 0.72     # LO HI GAMMA CELL FLATTEN
python3 build.py duo  ../ff-pullman-post.html
python3 build.py blue ../ff-pullman-post-blue.html
python3 shot.py ../ff-pullman-post.html out@2x.png preview.png
```

`tools/fonts/ofl/` holds the two open-licensed faces (Ultra, Pinyon Script);
`make_fonts.py` combines them with the subset Italian Plate weights.

Lower `LO` for a denser loaf, smaller `CELL` for a finer screen, higher
`FLATTEN` to open the shadow side further.

## Copy worth checking before it goes out

The four specification lines are Justin's own words and are the only body copy
in the post:

    100% Italian semolina  <>  Naturally leavened
    Shaped by hand  <>  Baked fresh daily

paired onto two lines and split by the brand lozenge.

Only one line is not from him:

- "Baked in house" — the oval callout.

The earlier descriptive paragraphs and the "Cut it thick. Eat it warm." sign-off
were cut when the copy was reduced to these four lines. They are in git history
if either is wanted back.
