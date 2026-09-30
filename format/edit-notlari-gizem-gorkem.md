# Edit notları — Gizem & Görkem tadım röportajı

Ham dosya: `DJI_20260921210633_0385_D (1).MP4` (DJI Osmo Pocket 3, 21.09.2026)
Format referansı: `format/mistanbul-roportaj-format.md`

## Ham kaynak

| | |
|---|---|
| Çözünürlük | 1080 × 1920 (zaten dikey, crop gerekmedi) |
| FPS | 59.94 |
| Codec | HEVC, ~46 Mbps |
| Süre | 103.34 sn |
| Ses | AAC 48 kHz stereo, ortalama −17.4 dBFS |
| Kesim | Yok — tek plan, elde çekim |

## Yapılan kesimler

| İşlem | Değer | Gerekçe |
|---|---|---|
| Baş kesme | 0 → 3.10 sn | Çarşıda yürüyüş girişi + "Hazır mıyız?" ön kaydı. Hook'un ilk 3 saniyesini yiyordu, marka mesajı taşımıyordu. |
| Son kesme | 97.50 sn'de bitir | Konuşma 95.87'de bitiyor. Sonrası 7.4 sn sessiz kaydırma. 1.6 sn dükkân cephesi bırakıldı, gerisi atıldı. |
| **Final süre** | **94.40 sn** | Referans 116.8 sn'ydi; bu daha sıkı. |

İçeride hiç kesim yapılmadı — format kuralı gereği tek plan korundu.

## Teknik çıktı

- 1080 × 1920, 30 fps, H.264 High@4.1, CRF 20
- Ses: AAC 192 kbps, loudnorm −14 LUFS / −1.5 dBTP
- `+faststart` (Instagram yüklemesi için)

## Altyazı

- 217 kelime, 55 ekran, kelime bazlı karaoke vurgusu
- Otomatik üretim: `faster-whisper large-v3` (TR, kelime zaman damgalı) → `make_ass.py`
- Konuşmacı renkleri:
  - **Volkan Usta** — `#F5AF0E` amber (formatla aynı)
  - **Gizem Hanım** — `#E75F5A` mercan (formatta misafir rengi)
  - **Görkem Bey** — `#2D96DC` mavi (üçüncü konuşmacı için yeni, formata eklendi)

  Görkem'in rengi önce lila seçilmişti; ayrıca chip ile vurgu rengi ASS'in
  ters byte dizilimi yüzünden birbirinden farklı çıkıyordu (chip `#8B4FD6`,
  vurgu `#D64F8B`). İkisi de `#2D96DC` olarak düzeltildi. Daha sakin bir
  ton istenirse turkuaz `#12A594` hazır alternatif.

## Transkriptte elle düzeltilenler

| Zaman (ham) | Whisper çıktısı | Düzeltilen | Neden |
|---|---|---|---|
| 5.55 | "3" | "üç" | Referans formatta rakamlar yazıyla |
| 7.53 / 8.63 / 59.41 | "gizem" / "görkem" | "Gizem" / "Görkem" | Özel isim |
| 72.15 | "300" + "-350" | "300-350" | Tokenizasyon hatası |
| 82.29 | "gördüğünüzden" | "gördüğümüzden" | ASR hatası (kullanıcı doğruladı) |
| 93.35 | "Erdoğan için de bekliyorum" | "Her zaman için de bekliyorum" | Açık ASR hatası; referans videoda da "Her zaman için de beklerim" geçiyor |
| 57.07–57.83 | "Bunları kararlı tutuyoruz. Tabii ki siz vereceksiniz" | "Bunların kararını tabii ki siz vereceksiniz" | "tutuyoruz." ASR güveni 0.447 ve süresi 0.06 sn — uydurma kelime, silindi |

## Altyazı stili — v2'de düzeltildi

İlk sürümde altyazı referansa oturmuyordu. Yeniden ölçüldü:

| Sorun | İlk sürüm | Düzeltilmiş |
|---|---|---|
| Font ailesi | Montserrat ExtraBold (yanlış) | **Inter ExtraBold** |
| Punto | 63 (%12 büyük) | **56** |
| Blok sabitleme | Alttan (tek satırlık altyazılar zıplıyordu) | **Üstten** |
| Satır aralığı | Font varsayılanı (~68px) | **92 px @1080** |
| Kutu dolgusu | Outline 11 | **Outline 13** |
| Chip | 33 punto, dar | **30 punto, `\h` ile genişletilmiş** |

En kritik olan blok sabitlemesi: referansta ilk satır kaç satır olursa olsun
hep y822'de (@720). Alttan sabitlersen tek satırlık altyazı iki satırlığın
ikinci satırının yerine düşüyor ve altyazı sürekli yer değiştiriyor.

Font tespiti üç bağımsız ölçümle yapıldı (cap yüksekliği 40.5px, gövde
kalınlığı 9px, bilinen bir cümlenin satır genişliği 890px @1080).
Montserrat aynı cap yüksekliğinde %12–16 geniş kalıyor; Inter ExtraBold 56
üçünü de %1 sapmayla tutturuyor.

## Doğrulaman gerekenler

1. **Kapanış 90–96 sn arası konuşmacı atamaları.**
   Bu bölümde teşekkürler üst üste biniyor ve önünden iki kişi geçtiği için
   görüntüden kimin konuştuğunu doğrulayamadım. Şu an:
   - "Çok sağ olun. Ayağınıza sağlık." → Volkan Usta
   - "Biz teşekkür ederiz abi." → Görkem Bey
   - "Çok çok teşekkür ediyorum." → Gizem Hanım
   - "Her zaman için de bekliyorum." → Volkan Usta
   - "Çok sağ olasın." → Görkem Bey

   Yanlışsa `konusmacilar.json` içindeki aralıkları düzeltip `make_ass.py`
   tekrar çalıştırılır.

2. **Hook'ta "ücretsiz" yok.** Referans videoda "Her gün üç kişiye **ücretsiz** tadım
   kampanyamız" deniyor; bu çekimde sadece "Her gün üç kişiye tadım kampanyamız".
   Whisper atlamadı, söylenmemiş. Teklifin bedava olduğu ilk 3 saniyede geçmiyor —
   bir sonraki çekimde bu kelimeyi söyletmek hook'u güçlendirir.

## İçerik değerlendirmesi

**Güçlü:** Gizem Hanım'ın "Bursalıyım" açılışı güçlü bir güvenilirlik kancası —
döner konusunda otorite iddiası taşıyan bir yerden geliyor. "Aradığımız o klasik
lezzetin yanı sıra burada çok farklı bir tat vardı" cümlesi caption alıntısı için
en uygun olanı.

**Riskli:** Görkem Bey'in 65–81 sn arası bölümü ("içine sos basıyor, et yok,
300-350 liraya satıyor") rakipleri hedef alıyor. Videoda misafirin ağzından
çıktığı için savunulabilir, ama yorumlarda tartışma açma ihtimali var.
Caption'a taşımadım. Tamamen temiz istersen bu bölümü kesmek mümkün —
ancak o zaman formatın "tek plan, kesim yok" kuralı bozulur. Bu yüzden
kesmedim; karar senin.
