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
| Konuşmacı etiketi (chip) | y 775–802 px, x 45–215 (%60.5–62.7) |
| Altyazı satır 1 | y 822–849 px (%64.2–66.3) |
| Altyazı satır 2 | y 883–910 px (%69.0–71.1) |
| Satır aralığı (üst-üst) | 61 px @720 = **92 px @1080** |
| Yatay hizalama | Metin bloğu **ortalı**; chip 1. satırın sol kenarını takip eder |
| Maksimum satır | 2 |

1080 × 1920'ye çevirmek için tüm px değerlerini **×1.5** yap.

### Blok YUKARIDAN sabitlenir — kritik

Ölçüm: tek satırlık altyazı y823–849, iki satırlık altyazının ilk satırı
y822–849. **İlk satır her zaman aynı yerde**, blok aşağı doğru büyür.

Altyazıyı alttan sabitlersen tek satırlık metinler iki satırlığın ikinci
satırının yerine oturur ve altyazı sürekli zıplar. Formatın en kolay
kaçırılan detayı bu.

ASS'te: `Alignment 8` (üst-orta) + her satır kendi Dialogue'u,
`{\pos(540, 1223 + satır_no × 78)}`.

**MarginV kullanma, `\pos` kullan.** libass üst üste binen altyazıları
otomatik aşağı itiyor (collision detection) ve MarginV'yi eziyor —
ikinci satır verdiğin yere gitmiyor. `\pos` bu davranışı kapatır.

### Tipografi — ölçümle doğrulandı

Referanstan ölçülen üç bağımsız değer:

| Ölçüm | Değer @1080 |
|---|---|
| Büyük harf (cap) yüksekliği | 40.5 px |
| Gövde (stem) kalınlığı | 9 px |
| "Her gün üç kişiye ücretsiz tadım" satır genişliği | 890 px |

Font: **Inter ExtraBold**.

> **Montserrat değil.** Aynı cap yüksekliğinde satır genişliği %12–16
> şaşıyor, yani Montserrat belirgin şekilde daha geniş. Poppins de değil
> (tek katlı 'a', referansta çift katlı).

### ASS Fontsize ≠ punto — tuzak

libass'in `Fontsize` değeri FreeType/PIL puntosuyla aynı şey değil; aynı
sayıyı verdiğinde belirgin şekilde daha küçük basıyor. Inter ExtraBold için:

| Ölçüm yöntemi | Değer |
|---|---|
| PIL punto (satır sarma hesabı için) | 56 |
| ASS `Fontsize` (stil dosyasına yazılan) | **69** |

İkisi de aynı görsel boyutu verir. Boyutu PIL'le hesaplayıp ASS'e aynen
yazarsan **%18 küçük** çıkar. Kalibrasyon her zaman render çıktısı
ölçülerek yapılmalı, font metriğinden hesaplanarak değil.

- Renk: beyaz `#FFFFFF`
- Arka plan: siyah `#151215`, **yuvarlatılmış köşe**, her satırın kendi kutusu var
- Kutu dolgusu: ASS `Outline 13`

### Referanstan bilinçli sapmalar

Aşağıdakiler ölçümle referansa eşitlendikten sonra, okunabilirlik için
kasten değiştirildi. Yeni videoda da bu değerler kullanılmalı:

| | Referans | Kullanılan | Neden |
|---|---|---|---|
| Kutu opaklığı | ~%75 (alpha `40`) | **~%87 (alpha `20`)** | Hareketli/açık renkli arka planda metin daha net |
| Satır aralığı | 78 @1080 | **88 @1080** | İki satır birbirine yapışık duruyordu |
| Satır genişlik sınırı | ~890 px | **1000 px** | Daha az satır kırılması, daha az zıplayan blok |
| Ekran başına kelime | 7 | **8** | Yukarıdakiyle uyumlu |

Bu ayarlarla 53 ekrandan 51'e düşüldü, iki satırlı ekran sayısı 17'den
15'e indi — altyazı daha az bölünüyor.

### Chip (konuşmacı etiketi) — ölçülen değerler

| | Referans @720 | Kullanılan ASS ayarı |
|---|---|---|
| Kutu | y768–805, x44–220 | `\pos(72,1162)`, Alignment 7 |
| İçindeki yazı | yük. 19, gen. 144 | Inter ExtraBold **44**, `Outline 5` |
| Yatay dolgu | sol 16, sağ 17 | `\h` × 3 her iki yana |

**Chip yatayda yazıyla birlikte kayar.** Satırlar ortalı olduğu için
1. satırın sol kenarı her ekranda değişir; chip de onunla birlikte kayar.
Ölçüm: kısa satırda chip x146 / yazı x166, uzun satırda chip x44 / yazı x63
— her ikisinde de chip yazının **19–20 px solunda**. Sabit sol kenara
koyarsan kısa altyazılarda etiket metinden kopuk kalır.

Formül: `chip_x = 540 − (1._satır_genişliği / 2) − 24` @1080.

**Chip altyazıya dikeyde de yapışık durur.** Referansta chip kutusunun alt kenarı
(y805) ile altyazı kutusunun üst kenarı (y806) arasında **0 piksel** var —
iki kutu tek parça gibi okunuyor. Arada boşluk bırakmak formatı bozar.

Bu yüzden `CHIP_Y`, altyazı kutusunun üst kenarına göre ayarlanır:
`CHIP_Y = SATIR1_Y − chip_kutu_yüksekliği`. Chip puntosu veya `Outline`'ı
değişirse kutu yüksekliği de değişir, `CHIP_Y` yeniden ölçülmelidir.

### Bu yöntemle kapatılamayan tek fark

Referansta kutu köşeleri yuvarlatılmış; libass yuvarlatma desteklemiyor,
kutular köşeli çıkıyor. Diğer her ölçü 1–2 piksel içinde eşleşiyor.
Birebir köşe istenirse CapCut gerekir.

### Kelime Vurgusu (karaoke)

Konuşulan kelime o an renklenir, sonra beyaza döner. **Sadece aktif kelime**
renklidir — sweep-and-stay değil.

### Konuşmacı Renk Kodu

| Konuşmacı | Chip rengi | Vurgu rengi | Chip yazı |
|---|---|---|---|
| Host (Volkan Usta) | `#F5AF0E` amber | `#F5AF0E` | siyah |
| 1. misafir | `#E75F5A` mercan | `#E75F5A` | beyaz |
| 3. konuşmacı gerekirse | `#2D96DC` mavi | `#2D96DC` | beyaz |

**ASS renk tuzağı:** ASS renk formatı `&HBBGGRR` — RGB'nin tersi. Chip
rengini stil satırına, vurgu rengini `\c` etiketine yazarken ikisi de aynı
BGR dizilimiyle girilmeli. Ters yazılırsa chip bir renk, vurgu başka renk
çıkar ve fark ilk bakışta gözden kaçar (`#8B4FD6` lila ↔ `#D64F8B` pembe
gibi).

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
