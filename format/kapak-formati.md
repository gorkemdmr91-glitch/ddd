# Kapak görseli formatı — tadım röportajları

Ölçü: **1080 × 1350 (4:5)**
Üretici: `format/uretim/kapak_yap.py` + `kapak_cfg.json`
Referans kapaklardan (Taylan / Halit / Barış) ölçülerek çıkarıldı.

---

## Yapı

Alttan yukarı doğru dört katman:

1. **Videodan kare** — 1080×1920 ham görüntüden 4:5 kırpılır, altyazısız
2. **Alt kararma** — yüksekliğin %42'sinden başlar, %78'de tam koyuluğa ulaşır
3. **TADIM etiketi** + altında kısa amber çizgi
4. **Alıntı** (son satır amber) ve **byline**

## Ölçüler (@1080×1350)

| Öğe | Değer |
|---|---|
| Sol kenar boşluğu | 100 px |
| TADIM | Inter ExtraBold 30, harf aralığı 8, amber |
| TADIM altı çizgi | 91 × 6 px, amber, etiketin 8 px altında |
| TADIM ↔ 1. alıntı satırı | 103 px |
| Alıntı | Inter ExtraBold 87 |
| Alıntı satır aralığı | 97 px |
| Son alıntı satırı, alttan | 302 px |
| Byline, alttan | 181 px |
| Byline | Inter SemiBold 34 |

**Blok alttan sabitlenir.** Alıntı iki satırdan uzunsa yukarı doğru büyür,
byline'ın üstüne taşmaz. Satır 940 px'i aşarsa punto otomatik kısılır.

## Renkler

| Öğe | Renk |
|---|---|
| TADIM + çizgi + vurgu satırı | `#F5AF0E` amber |
| Alıntı (vurgusuz satırlar) | `#FFFFFF` |
| Byline | `#D6C8C5` sıcak açık gri |

Amber, videodaki host chip rengiyle aynı — kapak ve video aynı sistemden
çıkıyor gibi okunuyor.

## Yazım kuralları

- Alıntı **« »** içinde (tırnak değil, guillemet)
- **Son satır amber.** Referansların üçünde de vurgu cümlenin sonunda:
  «…şiir gibi.» / «…bir daha gelirim.» / «…gerçekten enfes.»
  Bu yüzden alıntıyı, vurucu kelime sona gelecek şekilde seç.
- Alıntı **birebir** olmalı. Kısaltılabilir ama kelimeler değiştirilemez.
- Byline: `[İsim] Bey/Hanım — tadım misafirimiz`
- Emoji yok, ünlem yok.

## Kare seçimi

- Konuşan kişi net görünmeli, ağzı açık/jest halinde olmalı — donuk kare
  tıklanma oranını düşürür
- Kameranın önünden biri geçtiği anları ele: bu çekimde 44.6 ve 88–92 sn
  arası böyle
- Kırpma penceresi `kirpma_y` ile ayarlanır; 420 bu çekimde yüzleri üst
  üçte bire, metni masa bölgesine getiriyor

## Bu videoda seçilen

**C — «Bir tık daha üstünü / yapmaya çalışmışsın / ve başarmışsın.»**
Görkem Bey, kare 63.5 sn. Dosya: `mistanbul-gizem-gorkem-KAPAK.jpg`

Üç satırlı alıntı, punto 87'den 84'e otomatik kısıldı.

## Kullanım

```bash
python3 format/uretim/kapak_yap.py format/uretim/kapak_cfg.json
```

`kapak_cfg.json` içinde her kapak için: video yolu, saniye, kırpma,
alıntı satırları, hangi satırdan itibaren amber, byline, çıktı adı.
