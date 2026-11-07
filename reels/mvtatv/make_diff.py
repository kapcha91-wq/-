# makes src/p_9166_diff.jpg: right headlight blue -> orange, gold stripes -> red, grille emblem removed
import cv2, numpy as np
im = cv2.imread('src/p_9166.jpg'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.int32)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
reg = np.zeros(H.shape, bool); reg[385:495, 420:665] = True
blue = reg & (H > 95) & (H < 135) & (S > 60)
hsv[..., 0] = np.where(blue, 12, H)                       # orange
reg2 = np.zeros(H.shape, bool); reg2[320:465, 665:1140] = True
gold = reg2 & (H > 10) & (H < 32) & (S > 40) & (V > 70)
hsv[..., 0] = np.where(gold, 176, hsv[..., 0]); hsv[..., 1] = np.where(gold, np.minimum(255, S + 90), hsv[..., 1])  # red
out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
m = np.zeros(H.shape, np.uint8); cv2.ellipse(m, (263, 467), (52, 40), 0, 0, 360, 255, -1)
# cover the emblem with a patch of grille bars from just right of it, feathered at the edges
patch = out[425:509, 322:432].copy(); dst = out[425:509, 208:318]
f = np.zeros(patch.shape[:2], np.float32); cv2.ellipse(f, (55, 42), (50, 38), 0, 0, 360, 1, -1); f = cv2.GaussianBlur(f, (0, 0), 6)[..., None]
out[425:509, 208:318] = (patch * f + dst * (1 - f)).astype(np.uint8)
cv2.imwrite('src/p_9166_diff.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 92]); print(blue.sum(), gold.sum())
