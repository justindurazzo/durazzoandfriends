from playwright.sync_api import sync_playwright
from PIL import Image
import os
p = os.getcwd() + '/ff-pullman-post.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                           args=['--no-sandbox','--disable-gpu'])
    pg = b.new_page(viewport={'width':1200,'height':1500}, device_scale_factor=2)
    pg.goto('file://' + p + '?export')
    pg.wait_for_timeout(900)
    box = pg.locator('#stage').bounding_box()
    print('stage box', {k: round(v,1) for k,v in box.items()})
    pg.locator('#stage').screenshot(path='ff-pullman-post.png')
    b.close()
im = Image.open('ff-pullman-post.png')
print('shot', im.size)
im.resize((im.width//3, im.height//3), Image.LANCZOS).save('post_preview.png')
