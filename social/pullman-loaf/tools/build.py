import base64, os, sys
tpl  = open('post.tpl.html').read()
loaf = 'data:image/png;base64,' + base64.b64encode(open('loaf_halftone_q.png','rb').read()).decode()
out = (tpl.replace('__LOAF__', loaf)
          .replace('__MARKPATH__', open('mark_d_final.txt').read().strip())
          .replace('__MARKVB__', '121 218 787 563')
          .replace('/*__FONTS__*/', open('fonts/inline.css').read()))
open('ff-pullman-post.html','w').write(out)
print('html', os.path.getsize('ff-pullman-post.html')//1024, 'KB')
