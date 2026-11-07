# background removal (rembg, isnet-general-use) -> src/cut/<code>.png, trimmed to the object
import sys, glob, os
from rembg import remove, new_session
from PIL import Image
sess = new_session('isnet-general-use')
for code in sys.argv[1:]:
    im = Image.open(f'src/p_{code}.jpg').convert('RGB')
    out = remove(im, session=sess, post_process_mask=True)
    out = out.crop(out.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox())
    out.save(f'src/cut/{code}.png'); print(code, out.size)
