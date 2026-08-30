import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
tpl   = open(os.path.join(HERE, 'bag.tpl.html')).read()
loaf  = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, '..', 'assets', 'loaf-cutout.png'), 'rb').read()).decode()
wheat = open(os.path.join(HERE, 'wheat.svg')).read()
fonts = (open(os.path.join(HERE, 'fonts', 'inline.css')).read() + '\n'
         + open(os.path.join(HERE, 'fonts', 'inline-bodoni.css')).read())
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'partanna-pullman-bag.html')

out = (tpl.replace('__LOAF__', loaf)
          .replace('__WHEAT_L__', wheat.replace('class="wheat"', 'class="wheat l"'))
          .replace('__WHEAT_R__', wheat.replace('class="wheat"', 'class="wheat r"'))
          .replace('/*__FONTS__*/', fonts))
open(OUT,'w').write(out)
print('bag html', os.path.getsize(OUT)//1024, 'KB')
