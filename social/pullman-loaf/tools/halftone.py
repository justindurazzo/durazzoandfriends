from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np, sys, os

W, SS = 1800, 3
CELL = float(sys.argv[4]) if len(sys.argv)>4 else 23.0
ANG = np.deg2rad(45)
LO, HI, GAM = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])

src  = Image.open('loaf_src.png')
mask = Image.open('loaf_mask_clean.png').convert('L')

gray = ImageOps.grayscale(src)
gray = gray.filter(ImageFilter.UnsharpMask(radius=6, percent=110, threshold=2))
g = np.array(gray).astype(float)
mk = np.array(mask) > 128
# homomorphic flatten: open the shadowed flank without losing local form
FLAT = float(sys.argv[5]) if len(sys.argv) > 5 else 0.55
base = np.array(gray.filter(ImageFilter.GaussianBlur(60))).astype(float)
fill = g[mk].mean()
base = np.where(mk, base, fill)
flat = np.clip(g / np.maximum(base, 1.0) * fill, 0, 255)
g = (1 - FLAT) * g + FLAT * flat
lo, hi = np.percentile(g[mk], 2), np.percentile(g[mk], 98)
g = (g - lo) / (hi - lo)                       # 0..1 luminance in loaf
g = np.clip(g, 0, 1)
g = LO + (HI - LO) * (g ** GAM)                # remap into a printable window
g = np.where(mk, g, 1.0)                       # paper outside the loaf

tone = Image.fromarray((np.clip(g,0,1)*255).astype(np.uint8))
h = int(W * tone.height / tone.width)
tone = tone.resize((W, h), Image.LANCZOS)
t = np.array(tone).astype(float)/255.0

out = Image.new('L', (W*SS, h*SS), 0); d = ImageDraw.Draw(out)
R = np.hypot(W, h); rmax = CELL*0.60; n=0
for j in range(int(-R/CELL), int(R/CELL)+1):
    for i in range(int(-R/CELL), int(R/CELL)+1):
        u, v = i*CELL, j*CELL
        x = u*np.cos(ANG)-v*np.sin(ANG)+W/2
        y = u*np.sin(ANG)+v*np.cos(ANG)+h/2
        if not (-CELL<=x<W+CELL and -CELL<=y<h+CELL): continue
        xi, yi = int(min(max(x,0),W-1)), int(min(max(y,0),h-1))
        k = int(CELL*0.35)
        p = t[max(0,yi-k):yi+k+1, max(0,xi-k):xi+k+1]
        ink = 1.0 - (p.mean() if p.size else 1.0)
        if ink <= 0.02: continue
        r = rmax*(ink**0.5)
        d.ellipse([(x-r)*SS,(y-r)*SS,(x+r)*SS,(y+r)*SS], fill=255); n+=1
out = out.resize((W,h), Image.LANCZOS)
a = np.array(out); ys,xs = np.where(a>10)
box = (max(0,xs.min()-16), max(0,ys.min()-16), min(W,xs.max()+16), min(h,ys.max()+16))
rgba = Image.merge('RGBA', [Image.new('L', out.size, 0)]*3+[out]).crop(box)
rgba.save('loaf_halftone.png', optimize=True)
bg = Image.new('RGB', rgba.size, '#EDE4D0'); bg.paste(Image.new('RGB',rgba.size,'#1B2A5E'),(0,0),rgba)
bg.resize((rgba.width//3, rgba.height//3)).save('halftone_preview.png')
print('dots',n,'size',rgba.size,'bytes',os.path.getsize('loaf_halftone.png'),'mean ink',round(1-t[t<1].mean(),3))
