# Report Similarity Evaluation — info.md

## Overview

**Total report pairs evaluated:** 16

**Metrics used:**
- ROUGE-1/2/L F1 (lexical overlap at unigram, bigram, and longest common subsequence level)
- Jaccard similarity (unique token set overlap)
- TF-IDF cosine similarity (term-weighted topical similarity)
- Entity polarity match (do shared medical entities agree in positive/negative finding direction?)
- Length ratio (generated / ground_truth character count)

**Composite formula:**
`0.20×ROUGE1 + 0.10×ROUGE2 + 0.20×ROUGEL + 0.25×TF-IDF + 0.10×EntityPolarity + 0.15×Jaccard`

---

## Score Summary Table

| ID | R1 | R2 | RL | Jaccard | TF-IDF | Entity | **Composite** | Band |
|---|---|---|---|---|---|---|---|---|
| valid_100_a_1 | 47.8% | 21.9% | 26.0% | 26.8% | 61.9% | 78% | **44.2%** | 30-49% |
| valid_1001_a_1 | 54.9% | 23.7% | 29.5% | 38.9% | 65.6% | 88% | **50.2%** | 50-69% |
| valid_1003_a_1 | 47.4% | 22.5% | 28.9% | 26.4% | 64.1% | 100% | **47.5%** | 30-49% |
| valid_1005_a_1 | 56.0% | 29.1% | 34.9% | 40.8% | 67.2% | 100% | **54.0%** | 50-69% |
| valid_100_a_2 | 47.8% | 21.9% | 26.0% | 26.8% | 61.9% | 78% | **44.2%** | 30-49% |
| valid_1001_a_2 | 48.7% | 22.7% | 29.0% | 24.6% | 61.5% | 100% | **46.9%** | 30-49% |
| valid_1003_a_2 | 45.6% | 21.6% | 28.0% | 28.9% | 63.5% | 80% | **45.1%** | 30-49% |
| valid_1005_a_2 | 54.9% | 29.5% | 34.1% | 40.3% | 66.1% | 100% | **53.3%** | 50-69% |
| valid_1000_a_1 | 66.3% | 54.8% | 57.1% | 55.7% | 77.9% | 88% | **66.7%** | 50-69% |
| valid_1002_a_1 | 47.7% | 25.0% | 25.6% | 31.3% | 65.6% | 29% | **41.1%** | 30-49% |
| valid_1004_a_1 | 46.9% | 24.2% | 32.1% | 36.6% | 64.5% | 100% | **49.8%** | 30-49% |
| valid_1005_b_1 | 58.0% | 42.7% | 34.1% | 45.0% | 70.2% | 86% | **55.5%** | 50-69% |
| valid_1000_a_2 | 57.3% | 27.0% | 32.3% | 41.7% | 68.1% | 88% | **52.7%** | 50-69% |
| valid_1002_a_2 | 46.1% | 23.7% | 26.1% | 31.1% | 61.8% | 43% | **41.2%** | 30-49% |
| valid_1004_a_2 | 46.9% | 24.2% | 32.1% | 36.6% | 64.5% | 100% | **49.8%** | 30-49% |
| valid_1005_b_2 | 56.8% | 43.1% | 32.2% | 44.7% | 67.9% | 86% | **54.4%** | 50-69% |

---

## Per-Report Analysis

### valid_100_a_1

- **Composite score:** 44.2%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.57 (GT: 2328 chars, GEN: 1319 chars)
- **Entity polarity agreement:** 78%
- **Key observations:** generated significantly shorter than GT; low recall — GT findings significantly missed

### valid_1001_a_1

- **Composite score:** 50.2%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.80 (GT: 1283 chars, GEN: 1021 chars)
- **Entity polarity agreement:** 88%

### valid_1003_a_1

- **Composite score:** 47.5%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 1.95 (GT: 682 chars, GEN: 1333 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** generated significantly longer than GT; entity findings well-aligned despite surface differences

### valid_1005_a_1

- **Composite score:** 54.0%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.76 (GT: 1626 chars, GEN: 1228 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** entity findings well-aligned despite surface differences

### valid_100_a_2

- **Composite score:** 44.2%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.57 (GT: 2328 chars, GEN: 1319 chars)
- **Entity polarity agreement:** 78%
- **Key observations:** generated significantly shorter than GT; low recall — GT findings significantly missed

### valid_1001_a_2

- **Composite score:** 46.9%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.80 (GT: 1283 chars, GEN: 1026 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** entity findings well-aligned despite surface differences

### valid_1003_a_2

- **Composite score:** 45.1%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 1.95 (GT: 682 chars, GEN: 1330 chars)
- **Entity polarity agreement:** 80%
- **Key observations:** generated significantly longer than GT

### valid_1005_a_2

- **Composite score:** 53.3%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.63 (GT: 1626 chars, GEN: 1021 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** entity findings well-aligned despite surface differences

### valid_1000_a_1

- **Composite score:** 66.7%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 1.10 (GT: 1214 chars, GEN: 1330 chars)
- **Entity polarity agreement:** 88%
- **Key observations:** substantial verbatim phrase overlap; high topical similarity (TF-IDF)

### valid_1002_a_1

- **Composite score:** 41.1%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.65 (GT: 2032 chars, GEN: 1318 chars)
- **Entity polarity agreement:** 29%
- **Key observations:** many entity-level contradictions (polarity mismatches)

### valid_1004_a_1

- **Composite score:** 49.8%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.48 (GT: 2117 chars, GEN: 1021 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** generated significantly shorter than GT; entity findings well-aligned despite surface differences; low recall — GT findings significantly missed

### valid_1005_b_1

- **Composite score:** 55.5%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.79 (GT: 1659 chars, GEN: 1312 chars)
- **Entity polarity agreement:** 86%
- **Key observations:** substantial verbatim phrase overlap; high topical similarity (TF-IDF)

### valid_1000_a_2

- **Composite score:** 52.7%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.84 (GT: 1214 chars, GEN: 1021 chars)
- **Entity polarity agreement:** 88%

### valid_1002_a_2

- **Composite score:** 41.2%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.64 (GT: 2032 chars, GEN: 1291 chars)
- **Entity polarity agreement:** 43%
- **Key observations:** many entity-level contradictions (polarity mismatches); low recall — GT findings significantly missed

### valid_1004_a_2

- **Composite score:** 49.8%
- **Similarity band:** 30-49% — Low-moderate — same domain, significant contradictions
- **Length ratio:** 0.48 (GT: 2117 chars, GEN: 1021 chars)
- **Entity polarity agreement:** 100%
- **Key observations:** generated significantly shorter than GT; entity findings well-aligned despite surface differences; low recall — GT findings significantly missed

### valid_1005_b_2

- **Composite score:** 54.4%
- **Similarity band:** 50-69% — Moderate — shared structure but divergent findings
- **Length ratio:** 0.80 (GT: 1659 chars, GEN: 1319 chars)
- **Entity polarity agreement:** 86%
- **Key observations:** substantial verbatim phrase overlap

---

## Distribution Summary

- **50-69%:** 7 reports
- **30-49%:** 9 reports

- **Mean composite:** 49.8%
- **Min:** 41.1% (valid_1002_a_1)
- **Max:** 66.7% (valid_1000_a_1)
