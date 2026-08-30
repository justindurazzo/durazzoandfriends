"""Build tools/fonts/inline.css, the font payload build.py inlines into the page.

Two sources:
  fonts/ofl/*.woff2   Ultra and Pinyon Script - SIL Open Font License, committed.
  fonts/*.otf         Italian Plate No1 Expanded - licensed retail family, NOT
                      committed. Drop the OTFs in fonts/ before rebuilding.

The OTFs are subset to the Latin range the copy uses, which takes each weight
from ~100KB to ~23KB.
"""
import base64, glob, os, re, subprocess, sys
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
SUBSET = ("U+0020-007E,U+00A0,U+00B7,U+2013,U+2014,U+2018,U+2019,"
          "U+201C,U+201D,U+2022,U+25C6")
IP_WEIGHTS = {'Regular': 400, 'Medium': 500, 'Demibold': 600, 'Bold': 700}


def face(family, weight, style, path):
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    return (f"@font-face {{\n  font-family: '{family}';\n"
            f"  font-style: {style};\n  font-weight: {weight};\n"
            f"  font-display: swap;\n"
            f"  src: url(data:font/woff2;base64,{b64}) format('woff2');\n}}")


blocks = []
for p in sorted(glob.glob(os.path.join(FONTS, 'ofl', '*.woff2'))):
    names = {r.nameID: str(r) for r in TTFont(p)['name'].names if r.platformID == 3}
    blocks.append(face(names.get(1), 400, 'normal', p))
    print('ofl      %-32s %s' % (names.get(1), os.path.getsize(p) // 1024))

found = 0
for name, weight in IP_WEIGHTS.items():
    otf = os.path.join(FONTS, f'ItalianPlateNo1Expanded-{name}.otf')
    if not os.path.exists(otf):
        continue
    woff = os.path.join(FONTS, f'IP-{name}.woff2')
    subprocess.run(['pyftsubset', otf, f'--unicodes={SUBSET}',
                    '--layout-features=*', '--flavor=woff2',
                    f'--output-file={woff}'], check=True)
    blocks.append(face('Italian Plate No1 Expanded', weight, 'normal', woff))
    print('licensed Italian Plate %-14s %3d KB -> %2d KB'
          % (name, os.path.getsize(otf) // 1024, os.path.getsize(woff) // 1024))
    found += 1

if not found:
    sys.exit('No ItalianPlateNo1Expanded-*.otf in tools/fonts/ - the copy will '
             'fall back to Helvetica. See the README.')

out = os.path.join(FONTS, 'inline.css')
open(out, 'w').write('\n'.join(blocks))
print('wrote', out, os.path.getsize(out) // 1024, 'KB')
