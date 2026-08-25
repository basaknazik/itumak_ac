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
