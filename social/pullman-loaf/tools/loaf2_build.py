from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage as ndi

rng = np.random.default_rng(11)
a = np.array(Image.open('loaf2_src.png').convert('RGB')).astype(float)
R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
lum = a.mean(2); h,w = lum.shape
k=9; m9 = ndi.uniform_filter(lum,k)
sd = np.sqrt(np.maximum(ndi.uniform_filter(lum**2,k)-m9**2,0))
key = ~(((lum>130)&(sd<5)) | ((np.abs(R-B)<12)&(lum>118)&(sd<6)) | ((B>R+4)&(sd<8)))

poly = [(.32,0),(1,0),(1,.115),(.903,.15),(.874,.30),(.814,.45),(.754,.60),
        (.726,.72),(.716,.815),(.65,.842),(.55,.842),(.40,.812),(.25,.772),
        (.10,.731),(0,.706),(0,.26)]
pm = Image.new('L',(w,h),0); ImageDraw.Draw(pm).polygon([(x*w,y*h) for x,y in poly], fill=255)
loaf = key & (np.array(pm)>128)
loaf = ndi.binary_opening(loaf, np.ones((5,5)))
loaf = ndi.binary_closing(loaf, np.ones((25,25)))
lab,n = ndi.label(loaf); sizes = ndi.sum(loaf,lab,range(1,n+1))
loaf = ndi.binary_fill_holes(lab == (np.argmax(sizes)+1))
Image.fromarray((loaf*255).astype(np.uint8)).save('loaf2_mask.png')

yy,xx = np.mgrid[0:h,0:w]; fx, fy = xx/w, yy/h
crust_line = .285 + (fx - .015) * (.470-.285)/(.735-.015)
below = loaf & (fy > crust_line)
face  = ndi.binary_erosion(below, np.ones((3,3)), iterations=13)  # inset ~38px: a 4mm crust rim
                                                                 # is sub-screen at final size, so
                                                                 # the engraver's answer is to widen it
rim   = below & ~face
top   = loaf & ~below                                             # the baked top crust
dist  = ndi.distance_transform_edt(face)

def fractal(scale):
    hs = int(np.ceil(h/scale))+2; ws = int(np.ceil(w/scale))+2
    g = rng.normal(0,1,(hs,ws))
    return ndi.zoom(g, (h/hs, w/ws), order=3)[:h,:w]

# --- crumb: a pain de mie is fine and even, so it stays a whisper, not holes ---
nz = 0.46*fractal(30) + 0.32*fractal(14) + 0.22*fractal(6.5)
nz = ndi.gaussian_filter(nz,(2.4,1.7))
lo,hi = np.percentile(nz,3), np.percentile(nz,97)
nz = np.clip((nz-lo)/(hi-lo),0,1)
hole = np.clip((.46-nz)/.46,0,1)**.85
crumb_t = 1.0 - 0.22*hole*(0.35+0.65*np.clip(dist/26.,0,1))

# --- the engraver's move: give each plane its own tone so the form reads in one ink ---
texture = np.clip(lum / np.maximum(ndi.gaussian_filter(lum, 22), 1.0), 0.55, 1.6)
light   = ndi.gaussian_filter(lum, 90)
light   = (light - light[loaf].mean()) / max(light[loaf].std(), 1)   # normalised form shading

base = np.zeros_like(lum)
u = np.clip(0.62*fx + 0.38*(1-fy), 0, 1)                # distance along the loaf, near -> far
u = (u - u[top].min()) / max(u[top].max() - u[top].min(), 1e-6)
base[top]  = 92 + 40*u[top] + 12*np.clip(light[top], -1.6, 1.6)   # top crust, receding lighter
base[rim]  = 126 +  9*np.clip(light[rim],  -1.6, 1.6)   # crust rim outlines the cut
base[face] = 203 +  8*np.clip(light[face], -1.6, 1.6)   # cut face: lightest plane
base = ndi.gaussian_filter(base*loaf, 2.5) / np.maximum(ndi.gaussian_filter(loaf.astype(float), 2.5), 1e-6)

expo = np.zeros_like(lum)
expo[top] = 1.05; expo[rim] = 0.60; expo[face] = 0.12
expo = ndi.gaussian_filter(expo*loaf, 2.5) / np.maximum(ndi.gaussian_filter(loaf.astype(float), 2.5), 1e-6)
plate = base * (texture ** expo)
plate = np.where(face, plate * crumb_t, plate)
plate = np.where(loaf, np.clip(plate, 0, 255), 255)
CROP = (0, int(.065*h), int(.930*w), int(.862*h))   # include the loaf's own right profile   # enough length that it reads as a loaf
Image.fromarray(plate.astype(np.uint8)).convert('RGB').crop(CROP).save('loaf2_plate.png')
Image.fromarray((loaf*255).astype(np.uint8)).crop(CROP).save('loaf2_mask.png')
print('crop', CROP, '->', (CROP[2]-CROP[0], CROP[3]-CROP[1]))

for nm, msk in (('top',top), ('rim',rim), ('face',face)):
    print('%-5s %6.0fk px  mean tone %3.0f' % (nm, msk.sum()/1000, plate[msk].mean()))
