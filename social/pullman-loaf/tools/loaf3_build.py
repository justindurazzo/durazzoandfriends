"""Cut the loaf out of the F&F post photograph and screen it.

This loaf is photographed already cut, so the crumb is real - nothing here is
constructed. The only work is keying it off the blue seamless.
"""
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage as ndi
import sys

shot = sys.argv[1] if len(sys.argv) > 1 else 'post_screenshot.png'
im = Image.open(shot).convert('RGB')
a0 = np.array(im).astype(int)
blue_rows = ((a0[:,:,2] - a0[:,:,0]) > 40).mean(1) > 0.25
rows = np.where(blue_rows)[0]
im = im.crop((0, rows.min(), im.width, rows.max()+1))     # the photo, minus IG chrome
im.save('loaf3_src.png')

a = np.array(im).astype(float)
R, B = a[:,:,0], a[:,:,2]
# the seamless stays blue even in shadow, so key on hue ratio rather than brightness
loaf = ((B - R) / (B + R + 1.0)) < 0.10
loaf = ndi.binary_opening(loaf, np.ones((3,3)))
lab, n = ndi.label(loaf)
sizes = ndi.sum(loaf, lab, range(1, n+1))
body = ndi.binary_fill_holes(lab == (np.argmax(sizes) + 1))
Image.fromarray((body*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)).save('loaf3_mask.png')
ys, xs = np.where(body)
print('photo %s  loaf bbox x %d-%d y %d-%d  aspect %.3f' % (
      im.size, xs.min(), xs.max(), ys.min(), ys.max(),
      (xs.max()-xs.min())/(ys.max()-ys.min())))
