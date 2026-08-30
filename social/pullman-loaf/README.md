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
| `assets/pullman-photo.png` | The source photograph of the baked loaf. |
| `assets/loaf-plate.png` | The regraded illustration plate the screen is made from. |
| `assets/loaf-halftone.png` | The loaf as a 45° halftone screen, alpha only — tint with CSS `mask-image`. |
| `assets/loaf-halftone-dense.png` | A denser screen. Blue ink carries less optical weight than black, so the one-colour version uses this. |

## Design

Type is Ultra (hero), Oswald (caps and slabs), Pinyon Script (the connective
word, echoing the script mark) and Libre Baskerville (column copy). In the
two-colour version the blue plate on "since" is deliberately mis-registered by
3px, as a two-colour press would; in the one-colour version that becomes a
light tint of the single ink, reading as ink spread rather than mis-register.

## The loaf

The loaf is the actual baked Pullman (`assets/pullman-photo.png`), keyed off
the cutting board and screened at 45° so it reads as period newsprint.

Two things had to be built rather than photographed, both in `tools/loaf2_build.py`:

**The cut end.** The photograph is of an uncut loaf, so the end face is
constructed: the heel's interior is replaced with a generated crumb, inset to
leave a crust rim, and lit by the photograph's own light field so it sits in
the same light. The crumb is deliberately fine and even — a pain de mie, not
the open crumb of the rustic loaf that was here before. At an 11px screen a
1–3mm alveolus is smaller than one halftone cell, so the crumb reads as
subtle tone rather than visible holes. That is what a sandwich loaf actually
looked like in period newsprint.

**The tonal grade.** In the photograph the lit plane is the brown top crust
and the shaded plane is the pale end. Strip the colour for a one-ink screen
and those two swap roles, collapsing the loaf into a single dark slab. So
each plane is regraded to its own tone — dark top crust, mid crust rim, light
cut face — with the photograph's texture laid back over it, and the crust
modelled lighter as it recedes. The crust rim is also widened past life size:
a 4mm rim is sub-screen at final size and would simply vanish. All of this is
ordinary engraver's practice for one-colour reproduction.

## Re-rendering

Edit copy or layout in `tools/post.tpl.html` — one template drives both
colourways; the palettes live in `tools/build.py`.

```sh
cd tools
python3 build.py duo  ../ff-pullman-post.html
python3 build.py blue ../ff-pullman-post-blue.html
python3 shot.py ../ff-pullman-post.html out@2x.png preview.png
```

`loaf2_build.py` rebuilds the cutout, the cut face and the tonal plate from
the source photograph. `halftone2.py LO HI GAMMA CELL FLATTEN` then screens it
— lower `LO` for a denser loaf, smaller `CELL` for a finer screen; it reads
`HT_SRC`, `HT_MSK` and `HT_OUT` from the environment.

## Copy worth checking before it goes out

- "Pan-baked daily" — swap if the bake isn't every day.
- "Baked in house" — the oval callout.
- The body copy and the spec list describe this loaf: close tender crumb,
  crackling top crust. They are written to the photograph, not a spec sheet.
- The cut face is constructed, not photographed. If you send a photo of the
  loaf actually cut, it drops straight in and the construction comes out.
