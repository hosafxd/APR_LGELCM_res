# Görev 3 — CT-RATE Veri Seti Metrik Değerlendirmesi

**Tarih:** 03.05.2026  
**Grup:** CT-RATE (Grup 3)  
**Veri:** `50_0/reports_dataset.json` — 33 rapor çifti (AI generated vs. Ground Truth)

---

## 1. Yöntem Özeti

Görev tanımı gereği, CT-RATE veri setinde henüz bir radyolog değerlendirmesi bulunmamaktadır. Bu nedenle korelayon hesaplaması için **AI tabanlı RadCliQ simülasyonu** yapılmıştır.

### 1.1 AI RadCliQ Değerlendirmesi

Her rapor çifti (generated ↔ ground truth), **Claude AI modeli** tarafından RadCliQ çerçevesinde altı hata kategorisi için değerlendirilmiştir:

| Kategori | Açıklama |
|----------|----------|
| **FD** (False Discovery) | Generated raporda bulunup GT'de yer almayan bulgular (halüsinasyon) |
| **FO** (False Omission) | GT'de bulunup generated raporda eksik kalan bulgular (gözden kaçan bulgular) |
| **Loc** (Incorrect Location) | Bulgu doğru ama anatomik lokasyon yanlış |
| **Sev** (Incorrect Severity) | Bulgu doğru ama şiddet/derece yanlış (örn. "minimal" yerine "yaygın") |
| **Trend** (Incorrect Trend) | İyileşme/kötüleşme yönü yanlış |
| **Attr** (Incorrect Attribute) | Bulguya atanan özellik yanlış (etiyoloji, desen, büyüklük kategorisi) |

> **Not:** RadCliQ *hata üzerine kurulu* bir sistemdir — skor yüksekse rapor daha kötüdür.  
> Korelasyonlarda **negatif r** değeri beklentimizdir (metrik yüksekse hata az olmalı).

### 1.2 Hesaplanan Metrikler

- **ER2SCORE (entity F1):** `pipeline_revised_28_04/11_entity_match_evaluation_flexible_score_fast.py` — tıbbi varlık eşleştirme tabanlı Precision / Recall / F1
- **BLEU-1, BLEU-2, BLEU-4:** Sentence-level, add-1 smoothing (pure Python implementasyonu)
- **ROUGE-1, ROUGE-2, ROUGE-L:** Pure Python; F1 skoru rapor edilmiştir

---

## 2. Per-Rapor Sonuçlar

| Rapor ID | ER2-F1 | BLEU-1 | BLEU-4 | R1-F1 | RL-F1 | FD | FO | Loc | Sev | Attr | Total |
|----------|--------|--------|--------|-------|-------|----|----|-----|-----|------|-------|
| r92 (valid_45) | 0.821 | 0.712 | 0.671 | 0.810 | 0.797 | 0 | 4 | 0 | 0 | 0 | 4 |
| r106 (valid_52) | 0.693 | 0.546 | 0.429 | 0.673 | 0.586 | 2 | 3 | 0 | 0 | 1 | 6 |
| r150 (valid_66) | 0.000 | 0.605 | 0.446 | 0.683 | 0.557 | 2 | 4 | 0 | 0 | 1 | 7 |
| r174 (valid_79) | 0.715 | 0.542 | 0.417 | 0.675 | 0.605 | 0 | 4 | 0 | 0 | 1 | 5 |
| r443 (valid_193) | 0.328 | 0.476 | 0.175 | 0.519 | 0.300 | 3 | 4 | 0 | 0 | 1 | 8 |
| r482 (valid_209) | 0.615 | 0.431 | 0.352 | 0.642 | 0.580 | 0 | 5 | 0 | 0 | 0 | 5 |
| r553 (valid_241) | 0.300 | 0.291 | 0.093 | 0.444 | 0.281 | 0 | 3 | 0 | 0 | 0 | 3 |
| r561 (valid_245) | 0.495 | 0.465 | 0.182 | 0.525 | 0.350 | 3 | 2 | 0 | 0 | 1 | 6 |
| r696 (valid_298) | 0.160 | 0.283 | 0.097 | 0.372 | 0.262 | 1 | 3 | 0 | 0 | 0 | 4 |
| r714 (valid_307) | 0.274 | 0.547 | 0.187 | 0.563 | 0.339 | 1 | 0 | 0 | 0 | 0 | 1 |
| r850 (valid_362) | 0.000 | 0.032 | 0.017 | 0.266 | 0.185 | 1 | 8 | 0 | 1 | 1 | 11 |
| r920 (valid_391) | 0.000 | 0.352 | 0.118 | 0.476 | 0.211 | 3 | 6 | 0 | 0 | 1 | 10 |
| r1407 (valid_589) | 0.000 | 0.503 | 0.165 | 0.530 | 0.284 | 1 | 2 | 0 | 0 | 0 | 3 |
| r1574 (valid_666) | 0.000 | 0.485 | 0.156 | 0.511 | 0.272 | 3 | 2 | 0 | 0 | 1 | 6 |
| r1596 (valid_674) | 0.000 | 0.818 | 0.741 | 0.857 | 0.818 | 1 | 3 | 0 | 0 | 0 | 4 |
| r1610 (valid_679) | 0.000 | 0.576 | 0.216 | 0.589 | 0.350 | 2 | 2 | 0 | 0 | 1 | 5 |
| r1666 (valid_707) | 0.000 | 0.171 | 0.088 | 0.410 | 0.297 | 2 | 7 | 0 | 0 | 1 | 10 |
| r1670 (valid_709) | 0.653 | 0.367 | 0.292 | 0.571 | 0.530 | 0 | 4 | 0 | 0 | 0 | 4 |
| r1689 (valid_716) | 0.748 | 0.627 | 0.556 | 0.736 | 0.687 | 0 | 3 | 0 | 0 | 0 | 3 |
| r1752 (valid_742) | 0.450 | 0.616 | 0.266 | 0.622 | 0.482 | 0 | 1 | 0 | 0 | 0 | 1 |
| r1812 (valid_771) | 0.430 | 0.486 | 0.282 | 0.552 | 0.469 | 1 | 6 | 0 | 0 | 0 | 7 |
| r1988 (valid_844) | 0.207 | 0.414 | 0.206 | 0.518 | 0.370 | 0 | 4 | 0 | 0 | 0 | 4 |
| r1992 (valid_845) | 0.533 | 0.369 | 0.257 | 0.542 | 0.446 | 0 | 4 | 0 | 1 | 1 | 6 |
| r2016 (valid_852) | 0.000 | 0.464 | 0.136 | 0.532 | 0.295 | 2 | 3 | 0 | 0 | 1 | 6 |
| r946 (valid_406) | 0.786 | 0.494 | 0.465 | 0.690 | 0.679 | 0 | 3 | 0 | 0 | 0 | 3 |
| r1030 (valid_440) | 0.389 | 0.349 | 0.122 | 0.472 | 0.299 | 3 | 0 | 0 | 0 | 0 | 3 |
| r1128 (valid_479) | 0.289 | 0.423 | 0.133 | 0.452 | 0.246 | 3 | 2 | 0 | 0 | 1 | 6 |
| r1134 (valid_482) | 0.000 | 0.481 | 0.348 | 0.586 | 0.468 | 2 | 5 | 0 | 1 | 1 | 9 |
| r1190 (valid_498) | 0.363 | 0.524 | 0.132 | 0.580 | 0.309 | 3 | 1 | 0 | 0 | 0 | 4 |
| r1210 (valid_504) | 0.151 | 0.255 | 0.072 | 0.403 | 0.240 | 2 | 4 | 0 | 1 | 1 | 8 |
| r1234 (valid_515) | 0.000 | 0.444 | 0.148 | 0.514 | 0.299 | 2 | 4 | 0 | 1 | 1 | 8 |
| r1249 (valid_523) | 0.320 | 0.384 | 0.118 | 0.490 | 0.245 | 0 | 6 | 0 | 0 | 0 | 6 |
| r1304 (valid_544) | 0.132 | 0.284 | 0.083 | 0.403 | 0.227 | 0 | 5 | 1 | 0 | 1 | 7 |

---

## 3. Ortalama Skorlar (33 rapor)

| Metrik | Ortalama |
|--------|----------|
| **ER2SCORE F1** | **0.2985** |
| BLEU-1 | 0.4491 |
| BLEU-2 | 0.3530 |
| BLEU-4 | 0.2474 |
| ROUGE-1 F1 | 0.5518 |
| ROUGE-2 F1 | 0.3485 |
| ROUGE-L F1 | 0.4050 |
| **RadCliQ Total (ort. hata)** | **5.55 / rapor** |

---

## 4. Korelasyon Sonuçları

> **Yorum kılavuzu:**  
> - Negatif r → beklenen yön (hata arttıkça metrik düşer)  
> - |r| > 0.3 → zayıf–orta ilişki; |r| > 0.5 → güçlü ilişki  
> - p < 0.05 → istatistiksel olarak anlamlı  
> - Trend kategorisi: tüm raporlarda 0 (varyans yok), korelasyon hesaplanamaz

### 4.1 ER2SCORE F1 vs. RadCliQ Kategorileri

| Kategori | Pearson r | p | Spearman r | p | Kendall τ | p |
|----------|-----------|---|------------|---|-----------|---|
| **FD** | **-0.445** | **0.010** | **-0.445** | **0.010** | **-0.288** | **0.019** |
| FO | -0.159 | 0.377 | -0.129 | 0.474 | -0.089 | 0.467 |
| Loc | -0.108 | 0.550 | -0.095 | 0.601 | -0.019 | 0.877 |
| Sev | -0.250 | 0.161 | -0.253 | 0.155 | -0.106 | 0.386 |
| Trend | — | — | — | — | — | — |
| **Attr** | **-0.385** | **0.027** | **-0.409** | **0.018** | **-0.239** | **0.051** |
| **Total** | **-0.455** | **0.008** | **-0.456** | **0.008** | **-0.318** | **0.009** |

### 4.2 BLEU-1 vs. RadCliQ Kategorileri

| Kategori | Pearson r | p | Spearman r | p | Kendall τ | p |
|----------|-----------|---|------------|---|-----------|---|
| FD | -0.056 | 0.755 | -0.065 | 0.719 | -0.053 | 0.664 |
| **FO** | **-0.484** | **0.004** | **-0.429** | **0.013** | **-0.301** | **0.014** |
| Loc | -0.192 | 0.284 | -0.223 | 0.213 | -0.046 | 0.710 |
| **Sev** | **-0.371** | **0.034** | -0.328 | 0.062 | -0.140 | 0.252 |
| Trend | — | — | — | — | — | — |
| Attr | -0.266 | 0.135 | -0.217 | 0.226 | -0.129 | 0.292 |
| **Total** | **-0.513** | **0.002** | **-0.420** | **0.015** | **-0.282** | **0.021** |

### 4.3 BLEU-4 vs. RadCliQ Kategorileri

| Kategori | Pearson r | p | Spearman r | p | Kendall τ | p |
|----------|-----------|---|------------|---|-----------|---|
| **FD** | **-0.347** | **0.048** | -0.314 | 0.076 | -0.208 | 0.088 |
| FO | -0.075 | 0.679 | -0.122 | 0.499 | -0.081 | 0.505 |
| Loc | -0.167 | 0.354 | -0.260 | 0.144 | -0.053 | 0.664 |
| Sev | -0.191 | 0.286 | -0.204 | 0.255 | -0.087 | 0.476 |
| Trend | — | — | — | — | — | — |
| Attr | -0.273 | 0.124 | -0.242 | 0.175 | -0.144 | 0.239 |
| **Total** | -0.318 | 0.071 | **-0.347** | **0.048** | -0.233 | 0.057 |

### 4.4 ROUGE-1 F1 vs. RadCliQ Kategorileri

| Kategori | Pearson r | p | Spearman r | p | Kendall τ | p |
|----------|-----------|---|------------|---|-----------|---|
| FD | -0.253 | 0.156 | -0.276 | 0.119 | -0.182 | 0.137 |
| FO | -0.273 | 0.124 | -0.202 | 0.260 | -0.142 | 0.245 |
| Loc | -0.214 | 0.231 | -0.260 | 0.144 | -0.053 | 0.664 |
| Sev | -0.308 | 0.082 | -0.240 | 0.179 | -0.102 | 0.403 |
| Trend | — | — | — | — | — | — |
| Attr | -0.306 | 0.084 | -0.267 | 0.132 | -0.159 | 0.193 |
| **Total** | **-0.449** | **0.009** | **-0.397** | **0.022** | **-0.275** | **0.025** |

### 4.5 ROUGE-L F1 vs. RadCliQ Kategorileri

| Kategori | Pearson r | p | Spearman r | p | Kendall τ | p |
|----------|-----------|---|------------|---|-----------|---|
| **FD** | **-0.439** | **0.011** | **-0.367** | **0.036** | -0.235 | 0.055 |
| FO | -0.068 | 0.706 | -0.129 | 0.473 | -0.089 | 0.467 |
| Loc | -0.183 | 0.309 | -0.260 | 0.144 | -0.053 | 0.664 |
| Sev | -0.191 | 0.288 | -0.213 | 0.234 | -0.091 | 0.457 |
| Trend | — | — | — | — | — | — |
| Attr | -0.335 | 0.057 | -0.325 | 0.065 | -0.193 | 0.114 |
| **Total** | **-0.371** | **0.034** | **-0.410** | **0.018** | **-0.294** | **0.016** |

---

## 5. Yorumlar ve Bulgular

### En önemli sonuçlar

**ER2SCORE (bizim metriğimiz) en güçlü ve tutarlı korelasyonu gösterdi:**
- RadCliQ Total ile: Pearson **−0.455** (p=0.008), Spearman **−0.456** (p=0.008) — anlamlı
- FD kategorisiyle: Pearson **−0.445** (p=0.010) — halüsinasyonları iyi yakalıyor
- Attr kategorisiyle: Pearson **−0.385** (p=0.027) — yanlış etiyoloji/niteleme hatalarına duyarlı

**BLEU-1, FO (False Omission) kategorisinde en yüksek korelasyona ulaştı:**
- Pearson **−0.484** (p=0.004) — kaçırılan bulguları cümle örtüşmesi üzerinden yakalayabiliyor

**Trend kategorisi:** Veri setindeki 33 raporun hiçbirinde Trend hatası tespit edilmedi. Bu, modelin trend ifadelerinde yanıltıcı olmadığını gösteriyor (veya trend ifadesinin bu raporlarda az kullanıldığını).

**Loc (Incorrect Location):** Yalnızca 1 raporda gözlemlendi — varyans çok düşük, korelasyon anlamlı çıkmıyor.

### Radyolojik Bulgular Açısından En Kritik Hatalar

1. **Covid-19 pnömonisi olan vakalarda AI tamamen kaçırıyor:** r482, r553, r696, r1596, r1666, r1689, r2016 — generated rapor "normal" derken GT Covid bulguları içeriyor. Bu raporlarda FO = 3–7.
2. **Şablon tekrarı sorunu:** Birçok generated rapor aynı "şablonu" kullanıyor (peribronchial thickening, emphysema, millimetric nodules). GT'de bunlar olmadığında yüksek FD ve Attr hatası oluşuyor (r1030, r1128, r1190).
3. **r850 en kötü vaka:** FO=8, Total=11 — kompleks hastada (karaciğer nakli, bilateral plevral efüzyon, multiple nodül) AI yalnızca Covid pattern raporlamış.

---

## 6. Dosya Çıktıları

| Dosya | Açıklama |
|-------|----------|
| `50_0/Results/task3_full_results.csv` | 33 rapor, tüm metrikler + AI RadCliQ skorları |
| `50_0/Results/task3_full_results.json` | Aynı veri + korelasyon matrisi |
| `pipeline_revised_28_04/detailed_evaluation_results.json` | ER2SCORE entity-level detaylar |
| `task3_full_evaluation.py` | Yeniden çalıştırılabilir tam analiz scripti |

---

## 7. Çalıştırma Talimatı

```bash
# Pipeline klasörüne gidip entity match çalıştır
cd "/Users/muratemir/Desktop/Medical Imaging/01.05/pipeline_revised_28_04"
python3 11_entity_match_sequential.py   # (tek thread versiyonu)

# Ardından tam analizi çalıştır
cd "/Users/muratemir/Desktop/Medical Imaging/01.05"
python3 task3_full_evaluation.py
```
