# Yeni Mezun Makinacılar Anketi — Sonuç Sitesi

İTÜ Makina anketinin sonuçlarını gösteren, kendi kendine güncellenen bir site.
Google Form → Google Sheet → (saatlik) GitHub Action → Pull Request → sen onaylarsın → site güncellenir.

## Nasıl çalışıyor

```
Google Form yanıtları
        │
        ▼
Google Sheet (mevcut anketin)
        │  saatte bir, GitHub Actions
        ▼
scripts/sync_responses.py  → sadece YENİ satırları bulur
        │
        ▼
Pull Request açılır (sadece yeni yanıt varsa)
        │  ← telefonuna GitHub'dan bildirim gelir, bu senin "alarm"ın
        ▼
sen PR'ı incelersin, gerekirse satırı düzenlersin/silersin
        │
        ├─ Merge → data/responses.csv güncellenir → site güncellenir
        └─ Close → o yanıt hiçbir zaman yayınlanmaz
```

`data/responses.csv`, sitenin okuduğu **tek** veri kaynağıdır. Google Sheet'in
kendisi ne kadar dağınık olursa olsun (troll cevaplar dahil), site sadece bu
dosyadaki, senin onayladığın satırları gösterir.

## "Pull Request (PR) nedir?"

Bir PR, "bu dosyada şu değişikliği yapmak istiyorum, onaylar mısın?" demenin
GitHub'daki yoludur. Otomasyon yeni yanıt bulduğunda, `data/responses.csv`'ye
o satırları eklemeyi *öneren* bir PR açar — ama sen onaylayıp "Merge" demeden
hiçbir şey gerçek dosyaya (ve dolayısıyla siteye) yansımaz. PR ekranında:

- Eklenen satırları **kırmızı/yeşil satır farkı (diff)** olarak görürsün.
- Sorunlu bir cevap varsa: GitHub'ın web arayüzünde o satırı seçip silebilir
  ya da metnini düzenleyebilirsin (kalem ikonu / "Edit file").
- Hepsi düzgünse: **Merge pull request** butonuna basarsın → `responses.csv`
  güncellenir → birkaç dakika içinde site de güncellenir.
- Hiçbirini istemiyorsan: **Close pull request** ile kapatırsın, hiçbir şey
  değişmez, o yanıtlar bir daha da önerilmez (zaten "görüldü" sayılır).

Telefonunda GitHub mobil uygulaması varsa (ya da e-posta bildirimleri açıksa),
her yeni PR açıldığında bildirim alırsın — istediğin "alarm" bu.

## Kurulum (tek seferlik)

1. Bu klasördeki her şeyi yeni bir GitHub reponun köküne yükle (repo public
   ya da private olabilir, Pages ikisinde de çalışır).
2. Repo → **Settings → Pages** → "Deploy from a branch" → branch: `main`,
   folder: `/root` → Save. Birkaç dakika içinde
   `https://kullaniciadi.github.io/repo-adi/` adresinde yayında olur.
3. Repo → **Settings → Actions → General** → "Workflow permissions" altında
   **"Read and write permissions"** seçili olduğundan emin ol (otomasyonun PR
   açabilmesi için gerekli).
4. Hepsi bu — `.github/workflows/sync-responses.yml` saatte bir otomatik
   çalışmaya başlar. İstersen Actions sekmesinden "Run workflow" ile elle de
   tetikleyebilirsin.

## Kendi domainini bağlama (GitHub Student Pack)

1. Domain sağlayıcının DNS ayarlarına git.
2. **CNAME** kaydı ekle: `www` → `kullaniciadi.github.io` (kök domain için
   GitHub'ın A kayıtları: `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`).
3. Repo → Settings → Pages → "Custom domain" alanına domaini yaz ve kaydet.
4. DNS yayılması birkaç dakika–birkaç saat sürebilir; sertifika hazır olunca
   "Enforce HTTPS" kutusunu işaretle.

## Dosyalar

| Dosya | Ne işe yarar |
|---|---|
| `index.html` | Sitenin kendisi. `data/responses.csv`'yi aynı repo içinden okur (Google'a bağımlı değil, CORS sorunu yok). |
| `data/responses.csv` | **Onaylanmış** yanıtlar — sitenin gösterdiği tek veri. |
| `data/seen.json` | Hangi yanıtların (zaman damgasına göre) daha önce görüldüğünü tutar; bir daha PR'a düşmesinler diye. |
| `scripts/sync_responses.py` | Google Sheet'ten yeni satırları çekip yukarıdakileri güncelleyen script. |
| `.github/workflows/sync-responses.yml` | Bu scripti saatte bir çalıştırıp gerekirse PR açan otomasyon. |

## Notlar

- Maaş ortalaması, kategorik aralıkların (örn. "91.3-103.4") orta noktaları
  üzerinden **yaklaşık** olarak hesaplanır — sayfada da böyle etiketlenmiştir.
- İlk kurulumda `data/responses.csv` ve `data/seen.json`, bugüne kadarki
  yanıtlarla (troll/nefret söylemi içeren 2 yanıt hariç tutularak) önceden
  dolduruldu — otomasyon bundan sonrasını devralıyor.
- Google Sheet'in kendisini de düzenli temizlemek istersen (örn. "Publish to
  web" → "değişiklik yapıldığında otomatik yayınla" açıksa), bu tamamen
  isteğe bağlı bir ek önlem; site artık Sheet'i değil `responses.csv`'yi baz
  alıyor.
