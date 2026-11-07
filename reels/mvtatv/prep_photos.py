# crops each product photo to 4:3, paints over the supplier's code labels / Chinese text, saves src/p_<code>.jpg (1200x900)
import cv2, numpy as np, sys, os
U = sys.argv[1]; OUT = sys.argv[2]
P = [  # code, upload id, crop (x0,y0,x1,y1), label rects to paint over
 ('9166', 'ccad94c1', (90, 0, 1511, 1066), []),
 ('L6',   '292765af', (135, 195, 935, 795), []),
 ('G63',  'bdf062e4', (160, 60, 1240, 870), [(1155, 45, 1475, 205)]),
 ('FT908','6203f05f', (26, 545, 826, 1145), [(540, 1115, 810, 1240)]),
 ('6666', 'df567726', (0, 100, 1280, 1060), [(95, 115, 405, 245)]),
 ('009',  '5cf92aae', (68, 0, 1201, 850), [(948, 62, 1188, 178)]),
 ('5688', '4eb82c24', (0, 200, 800, 800), []),
 ('800',  '4e49f882', (0, 107, 800, 707), [(584, 24, 746, 127)]),
 ('T08',  'f88550d2', (230, 50, 1250, 815), [(90, 70, 335, 215)]),
]
for code, uid, (x0, y0, x1, y1), rects in P:
    im = cv2.imread(f'{U}/{uid}-image.jpg')
    if rects:
        m = np.zeros(im.shape[:2], np.uint8)
        for a, b, c, d in rects: m[b:d, a:c] = 255
        im = cv2.inpaint(im, m, 12, cv2.INPAINT_TELEA)
        # soften the painted patch so it reads as out-of-focus background
        bl = cv2.GaussianBlur(im, (0, 0), 9); mm = cv2.GaussianBlur(m, (0, 0), 6)[..., None] / 255.0
        im = (im * (1 - mm) + bl * mm).astype(np.uint8)
    c = im[y0:y1, x0:x1]
    c = cv2.resize(c, (1200, 900), interpolation=cv2.INTER_LANCZOS4 if c.shape[1] < 1200 else cv2.INTER_AREA)
    if c.shape[1] < 1200: pass
    g = cv2.GaussianBlur(c, (0, 0), 1.2); c = cv2.addWeighted(c, 1.35, g, -0.35, 0)  # light sharpen
    cv2.imwrite(f'{OUT}/p_{code}.jpg', c, [cv2.IMWRITE_JPEG_QUALITY, 92]); print(code, c.shape)
# orange buggy from the earlier reel: 4:3 crop of src/buggy.jpg
b = cv2.imread(f'{OUT}/buggy.jpg'); b = b[70:602, 0:710]
cv2.imwrite(f'{OUT}/p_BUGGY.jpg', cv2.resize(b, (1200, 900), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_JPEG_QUALITY, 92])
