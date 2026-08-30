from playwright.sync_api import sync_playwright
from PIL import Image
import os, sys
src = sys.argv[1]; dst = sys.argv[2]; prev = sys.argv[3]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                           args=['--no-sandbox','--disable-gpu'])
    pg = b.new_page(viewport={'width':1200,'height':1500}, device_scale_factor=2)
    pg.goto('file://' + os.getcwd() + '/' + src + '?export')
    pg.wait_for_timeout(900)
    pg.locator('#stage').screenshot(path=dst)
    b.close()
im = Image.open(dst)
im.resize((im.width//3, im.height//3), Image.LANCZOS).save(prev)
print(dst, im.size)
