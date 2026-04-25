# Scoring Enhancement Plan

## The Core Problem

Pipeline ranks reports correctly (low/medium/high similarity).
But absolute scores are not trustworthy — same prompt gives 0.18 vs 0.42 on different reports.
Goal: make the score mean something, not just point in the right direction.

---

## Fix 1 — Remove Trend from Average (easy, high impact)

**Problem:** Trend entities almost never appear in chest CT reports.
Including trend in the average caps the max possible score at 0.75.

**Fix:** Only average fields that have at least 1 entity in GT or prediction.
```
fl_mean = average of fields where (GT_count + Pred_count) > 0
```
Expected gain: TEST_3 score rises from ~0.42 → ~0.56+

---

## Fix 2 — Bilateral Location Normalization (medium effort, high impact)

**Problem:** GT says "bilateral lungs". Model says "right lung" + "left lung".
System sees these as different → false positives + false negatives.
Clinically they are identical.

**Fix:** Before matching, merge location pairs:
```
"right X" + "left X" → "bilateral X"
```
Expected gain: Location F1 improves from ~0.29 → ~0.50 on harder reports.

---

## Fix 3 — Hungarian Matching Instead of Greedy (medium effort, medium impact)

**Problem:** Current system matches GT→Pred in order (greedy).
First match "wins" even if a better global assignment exists.
Reports with many similar entities (e.g., long normal-finding lists) are most affected.

**Fix:** Build score matrix for all GT×Pred pairs, find optimal assignment.
Already implemented in MARCH_v2 — can be adapted directly.

Expected gain: TP count increases ~5–15%, FP/FN decreases.

---

## Fix 4 — Rebuild Embedding Cache Per Test Set (medium effort, medium impact)

**Problem:** embedding_synonyms.json was built from a specific entity.json vocabulary.
New test reports may contain degree/observation terms not in that cache.
When a term is missing → matching score = 0.0, even if it is clinically correct.

This is why Degree F1 = 0.78 in TEST_3 but 0.16 in TEST (same pipeline, different reports).

**Fix:** Run steps 1–3 of the pipeline (entity extractor → tokenizer → embedding)
on every new test dataset before running evaluation.
Cache must be fresh per dataset, not reused from old runs.

---

## Fix 5 — Separate Pathological F1 from Normal F1 (easy, high clinical value)

**Problem:** "Absent" findings (e.g., "no mass detected") are easy to match.
They inflate overall F1 and hide poor performance on real findings.

**Fix:** Report two separate scores:
- **Pathological F1** — only entities with status = present or uncertain
- **Normal F1** — only entities with status = absent

Pathological F1 is the number clinicians actually care about.
It will also correlate much better with human expert judgment.

---

## Step 6 — Radiologist Calibration (required for true accuracy)

All fixes above make the system more consistent and raise the ceiling.
But none of them prove that a score of 0.65 means "65% clinically correct."

To make the score a real measurement:
- Take 10–15 report pairs
- Ask a radiologist to score each pair: 0–100 (clinical equivalence)
- Compare radiologist scores vs pipeline scores (Pearson correlation)
- If Pearson r > 0.85 → pipeline is a reliable ruler, not just a compass

Without this step, absolute scores can be improved but not fully trusted.

---

## Priority Order

| Fix | Effort | Impact | Do When |
|-----|--------|--------|---------|
| Remove trend from average | Low | High | Immediately |
| Bilateral normalization | Low | High | Immediately |
| Rebuild cache per dataset | Low | High | Every new test run |
| Separate pathological F1 | Low | High (clinical) | Immediately |
| Hungarian matching | Medium | Medium | Next sprint |
| Radiologist calibration | High | Critical | Before any publication |
