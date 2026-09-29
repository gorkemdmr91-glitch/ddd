# Üretim hattı — röportaj videosundan Mistanbul formatına

Bir sonraki videoda bu hattı aynen tekrar çalıştır. Tüm adımlar test edildi.

## Kurulum (container sıfırlanmışsa)

```bash
pip install yt-dlp gdown faster-whisper pillow numpy
apt-get update && apt-get install -y ffmpeg fonts-montserrat
```

## Adımlar

**1. Ham dosyayı indir**

```bash
gdown "https://drive.google.com/uc?id=<DOSYA_ID>" -O ham.mp4
```

Drive klasörü paylaşıma açık olmalı ("bağlantıya sahip olan herkes").
Klasör HTML'inden dosya ID'si: `grep -oE '"1[A-Za-z0-9_-]{27,44}"' klasor.html`

**2. Sesi çıkar ve transkript al**

```bash
ffmpeg -i ham.mp4 -map 0:a:0 -ac 1 -ar 16000 -c:a pcm_s16le ses.wav
python3 asr.py          # -> transkript.json (kelime zaman damgalı)
```

`asr.py` içindeki `initial_prompt` marka ve kişi adlarını içerir — yeni
isimler için güncelle, doğruluğu ciddi artırıyor. 4 çekirdekte ~100 sn'lik
ses için 3-5 dakika sürer.

**3. Kesim noktalarını ve düzeltmeleri gir**

`duzelt.py` içinde:
- `TRIM_START` / `TRIM_END` — kesim noktaları (ham zaman ekseninde)
- `DUZELTME` — transkript hataları: `(zaman, eski_kelime, yeni_kelime)`

```bash
python3 duzelt.py       # -> transkript_fix.json (kesilmiş + kaydırılmış)
```

**4. Konuşmacıları ata**

`konusmacilar.json` — kesim sonrası zaman ekseninde aralıklar:

```json
[{"start": 0, "end": 16.79, "who": "host"},
 {"start": 16.79, "end": 42.45, "who": "misafir1"}]
```

`who` değerleri: `host`, `misafir1`, `misafir2`.
Etiket adları ve renkler `make_ass.py` içindeki `SPEAKERS` sözlüğünde.

Kim konuşuyor bilmiyorsan o saniyeden kare çıkar, mikrofon kimde bak:

```bash
ffmpeg -ss 62 -i ham.mp4 -frames:v 1 kontrol.png
```

**5. Altyazıyı üret**

```bash
python3 make_ass.py transkript_fix.json konusmacilar.json altyazi.ass
```

Otomatik yapar: cümle bazlı ekran bölme, 2 satıra dengeli sarma,
kelime kelime karaoke vurgusu, konuşmacı etiketleri.

**6. Render**

```bash
bash render.sh
```

`render.sh` içindeki `-ss` / `-t` değerlerini `duzelt.py`'deki kesimle
aynı tut. Ses ölçümü + normalizasyon (−14 LUFS) otomatik.

## Ayar noktaları

`make_ass.py` başındaki sabitler:

| Sabit | Varsayılan | Etki |
|---|---|---|
| `SIZE` | 63 | Altyazı puntosu (1080 genişlik için) |
| `MAX_LINE_PX` | 880 | Satır genişlik sınırı |
| `MAX_WORDS` | 7 | Ekran başına kelime üst sınırı |
| `MAX_GAP` | 0.65 | Bu kadar sessizlikten sonra yeni ekran |

## Bilinen sınırlar

- **Konuşmacı ayrımı otomatik değil.** Whisper diarization yapmıyor;
  `konusmacilar.json` elle doldurulur. Üst üste binen konuşmalarda
  görüntüden doğrulamak gerekir.
- **Köşe yuvarlatma yok.** libass desteklemiyor. Birebir referans görünümü
  için CapCut gerekir; fark sadece altyazı kutularının köşelerinde.
- **Türkçe ASR hataları** özel isimlerde ve kalabalık ortam sesinde artıyor.
  Üretilen transkripti her seferinde gözden geçir.
