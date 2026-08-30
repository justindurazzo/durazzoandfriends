import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'partanna-pullman-bag.html')

tpl   = open(os.path.join(HERE, 'bag.tpl.html')).read()
wheat = open(os.path.join(HERE, 'wheat.svg')).read()
mark  = open(os.path.join(HERE, 'partanna_mark.svg')).read()
fonts = (open(os.path.join(HERE, 'fonts', 'inline.css')).read() + '\n'
         + open(os.path.join(HERE, 'fonts', 'inline-bodoni.css')).read())

out = (tpl.replace('__PARTANNA__', mark)
          .replace('__WHEAT_L__', wheat.replace('class="wheat"', 'class="wheat l"'))
          .replace('__WHEAT_R__', wheat.replace('class="wheat"', 'class="wheat r"'))
          .replace('/*__FONTS__*/', fonts))
open(OUT, 'w').write(out)
print('bag html', os.path.getsize(OUT) // 1024, 'KB')
