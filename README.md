# GGD Digital — Marka & Format Arşivi

Bu repo, oturumlar arası kalıcı hafıza görevi görür. Yeni bir Claude oturumu
açıldığında önceki sohbetler hatırlanmaz; buradaki dosyalar hatırlanır.

## Dizin

| Yol | İçerik |
|---|---|
| `format/mistanbul-roportaj-format.md` | Mistanbul Döner müşteri röportajı video formatı — tam spesifikasyon |
| `format/altyazi-stili.ass` | Formatın altyazı stili (ffmpeg/libass ile render için, test edildi) |
| `format/reference/` | Referans videodan çıkarılmış kareler ve altyazı detayları |

## Yeni video edit isteğinde

1. İlgili format dosyasını oku.
2. Ham çekimi indir (yt-dlp / doğrudan link).
3. Formattaki kurallara göre kes veya edit sheet üret.

## Ortam notları

Bu container'da video işi için gerekenler:

```bash
pip install yt-dlp
apt-get update && apt-get install -y ffmpeg fonts-montserrat
```

Network politikası `instagram.com` ve `cdninstagram.com` için açık.
`raw.githubusercontent.com` kapalı — Google Fonts yerine apt paketi kullan.
