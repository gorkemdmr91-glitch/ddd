#!/usr/bin/env python3
"""transkript.json (kelime zamanlı) + konusmacilar.json -> Mistanbul formatında .ass

Kullanım: python3 make_ass.py transkript.json konusmacilar.json cikti.ass
"""
import json, sys
from PIL import ImageFont

W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

# DİKKAT: ASS'in Fontsize'ı FreeType/PIL puntosuyla aynı şey değil.
# libass aynı sayıda gözle görülür biçimde daha küçük basar.
# Bu yüzden iki ayrı değer tutuluyor:
#   OLCU_SIZE  -> satır sarma hesabı için PIL'e verilen punto
#   ASS_SIZE   -> .ass stil dosyasına yazılan Fontsize
# İkisi de referans render'ı ölçülerek eşitlendi (satır genişliği 594px @720).
OLCU_SIZE = 56
ASS_SIZE = 69

CHIP_SIZE = 44
CHIP_PAD = r"\h\h\h"   # chip yatay dolgusu
MAX_LINE_PX = 1000          # referans satır genişliği ~890px @1080
MAX_WORDS = 8              # ekran başına kelime üst sınırı
MAX_GAP = 0.65             # bu kadar sessizlikten sonra yeni ekran
MIN_CHUNK_DUR = 0.45

# Referansta altyazı bloğu YUKARIDAN sabit: ilk satır kaç satır olursa olsun
# hep aynı yerde duruyor, blok aşağı doğru büyüyor.
# Konumlandırma \pos ile yapılıyor, MarginV ile DEĞİL: libass üst üste binen
# altyazıları otomatik aşağı itiyor ve MarginV'yi eziyor. \pos bunu kapatır.
SATIR1_Y = 1223            # ilk satırın üst noktası @1080 (Alignment 8)
SATIR_ADIM = 88            # satır aralığı @1080 (referans: 55px @720)
CHIP_X, CHIP_Y = 72, 1162  # chip sol-üst @1080; alt kenarı altyazı kutusuna yapışık (boşluk 0)

SPEAKERS = {
    "host":    {"style": "ChipHost",    "hi": "&H0EAFF5&", "label": "Volkan Usta"},
    "misafir1":{"style": "ChipMisafir", "hi": "&H5A5FE7&", "label": "Gizem Hanım"},
    "misafir2":{"style": "ChipMisafir2","hi": "&H8B4FD6&", "label": "Görkem Bey"},
}

font = ImageFont.truetype(FONT, OLCU_SIZE)


def px(text):
    return font.getbbox(text)[2] - font.getbbox(text)[0]


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def who(t, spans, default="host"):
    for sp in spans:
        if sp["start"] <= t < sp["end"]:
            return sp["who"]
    return default


def chunk_words(words, spans):
    """Önce cümlelere böl (konuşmacı değişimi / cümle sonu / uzun sessizlik),
    sonra uzun cümleyi eşit parçalara ayır. Böylece tek kelimelik yetim ekran olmaz."""
    sentences, cur = [], []
    for w in words:
        if not cur:
            cur = [w]; continue
        gap = w["s"] - cur[-1]["e"]
        same_speaker = who(w["s"], spans) == who(cur[0]["s"], spans)
        if (not same_speaker) or cur[-1]["w"].endswith((".", "?", "!", "…")) \
                or gap > MAX_GAP:
            sentences.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur:
        sentences.append(cur)

    chunks = []
    for sent in sentences:
        n = len(sent)
        # kaç ekrana bölünmeli: kelime sayısı ve genişlik kısıtı
        parts = max(1, -(-n // MAX_WORDS))
        while parts < n and px(" ".join(x["w"] for x in sent)) / parts > MAX_LINE_PX * 2 * 0.92:
            parts += 1
        if parts == 1:
            chunks.append(sent); continue
        base, extra = divmod(n, parts)       # eşit dağıt, artanı baştan ver
        i = 0
        for k in range(parts):
            size = base + (1 if k < extra else 0)
            chunks.append(sent[i:i + size]); i += size
    return chunks


def wrap(words):
    """Kelimeleri en fazla 2 satıra, genişlik dengeli şekilde dağıt.
    Dönen: satır başına kelime indeks listesi."""
    texts = [w["w"] for w in words]
    if px(" ".join(texts)) <= MAX_LINE_PX:
        return [list(range(len(texts)))]
    best, best_cost = None, None
    for cut in range(1, len(texts)):
        a, b = " ".join(texts[:cut]), " ".join(texts[cut:])
        wa, wb = px(a), px(b)
        if wa > MAX_LINE_PX or wb > MAX_LINE_PX:
            continue
        cost = abs(wa - wb)
        if best_cost is None or cost < best_cost:
            best, best_cost = cut, cost
    if best is None:                       # sığmıyorsa en az taşan bölmeyi al
        best = len(texts) // 2
    return [list(range(best)), list(range(best, len(texts)))]


def render(words, hi_index, lines):
    """Ekranın her satırını ayrı üret; hi_index'teki kelime renkli.
    Dönen: satır metinleri listesi (her biri kendi Dialogue'u olacak)."""
    hi = SPEAKERS[words[0]["_who"]]["hi"]
    out = []
    for ln in lines:
        parts = []
        for i in ln:
            w = words[i]["w"]
            parts.append(f"{{\\c{hi}}}{w}{{\\c&HFFFFFF&}}" if i == hi_index else w)
        out.append(" ".join(parts))
    return out


def main(tr_path, sp_path, out_path):
    segs = json.load(open(tr_path, encoding="utf-8"))
    spans = json.load(open(sp_path, encoding="utf-8"))

    words = []
    for s in segs:
        for w in s.get("words", []):
            if w["w"].strip():
                words.append(dict(w))
    words.sort(key=lambda x: x["s"])
    for w in words:
        w["_who"] = who(w["s"], spans)

    header = open("ass_header.txt", encoding="utf-8").read()
    ev = []
    for ch in chunk_words(words, spans):
        lines = wrap(ch)
        start, end = ch[0]["s"], max(ch[-1]["e"], ch[0]["s"] + MIN_CHUNK_DUR)
        sp = SPEAKERS[ch[0]["_who"]]
        # \h = ASS sert boşluk; chip'in yatay dolgusunu büyütmek için
        etiket = CHIP_PAD + sp["label"] + CHIP_PAD
        ev.append(f"Dialogue: 0,{ts(start)},{ts(end)},{sp['style']},,0,0,0,,"
                  f"{{\\pos({CHIP_X},{CHIP_Y})}}{etiket}")
        for i, w in enumerate(ch):
            a = w["s"] if i else start
            b = ch[i + 1]["s"] if i + 1 < len(ch) else end
            if b - a < 0.05:
                b = a + 0.05
            # her satır kendi Dialogue'u: MarginV ile yukarıdan sabitlenir
            for j, satir in enumerate(render(ch, i, lines)):
                y = SATIR1_Y + j * SATIR_ADIM
                ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},Altyazi,,0,0,0,,"
                          f"{{\\pos(540,{y})}}{satir}")

    open(out_path, "w", encoding="utf-8").write(header + "\n".join(ev) + "\n")
    print(f"{out_path}: {len(words)} kelime, {len(ev)} dialogue satırı")


if __name__ == "__main__":
    main(*sys.argv[1:4])
