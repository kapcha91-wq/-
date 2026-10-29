"""Карточки-инфографика для Авито из готовых рендеров и исходных фото (без нейросети)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = sys.argv[1]
SRC, FIN, OUT = f"{ROOT}/../assets/airwrap-hs08", f"{ROOT}/final", f"{ROOT}/final2"
W, H = 1500, 2000
PLUM, PLUM2, ROSE, CREAM = (42, 22, 44), (92, 48, 92), (238, 183, 196), (248, 241, 238)
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
def fin(n): return Image.open(f"{FIN}/avito-dyson-airwrap-hs08-{n:02d}.jpg").convert("RGB")
def raw(n): return Image.open(f"{ROOT}/raw/{n:02d}.jpg").convert("RGB")
def src(n): return Image.open(f"{SRC}/{n}").convert("RGB")

def gradient(top, bot, size=(W, H)):
    g = Image.new("RGB", size)
    d = ImageDraw.Draw(g)
    for y in range(size[1]):
        t = y / size[1]
        d.line([(0, y), (size[0], y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return g

def fit(im, w, h): return ImageOps.fit(im, (w, h), Image.LANCZOS)

def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, *im.size], r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, mask=m); return out

def header(d, title, sub=None, y=110, color="white", subcolor=None):
    tf = font("Bold", 92)
    while d.textlength(title, font=tf) > W - 200: tf = font("Bold", tf.size - 4)
    d.text((W // 2, y), title, font=tf, fill=color, anchor="mt")
    if sub: d.text((W // 2, y + tf.size + 30), sub, font=font("Medium", 46), fill=subcolor or ROSE, anchor="mt")

def bullets(d, items, x, y, gap=118, size=50, color="white", dot=ROSE):
    f = font("SemiBold", size)
    for it in items:
        d.ellipse([x, y + size * 0.32, x + 26, y + size * 0.32 + 26], fill=dot)
        d.text((x + 56, y), it, font=f, fill=color)
        y += gap

def grid(cells, cols, top, gap=24, margin=60, h=None, bg=None, labels=None):
    cw = (W - 2 * margin - gap * (cols - 1)) // cols
    ch = h or cw * 4 // 3
    for i, im in enumerate(cells):
        x = margin + (i % cols) * (cw + gap); y = top + (i // cols) * (ch + gap)
        tile = rounded(fit(im, cw, ch), 28)
        bg.paste(tile, (x, y), tile)
        if labels:
            d = ImageDraw.Draw(bg); f = font("Bold", 44)
            tw = d.textlength(labels[i], font=f)
            d.rounded_rectangle([x + 22, y + ch - 96, x + 22 + tw + 48, y + ch - 24], 34, fill=(255, 255, 255))
            d.text((x + 46, y + ch - 88), labels[i], font=f, fill=PLUM)
    return top + (len(cells) + cols - 1) // cols * (ch + gap)

cards = {}

# 21 Что в комплекте
c = gradient((24, 14, 26), (54, 28, 56)); d = ImageDraw.Draw(c)
header(d, "Что в комплекте", "Всё для любой укладки")
s = fit(src("set-purple-black.jpg"), 1300, 1300)
c.paste(rounded(s, 40), (100, 330), rounded(s, 40))
bullets(d, ["Стайлер Airwrap i.d. + конический ствол", "Диффузор и насадка для пушка",
            "Разглаживающая и круглая щётки", "Насадка-гребень · кейс для хранения"], 130, 1690, gap=74, size=44)
cards[21] = c

# 22 Характеристики
c = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(c)
header(d, "Dyson Airwrap i.d. HS08", "Мультистайлер и фен в одном", color=PLUM, subcolor=PLUM2)
s = src("set-purple-white.jpg").crop((0, 60, 800, 1140)); s = fit(s, 700, 945)
c.paste(s, (60, 420))
y = 470
for t, s2 in [("i.d. curl", "авто-завивка кнопкой"), ("Bluetooth", "настройки в приложении"), ("Эффект Коанда", "волосы сами накручиваются"),
              ("Бережно", "без экстремального нагрева"), ("4 в 1", "сушка, завивка, объём, гладкость")]:
    d.ellipse([800, y + 18, 826, y + 44], fill=PLUM2)
    d.text((850, y), t, font=font("Bold", 52), fill=PLUM)
    d.text((850, y + 66), s2, font=font("Medium", 36), fill=PLUM2)
    y += 190
cards[22] = c

# 23 Любые укладки (коллаж)
c = gradient((250, 236, 240), (232, 214, 232)); d = ImageDraw.Draw(c)
header(d, "Любая укладка дома", "Локоны · волны · объём · гладкость", color=PLUM, subcolor=PLUM2)
grid([raw(4), raw(16), raw(5), raw(17)], 2, 330, h=780, bg=c, labels=["Локоны", "Кудри", "Волны", "Гладкость"])
cards[23] = c

# 24 Как это работает
c = gradient((30, 16, 32), (70, 36, 72)); d = ImageDraw.Draw(c)
header(d, "Как это работает", "Три шага до укладки как из салона")
y = 330
for i, (im, t, s2) in enumerate([(raw(7), "Поднесите прядь", "воздух сам наматывает её"),
                                  (raw(4), "Нажмите i.d. curl", "стайлер всё сделает сам"),
                                  (raw(5), "Готово!", "блестящие стойкие локоны")]):
    tile = rounded(fit(im, 520, 500), 30); c.paste(tile, (90, y), tile)
    d.ellipse([650, y + 120, 770, y + 240], fill=ROSE)
    d.text((710, y + 180), str(i + 1), font=font("Bold", 70), fill=PLUM, anchor="mm")
    d.text((810, y + 130), t, font=font("Bold", 56), fill="white")
    d.text((810, y + 210), s2, font=font("Medium", 40), fill=(225, 205, 225))
    y += 540
cards[24] = c

# 25 Цвета
c = gradient((22, 14, 20), (46, 26, 40)); d = ImageDraw.Draw(c)
header(d, "Разные цвета", "Уточняйте наличие в сообщениях")
grid([raw(1), raw(13), raw(14), src("boxes-colors.jpg")], 2, 330, h=780, bg=c)
cards[25] = c

# 26 Реальный интерьер (исходник) + подпись
c = fit(src("lifestyle-purple.jpg"), W, H); d = ImageDraw.Draw(c)
ov = Image.new("RGBA", (W, 520), (30, 16, 32, 0)); od = ImageDraw.Draw(ov)
for yy in range(520): od.line([(0, yy), (W, yy)], fill=(30, 16, 32, int(220 * yy / 520)))
c.paste(ov, (0, H - 520), ov)
d.text((90, H - 300), "Стайлер, который заменит всё", font=font("Bold", 74), fill="white")
d.text((90, H - 190), "Фен, плойка, брашинг и выпрямитель", font=font("Medium", 46), fill=(240, 226, 236))
cards[26] = c

# 27 Коробки (исходник)
c = fit(src("boxes-colors.jpg"), W, H); d = ImageDraw.Draw(c)
c.paste(ov, (0, H - 520), ov)
d.text((90, H - 300), "Новые, в упаковке", font=font("Bold", 80), fill="white")
d.text((90, H - 190), "Выбор цветов · отправка по России", font=font("Medium", 46), fill=(240, 226, 236))
cards[27] = c

# 28 Оранжевый цвет (исходник)
c = gradient((255, 226, 206), (246, 196, 170)); d = ImageDraw.Draw(c)
header(d, "Яркий оранжевый", "Тот же HS08 в другом цвете", color=(90, 34, 16), subcolor=(150, 70, 40))
o = src("set-orange.jpg"); o = o.resize((int(o.width * 1530 / o.height), 1530), Image.LANCZOS)
sh = Image.new("RGB", o.size, (255, 255, 255))
c.paste(rounded(o, 30), ((W - o.width) // 2, 380), rounded(o, 30))
cards[28] = c

# 29 Подарок-коллаж
c = gradient((44, 20, 34), (96, 44, 72)); d = ImageDraw.Draw(c)
header(d, "Лучший подарок", "Для мамы, жены, сестры, подруги")
grid([raw(8), raw(20)], 2, 340, h=1150, bg=c)
bullets(d, ["Красивый кейс — можно дарить сразу", "Подойдёт для любого типа волос"], 120, 1640, gap=90, size=48)
cards[29] = c

# 30 Почему стоит купить
c = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(c)
header(d, "Почему HS08", "Новое поколение Airwrap", color=PLUM, subcolor=PLUM2)
tile = rounded(fit(raw(19), 1300, 900), 40); c.paste(tile, (100, 330), tile)
bullets(d, ["Кнопка i.d. curl: завивка в один клик", "Bluetooth: настройки под ваши волосы",
            "Насадки для прямых и волнистых волос", "Бережно: без экстремального нагрева",
            "Кейс для хранения в комплекте"], 110, 1310, gap=118, size=45, color=PLUM, dot=PLUM2)
cards[30] = c

os.makedirs(OUT, exist_ok=True)
for n, im in cards.items():
    im.convert("RGB").save(f"{OUT}/avito-dyson-airwrap-hs08-{n}.jpg", quality=92); print("ok", n)
