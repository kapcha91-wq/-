"""Накладывает русские подписи на сгенерированные фото и сохраняет финал для Авито."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAW, OUT = sys.argv[1], sys.argv[2]
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)

CAPS = {
 "01": ("Dyson Airwrap i.d. HS08", "Мультистайлер · 6 насадок · кейс"),
 "02": ("Полный комплект", "Стайлер, 6 насадок и кейс для хранения"),
 "04": ("Волосы сами наматываются", "Эффект Коанда — завиток без зажимов"),
 "06": ("Кнопка i.d. curl", "Автоматическая завивка одним нажатием"),
 "07": ("Без экстремального нагрева", "Сушит и укладывает потоком воздуха"),
 "08": ("Подарок, который точно порадует", "Идеально к Новому году"),
 "12": ("Bluetooth + приложение", "Настройки под ваш тип волос"),
 "13": ("Выбор цветов", "Уточняйте наличие в сообщениях"),
 "15": ("Новые, в упаковке", "Разные цвета · отправка Авито Доставкой"),
 "16": ("Диффузор для кудрей", "Объём и чёткие локоны без пушения"),
 "17": ("Гладкость и блеск", "Круглая щётка для объёма в комплекте"),
 "19": ("Dyson Airwrap i.d.", "Сушка, завивка, объём, выпрямление"),
}
SPLIT = {"11": ("ДО", "ПОСЛЕ")}

def caption(im, title, sub):
    W, H = im.size
    band = int(H * 0.26)
    grad = Image.new("L", (1, band))
    for y in range(band): grad.putpixel((0, y), int(215 * (y / band) ** 1.4))
    shade = Image.new("RGB", (W, band), (26, 14, 30))
    im.paste(shade, (0, H - band), grad.resize((W, band)))
    d = ImageDraw.Draw(im)
    pad = int(W * 0.06)
    ts = int(W * 0.068)
    tf = font("Bold", ts)
    while d.textlength(title, font=tf) > W - 2 * pad: ts -= 2; tf = font("Bold", ts)
    sf = font("Medium", int(W * 0.036))
    sy = H - pad - sf.size
    ty = sy - int(ts * 1.25)
    acc = (238, 183, 196)
    d.rectangle([pad, ty - int(ts * 0.45), pad + int(W * 0.09), ty - int(ts * 0.45) + max(4, W // 250)], fill=acc)
    d.text((pad, ty), title, font=tf, fill="white")
    d.text((pad, sy), sub, font=sf, fill=(240, 226, 236))

def chips(im, left, right):
    W, H = im.size
    d = ImageDraw.Draw(im)
    f = font("Bold", int(W * 0.05))
    for txt, cx in ((left, W * 0.25), (right, W * 0.75)):
        tw = d.textlength(txt, font=f); ph, pv = W * 0.035, W * 0.018
        x0, y0 = cx - tw / 2 - ph, W * 0.05
        d.rounded_rectangle([x0, y0, x0 + tw + 2 * ph, y0 + f.size + 2 * pv], radius=int(W * 0.04),
                            fill=(255, 255, 255) if txt == left else (122, 58, 110))
        d.text((x0 + ph, y0 + pv - f.size * 0.08), txt, font=f, fill=(40, 30, 40) if txt == left else "white")

os.makedirs(OUT, exist_ok=True)
for fn in sorted(os.listdir(RAW)):
    k = fn[:2]
    im = Image.open(os.path.join(RAW, fn)).convert("RGB").resize((1500, 2000), Image.LANCZOS)
    if k in CAPS: caption(im, *CAPS[k])
    if k in SPLIT: chips(im, *SPLIT[k])
    im.save(os.path.join(OUT, f"avito-dyson-airwrap-hs08-{k}.jpg"), quality=92)
    print("ok", k)
