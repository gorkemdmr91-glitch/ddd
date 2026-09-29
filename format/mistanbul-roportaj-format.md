# Mistanbul Döner — Müşteri Röportajı Video Formatı

Referans: `https://www.instagram.com/p/DdzXUrYCbqn/` (@mistanbul_doner, 27.09.2026)
Analiz tarihi: 29.09.2026 · Görsel referanslar: `format/reference/`

Bu dosya, yeni videoların aynı formatta kesilmesi için referanstır.
Yeni bir edit isteğinde önce bunu oku.

---

## 1. Teknik Spesifikasyon

| Parametre | Değer |
|---|---|
| Çözünürlük | 720 × 1280 (9:16) — export için 1080 × 1920 önerilir |
| FPS | 30 |
| Süre | 116.8 sn (~1:57) |
| Video codec | H.264, ~2.3 Mbps |
| Ses | AAC, 48 kHz, stereo |
| Ortalama ses seviyesi | −17.9 dBFS (peak −0.5 dB) |

## 2. Kurgu Yapısı — EN KRİTİK NOKTA

**Kesim yok. Sıfır.** Scene-change analizi 116 saniye boyunca 0.01–0.04
arası skor verdi (eşik 0.06'nın altı). Yani:

- Tek plan, kesintisiz çekim
- Sabit kamera, sabit çerçeve, zoom yok
- Jump cut yok, b-roll yok, stok görsel yok
- Geçiş efekti yok
- Intro kartı yok, outro kartı yok, logo bug'ı yok
- Arka plan müziği yok (140 Hz altı enerji −33 dB — sadece mekân sesi)

Tüm kurgu yükü **altyazıda**. Görüntü ham.

> Bu formatın işi bu: "kurgulanmamış, gerçek" hissi. Jump cut eklemek
> formatı bozar, samimiyeti düşürür. Ekleme.

## 3. Çerçeve ve Sahne

- İki kişilik medium-wide plan, yan yana bar taburesinde
- Mekân içi: duvarda harita tablosu, tezgâh, çay bardakları
- Sol: **Volkan Usta** (işletme sahibi, elinde mikrofon, soruyu soran)
- Sağ: **Misafir** (müşteri, cevap veren)
- Doğal ışık + mekân aydınlatması, renk düzeltme minimal/yok

## 4. Altyazı Sistemi (formatın imzası)

### Yerleşim (720 × 1280 referansında)

| Öğe | Konum |
|---|---|
| Konuşmacı etiketi (chip) | y ≈ 775–802 px (%60.5–62.7) |
| Altyazı satır 1 | y ≈ 822–856 px (%64.2–66.9) |
| Altyazı satır 2 | y ≈ 883–902 px (%69.0–70.5) |
| Satır aralığı | 61 px (≈1.45×) |
| Yatay hizalama | Metin bloğu **ortalı**; chip bloğun **sol kenarına** hizalı |
| Maksimum satır | 2 |

1080 × 1920'ye çevirmek için tüm px değerlerini **×1.5** yap.

### Tipografi

- Font: ağır geometrik sans — **Montserrat ExtraBold** (veya Poppins Bold /
  Gilroy ExtraBold). Türkçe karakter desteği şart: ğ ı İ ş ç ö ü
- Punto: ≈42 px @720w → **≈63 px @1080w**
- Renk: beyaz `#FFFFFF`
- Arka plan: siyah kutu, ~%75 opaklık, **yuvarlatılmış köşe** (~8 px),
  her satırın kendi kutusu var (blok değil, satır bazlı)
- Kutu içi padding: yatay ~14 px, dikey ~8 px @720w

### Kelime Vurgusu (karaoke)

Konuşulan kelime o an renklenir, sonra beyaza döner. **Sadece aktif kelime**
renklidir — sweep-and-stay değil.

### Konuşmacı Renk Kodu

| Konuşmacı | Chip rengi | Vurgu rengi | Chip yazı |
|---|---|---|---|
| Volkan Usta (host) | `#F5AF0E` amber | `#F5AF0E` | siyah |
| Misafir (ör. Taylan Bey) | `#E75F5A` mercan/kırmızı | `#E75F5A` | beyaz |

Chip: küçük punto (~22 px @720w), bold, yuvarlatılmış köşe, altyazının
hemen üstünde.

**Kural: her konuşmacıya sabit bir renk.** Host her videoda amber kalır.
Misafir rengi mercan kalır. Üçüncü konuşmacı girerse yeni renk ata.

### Segmentleme

- Ekran başına **4–7 kelime**
- Cümle ortasında bölmek serbest (doğal konuşma ritmi takip ediliyor)
- Noktalama korunuyor (virgül, nokta dahil)
- Segmentler arası yumuşak fade in/out

## 5. İçerik Akışı

| Bölüm | Süre | İçerik |
|---|---|---|
| Hook | 0–5 sn | Host selam + kampanya çerçevesi: "Herkese merhabalar. Her gün üç kişiye ücretsiz tadım kampanyamızla alakalı, bugün [isim] abimiz misafirimiz." |
| Isınma | 5–20 sn | Kısa tanışma, mahalle/komşuluk bağı, "top sende abi" ile sözü devretme |
| Ana gövde | 20–100 sn | Misafirin serbest yorumu. Yönlendirme yok, kesme yok, övgü organik çıkıyor ("şiir gibi aktı gitti", "gram abartmıyorum") |
| Kapanış | 100–117 sn | Karşılıklı teşekkür + "her zaman bekleriz" + "muhabbetimiz daim olsun" |

**Hook kuralı:** ilk 3 saniyede kampanya adı geçiyor. Ücretsiz tadım teklifi
erken söyleniyor — izleyiciye "bu bende de olabilir" hissi veriyor.

**CTA:** videoda ekran üstü CTA yok. CTA **caption'a** bırakılmış:
"konum için bize mesaj atabilirsiniz."

## 6. Caption Şablonu

Referans caption yapısı:

```
Bugün tadım kampanyamızda [İsim] Bey'i ağırladık.

[Ürünü] tattıktan sonra yorumu kısa ve netti:

"[Videodaki en çarpıcı cümle]"

Bizim için en değerlisi de tam olarak bu; hazırlanmış cümleler değil,
deneyen insanların kendi kelimeleri.

[İsim] Bey'e ziyareti ve samimi yorumu için teşekkür ediyoruz.

Siz de Mistanbul'u denemek istiyorsanız, konum için bize mesaj atabilirsiniz.

#mistanbul #etdöner #müşterimemnuniyeti
```

Yapı: **durum → alıntı → marka felsefesi → teşekkür → CTA → 3 hashtag.**
Hashtag sayısı az tutuluyor (3). Emoji yok.

## 7. Üretim Akışı (yeni video için)

1. Ham çekimi tek planda, sabit kamerayla al. Kesme.
2. Otomatik altyazı çıkar (CapCut auto-caption TR).
3. Altyazıyı elle düzelt — özellikle marka adı, kişi isimleri, Türkçe ekler.
4. Konuşmacı chip'lerini ekle, renk kodunu uygula.
5. Karaoke vurgusunu aç, rengi konuşmacıya göre ayarla.
6. Sesi −16/−14 LUFS'a normalize et. Müzik ekleme.
7. 1080×1920, H.264, ~8 Mbps export.

### CapCut ile (birebir eşleşir)
Yuvarlatılmış köşe, per-satır kutu ve karaoke vurgusu CapCut'ta native var.
Önerilen yol.

### ffmpeg + ASS ile (%95 eşleşir)
`format/altyazi-stili.ass` dosyasındaki stili kullan. Tek fark: libass
yuvarlatılmış köşe desteklemiyor, kutular köşeli çıkar.

## 8. Yapma

- Jump cut / hızlı kesim ekleme
- Arka plan müziği koyma
- Intro/outro kartı, logo animasyonu ekleme
- Ekran üstü CTA yazısı koyma
- Altyazıyı 2 satırdan uzun yapma
- Konuşmacı renklerini videodan videoya değiştirme
- Misafirin cümlelerini "düzeltme" — ham dil formatın değeri
