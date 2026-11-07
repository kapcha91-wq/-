# Игровые рилсы для @mvtatv

Детские электромобили, квадроциклы, снегоходы. Вертикальное видео 1080×1920, 30 к/с.

Готово:
- `out/1_ugadaj-cenu_baggi.mp4`: «Угадай цену», 14,4 с, женский голос Piper «Ирина».
- `out/bez_ozvuchki/`: 20 игровых рилсов без звука (`01_…20_*.mp4`), музыку добавляют в Instagram. Исходники сцен 4–20 лежат в `s04_…s20_*.html`, общие части в `kit.css` и `kit.js`.
- `src/cut/`: товары без фона (rembg, `cutout.py`); `src/p_9166_diff.jpg`: фото для «Найди отличия» (`make_diff.py`).
- Пачка видео: `./render_queue.sh s06_naperstki.html:11:06_naperstki …` (страница:секунды:имя файла).
- `SCENES.md`: 20 сцен для пробных рилсов без озвучки.

Фото товаров: `python prep_photos.py <папка с фото> src` обрезает их до 4:3 и закрашивает ярлыки с кодами. Список товаров для страниц лежит в `products.js`.
Видео без звука: `./make_silent.sh stopkadr.html 10.2 out/bez_ozvuchki/1_stop-kadr.mp4`.

## Как пересобрать

```bash
# голос (нужна модель ru-irinia-medium.onnx из rhasspy/piper v0.0.2 и pip install piper-tts)
python tts.py vo_lines.json vo path/to/ru-irinia-medium.onnx
# кадры, звук, видео
node render.js ugaday.html fr_ugaday 14.4 30
python mix.py fr_ugaday/sfx.json sched_ugaday.json fr_ugaday/mix.wav
ffmpeg -framerate 30 -i fr_ugaday/%05d.jpg -i fr_ugaday/mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart out/1_ugadaj-cenu_baggi.mp4
```

- Каждый кадр строится функцией `seek(t)` в HTML, звуки страница отдаёт в `window.SFX`.
- Время фраз голоса задаётся в `sched_*.json`, звуковые эффекты синтезирует `sfx_lib.py`.
- Надписи держатся в пределах x 80–940 и y 230–1500, чтобы их не закрывали кнопки и подпись Instagram.
- Шрифт Unbounded (лицензия SIL OFL), фото товара `src/buggy.jpg` взято из рилса @mvtatv.
