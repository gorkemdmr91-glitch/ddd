#!/usr/bin/env python3
"""Mistanbul tadım röportajı kapak görseli üretici (4:5 — 1080x1350).

Ölçüler referans kapaklardan (544x736 panel) çıkarılıp 1080x1350'ye ölçeklendi.
Metin bloğu ALTTAN hizalanır, böylece alıntı uzadıkça yukarı doğru büyür.
"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_BYLINE = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

SOL = 100                    # sol kenar boşluğu
ETIKET_PUNTO = 30            # "TADIM"
ETIKET_ARALIK = 8            # harf aralığı
CIZGI_KALINLIK = 6
CIZGI_GENISLIK = 91
ALINTI_PUNTO = 87
SATIR_ADIM = 97
BYLINE_PUNTO = 34
SIGDIR_GENISLIK = 940        # alıntı satırı bu genişliği aşarsa punto kısılır

# alttan uzaklıklar (referanstan ölçüldü, x1.985)
ALINTI_SON_ALT = 302         # SON alıntı satırının üst kenarının alttan uzaklığı
ETIKET_BOSLUK = 103          # "TADIM" ile 1. alıntı satırı arası
BYLINE_ALT = 181             # byline üst kenarı
# Blok ALTTAN sabit: alıntı uzadıkça yukarı doğru büyür, byline'a taşmaz.

AMBER = (245, 175, 14)
BEYAZ = (255, 255, 255)
GRI = (214, 200, 197)

GRADYAN_BAS = 0.42           # kararma nerede başlasın (yükseklik oranı)
GRADYAN_BIT = 0.78           # nerede tam koyuluğa ulaşsın
GRADYAN_MAX = 0.93           # en koyu nokta


def kare_al(video, saniye, cikti, kirpma_y=420):
    """Videodan 1080x1920 kare al, 4:5'e kırp."""
    subprocess.run([
        "ffmpeg", "-v", "error", "-ss", str(saniye), "-i", video,
        "-map", "0:v:0", "-frames:v", "1",
        "-vf", f"crop=1080:{H}:0:{kirpma_y}",
        "-y", cikti,
    ], check=True)


def gradyan_uygula(im):
    g = Image.new("L", (1, H))
    for y in range(H):
        t = (y / H - GRADYAN_BAS) / (GRADYAN_BIT - GRADYAN_BAS)
        t = max(0.0, min(1.0, t))
        t = t * t * (3 - 2 * t)                      # yumuşak geçiş
        g.putpixel((0, y), int(255 * GRADYAN_MAX * t))
    maske = g.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, maske)


def aralikli_yaz(d, xy, metin, font, renk, aralik):
    x, y = xy
    for ch in metin:
        d.text((x, y), ch, font=font, fill=renk)
        x += d.textlength(ch, font=font) + aralik
    return x - aralik


def kapak(kare_yolu, satirlar, vurgu_satir, byline, cikti):
    """satirlar: alıntı satırları (« » dahil). vurgu_satir: amber olacak satır indeksi."""
    im = Image.open(kare_yolu).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    im = gradyan_uygula(im)
    d = ImageDraw.Draw(im)

    f_etiket = ImageFont.truetype(FONT, ETIKET_PUNTO)
    f_byline = ImageFont.truetype(FONT_BYLINE, BYLINE_PUNTO)

    # alıntı kareye sığmazsa puntoyu kıs (uzun alıntılarda taşmayı önler)
    punto, adim = ALINTI_PUNTO, SATIR_ADIM
    f_alinti = ImageFont.truetype(FONT, punto)
    en_genis = max(d.textlength(s, font=f_alinti) for s in satirlar)
    if en_genis > SIGDIR_GENISLIK:
        oran = SIGDIR_GENISLIK / en_genis
        punto = int(punto * oran)
        adim = int(adim * oran)
        f_alinti = ImageFont.truetype(FONT, punto)
        print(f"   (alıntı {ALINTI_PUNTO} -> {punto} puntoya kısıldı)")

    # blok alttan hizalanır: önce 1. satırın y'si bulunur
    ilk_y = H - ALINTI_SON_ALT - (len(satirlar) - 1) * adim

    # TADIM etiketi + altındaki çizgi
    y = ilk_y - ETIKET_BOSLUK
    aralikli_yaz(d, (SOL, y), "TADIM", f_etiket, AMBER, ETIKET_ARALIK)
    cy = y + ETIKET_PUNTO + 8
    d.rectangle([SOL, cy, SOL + CIZGI_GENISLIK, cy + CIZGI_KALINLIK - 1], fill=AMBER)

    # alıntı — son satır(lar) amber
    y = ilk_y
    for i, s in enumerate(satirlar):
        d.text((SOL, y), s, font=f_alinti,
               fill=AMBER if i >= vurgu_satir else BEYAZ)
        y += adim

    # byline
    d.text((SOL, H - BYLINE_ALT), byline, font=f_byline, fill=GRI)

    im.save(cikti, quality=95)
    print(f"{cikti}  ({im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    import json
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    for k in cfg:
        kare_al(k["video"], k["saniye"], k["kare"], k.get("kirpma_y", 420))
        kapak(k["kare"], k["satirlar"], k["vurgu_satir"], k["byline"], k["cikti"])
