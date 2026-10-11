"""Build the reel thumbnails from two frames of the final video.

  thumbnail_reels_1080x1920.jpg  - Instagram Reels / YouTube Shorts cover (9:16)
  thumbnail_youtube_1280x720.jpg - YouTube / Facebook thumbnail (16:9)

Frames: frame_angry.png (0:14.0) and frame_boy.png (0:06.8), pulled with ffmpeg.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

TE = '/usr/share/fonts/truetype/noto/NotoSansTelugu-Bold.ttf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
YELLOW = (255, 214, 10)
WHITE = (255, 255, 255)
RED = (235, 40, 50)


def font(size):
    return ImageFont.truetype(TE, size, layout_engine=ImageFont.Layout.RAQM)


def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109, layout_engine=ImageFont.Layout.RAQM)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)


def text(img, xy, s, size, fill, stroke=10, anchor='mm', shadow=True):
    d = ImageDraw.Draw(img)
    f = font(size)
    if shadow:
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 10), s, font=f, fill=(0, 0, 0, 170), anchor=anchor,
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke)


def hide_sparkle(img, box):
    """Blur away the AI generator's sparkle watermark."""
    pad = 40
    x0, y0, x1, y1 = box
    big = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    reg = img.crop(big).filter(ImageFilter.GaussianBlur(16))
    m = Image.new('L', reg.size, 0)
    ImageDraw.Draw(m).ellipse([pad // 2, pad // 2, reg.width - pad // 2, reg.height - pad // 2], fill=255)
    img.paste(reg, big[:2], m.filter(ImageFilter.GaussianBlur(pad // 2)))


def vignette(img, strength=0.55):
    w, h = img.size
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).ellipse([-w * 0.25, -h * 0.15, w * 1.25, h * 1.15], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    dark = Image.new('RGBA', (w, h), (0, 0, 0, int(255 * strength)))
    img.paste(dark, (0, 0), Image.eval(m, lambda v: 255 - v))


def circle_inset(src, box, size, ring=12):
    ph = src.crop(box).resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    out = Image.new('RGBA', (size + ring * 2, size + ring * 2), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([0, 0, size + ring * 2 - 1, size + ring * 2 - 1], fill=WHITE)
    out.paste(ph, (ring, ring), m)
    return out


def drop_shadow(layer, img, at, blur=18, alpha=150):
    a = layer.getchannel('A').point(lambda v: v * alpha // 255)
    sh = Image.new('RGBA', layer.size, (0, 0, 0, 255)); sh.putalpha(a)
    pad = Image.new('RGBA', img.size, (0, 0, 0, 0)); pad.paste(sh, (at[0] + 8, at[1] + 14))
    img.alpha_composite(pad.filter(ImageFilter.GaussianBlur(blur)))
    img.alpha_composite(layer, at)


angry = Image.open('frame_angry.png').convert('RGBA')
boy = Image.open('frame_boy.png').convert('RGBA')

# ------------------------------------------------------------- 9:16 cover
# Instagram's profile grid shows only the centre 1080x1440 (y 240-1680), so all text stays inside it.
img = angry.copy()
hide_sparkle(img, (845, 1685, 955, 1795))
img = ImageEnhance.Contrast(img).enhance(1.08)
img = ImageEnhance.Color(img).enhance(1.12)
vignette(img, 0.5)
# darken the top so the title pops
top = Image.new('L', img.size, 0)
ImageDraw.Draw(top).rectangle([0, 0, 1080, 620], fill=200)
img.paste(Image.new('RGBA', img.size, (5, 8, 25, 255)), (0, 0), top.filter(ImageFilter.GaussianBlur(90)))

text(img, (540, 345), 'ఇంకో 5 నిమిషాలే!', 112, YELLOW, stroke=12)
b = text(img, (540, 488), 'అర్ధరాత్రి 12 అయింది!', 66, WHITE, stroke=9)
e = emoji('\U0001F621', 84)  # pouting face
img.alpha_composite(e, (b[2] + 6, 488 - e.height // 2 - 4))

# grinning boy inset, bottom-left, with a "VS" angry-phone reading
inset = circle_inset(boy, (180, 330, 900, 1050), 330)
drop_shadow(inset, img, (40, 1290))
e = emoji('\U0001F4F1', 90)  # mobile phone
img.alpha_composite(e, (300, 1270))

# bottom tag: series name
tag_font = font(54)
d = ImageDraw.Draw(img)
label = 'మాట్లాడే మొబైల్'
tb = d.textbbox((0, 0), label, font=tag_font)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
x1, y1 = 1040, 1610
x0, y0 = x1 - tw - 70, y1 - th - 46
d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=RED)
d.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=tag_font, fill=WHITE, anchor='mm')

img.convert('RGB').save('thumbnail_reels_1080x1920.jpg', quality=93)

# ------------------------------------------------------------- 16:9 YouTube
W, H = 1280, 720
yt = Image.new('RGBA', (W, H), (10, 12, 30, 255))
left = boy.crop((0, 260, 1080, 1868)).resize((484, 720), Image.LANCZOS)   # boy + phone, grinning
right = angry.crop((40, 420, 1080, 1965 - 420)).resize((W - 560, int((W - 560) * 1125 / 1040)), Image.LANCZOS)
right = right.crop((0, 70, right.width, 70 + H))
yt.paste(right, (560, 0))
# slanted split: boy panel with a white edge
mask = Image.new('L', (W, H), 0)
ImageDraw.Draw(mask).polygon([(0, 0), (640, 0), (540, H), (0, H)], fill=255)
lp = Image.new('RGBA', (W, H)); lp.paste(left.resize((640, 952)).crop((0, 140, 640, 860)), (0, 0))
yt.paste(lp, (0, 0), mask)
ImageDraw.Draw(yt).line([(640, 0), (540, H)], fill=WHITE, width=12)
hide_sparkle(yt, (1150, 600, 1270, 715))
yt = ImageEnhance.Color(yt).enhance(1.12)
vignette(yt, 0.35)
band = Image.new('L', (W, H), 0)
ImageDraw.Draw(band).rectangle([0, H - 230, W, H], fill=210)
yt.paste(Image.new('RGBA', (W, H), (5, 8, 25, 255)), (0, 0), band.filter(ImageFilter.GaussianBlur(60)))
text(yt, (W // 2, H - 135), 'ఇంకో 5 నిమిషాలే!', 104, YELLOW, stroke=11)
b = text(yt, (W // 2 - 30, H - 50), 'అర్ధరాత్రి 12 అయింది!', 52, WHITE, stroke=8)
e = emoji('\U0001F621', 62)
yt.alpha_composite(e, (b[2] + 6, H - 50 - e.height // 2 - 3))
e = emoji('\U0001F602', 80)  # tears of joy near the boy
yt.alpha_composite(e, (40, 40))
yt.convert('RGB').save('thumbnail_youtube_1280x720.jpg', quality=93)
print('done')
