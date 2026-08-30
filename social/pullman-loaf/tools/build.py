import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

TITLES = {'duo': 'The Better White Bread', 'blue': 'Better White Bread in Blue'}

PALETTES = {
 # two-colour job: press black + F&F blue
 'duo': """    --paper:     #E7E0CC;   /* newsprint pulp                    */
    --paper-hi:  #F1EBDA;   --paper-hi-0: rgba(241,235,218,0);
    --paper-lo:  #D9D0B7;   --paper-lo-0: rgba(217,208,183,0);
    --ink:       #211D18;   /* warm press black                  */
    --ink-soft:  #4A423A;
    --brand:     #194887;   /* F&F blue, off the master artwork  */
    --ghost:     #8FA0C4;   /* blue plate, slipped on press      */
    --plate2:    var(--ink);
    --loaf-ink:  var(--ink);""",

 # one-colour job: F&F blue only, values carried by screens
 'blue': """    --paper:     #EAE5D5;   /* newsprint, nudged cooler for blue */
    --paper-hi:  #F4F0E2;   --paper-hi-0: rgba(244,240,226,0);
    --paper-lo:  #DBD4C0;   --paper-lo-0: rgba(219,212,192,0);
    --ink:       #194887;   /* the only ink on the press         */
    --ink-soft:  #41598C;
    --brand:     #194887;
    --ghost:     #9AAAC9;   /* a light tint of the same ink      */
    --plate2:    #7E92BC;
    --loaf-ink:  #194887;""",
}

variant = sys.argv[1] if len(sys.argv) > 1 else 'duo'
out_name = sys.argv[2] if len(sys.argv) > 2 else 'ff-pullman-post.html'

tpl  = open(os.path.join(HERE, 'post.tpl.html')).read()
# blue ink carries less optical weight than black, so it gets a denser screen
screen = os.path.join(HERE, '..', 'assets',
                      {'duo': 'loaf-halftone.png',        # black holds at a lighter screen
                       'blue': 'loaf-halftone-dense.png'  # blue needs the denser one
                       }[variant])
loaf = 'data:image/png;base64,' + base64.b64encode(open(screen,'rb').read()).decode()
out = (tpl.replace('__LOAF__', loaf)
          .replace('__MARKINNER__', open(os.path.join(HERE, 'mark_inner.txt')).read().strip())
          .replace('__TITLE__', TITLES[variant])
          .replace('/*__PALETTE__*/', PALETTES[variant])
          .replace('/*__FONTS__*/', open(os.path.join(HERE, 'fonts', 'inline.css')).read()))
open(out_name, 'w').write(out)
print(f'{variant:5s} -> {out_name}  {os.path.getsize(out_name)//1024} KB')
