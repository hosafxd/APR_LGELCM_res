"""
Task 3 — CT-RATE Dataset Full Evaluation
=========================================
AI tabanlı RadCliQ skorları + ER2SCORE (entity F1) + BLEU + ROUGE
Pearson, Spearman ve Kendall's Tau korelasyonları

Tüm 33 rapor çifti üzerinde çalışır.
Dış kütüphane gerektirmez (sadece numpy).
"""

import json
import os
import re
import math
import numpy as np
from collections import Counter

# ─── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR       = "/Users/muratemir/Desktop/Medical Imaging/01.05"
PIPELINE_DIR   = os.path.join(BASE_DIR, "pipeline_revised_28_04")
REPORTS_JSON   = os.path.join(BASE_DIR, "50_0/reports_dataset.json")
DETAILED_JSON  = os.path.join(PIPELINE_DIR, "detailed_evaluation_results.json")
OUT_DIR        = os.path.join(BASE_DIR, "50_0/Results")
os.makedirs(OUT_DIR, exist_ok=True)

# ─── AI RadCliQ SCORES (33 reports) ───────────────────────────────────────────
# Evaluated by Claude (AI model) following RadCliQ framework:
#   FD  = False Discovery    (hallucinated findings not in GT)
#   FO  = False Omission     (GT findings missed by generated report)
#   Loc = Incorrect Location (correct finding, wrong anatomical site)
#   Sev = Incorrect Severity (correct finding, wrong severity/degree)
#   Trend = Incorrect Trend  (stable/worsening/improving described incorrectly)
#   Attr = Incorrect Attribute (wrong feature: size, etiology, pattern label)
AI_RADCLIQ = {
    "report_generation_92, valid_45_a_1.nii.gz":    {"FD":0,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_106, valid_52_a_1.nii.gz":   {"FD":2,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_150, valid_66_a_1.nii.gz":   {"FD":2,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_174, valid_79_a_1.nii.gz":   {"FD":0,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_443, valid_193_a_1.nii.gz":  {"FD":3,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_482, valid_209_a_1.nii.gz":  {"FD":0,"FO":5,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_553, valid_241_a_1.nii.gz":  {"FD":0,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_561, valid_245_a_1.nii.gz":  {"FD":3,"FO":2,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_696, valid_298_a_1.nii.gz":  {"FD":1,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_714, valid_307_a_1.nii.gz":  {"FD":1,"FO":0,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_850, valid_362_a_1.nii.gz":  {"FD":1,"FO":8,"Loc":0,"Sev":1,"Trend":0,"Attr":1},
    "report_generation_920, valid_391_a_1.nii.gz":  {"FD":3,"FO":6,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_1407, valid_589_a_1.nii.gz": {"FD":1,"FO":2,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1574, valid_666_a_1.nii.gz": {"FD":3,"FO":2,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_1596, valid_674_a_1.nii.gz": {"FD":1,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1610, valid_679_a_1.nii.gz": {"FD":2,"FO":2,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_1666, valid_707_a_1.nii.gz": {"FD":2,"FO":7,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_1670, valid_709_a_1.nii.gz": {"FD":0,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1689, valid_716_a_1.nii.gz": {"FD":0,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1752, valid_742_a_1.nii.gz": {"FD":0,"FO":1,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1812, valid_771_a_1.nii.gz": {"FD":1,"FO":6,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1988, valid_844_a_1.nii.gz": {"FD":0,"FO":4,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1992, valid_845_a_1.nii.gz": {"FD":0,"FO":4,"Loc":0,"Sev":1,"Trend":0,"Attr":1},
    "report_generation_2016, valid_852_a_1.nii.gz": {"FD":2,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_946, valid_406_a_1.nii.gz":  {"FD":0,"FO":3,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1030, valid_440_a_1.nii.gz": {"FD":3,"FO":0,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1128, valid_479_a_1.nii.gz": {"FD":3,"FO":2,"Loc":0,"Sev":0,"Trend":0,"Attr":1},
    "report_generation_1134, valid_482_a_1.nii.gz": {"FD":2,"FO":5,"Loc":0,"Sev":1,"Trend":0,"Attr":1},
    "report_generation_1190, valid_498_a_1.nii.gz": {"FD":3,"FO":1,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1210, valid_504_a_1.nii.gz": {"FD":2,"FO":4,"Loc":0,"Sev":1,"Trend":0,"Attr":1},
    "report_generation_1234, valid_515_a_1.nii.gz": {"FD":2,"FO":4,"Loc":0,"Sev":1,"Trend":0,"Attr":1},
    "report_generation_1249, valid_523_a_1.nii.gz": {"FD":0,"FO":6,"Loc":0,"Sev":0,"Trend":0,"Attr":0},
    "report_generation_1304, valid_544_a_1.nii.gz": {"FD":0,"FO":5,"Loc":1,"Sev":0,"Trend":0,"Attr":1},
}

# Also compute RadCliQ total error score (sum of all categories = overall error)
for k in AI_RADCLIQ:
    AI_RADCLIQ[k]["Total"] = sum(AI_RADCLIQ[k].values())

# ─── BLEU helpers (pure Python) ───────────────────────────────────────────────

def tokenize(text):
    return re.findall(r'\b[a-z]+\b', text.lower())

def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def clipped_precision(hyp_tokens, ref_tokens, n):
    hyp_ng = Counter(ngrams(hyp_tokens, n))
    ref_ng = Counter(ngrams(ref_tokens, n))
    clipped = sum(min(c, ref_ng[g]) for g, c in hyp_ng.items())
    total = max(sum(hyp_ng.values()), 1)
    return clipped / total

def brevity_penalty(hyp_len, ref_len):
    if hyp_len >= ref_len:
        return 1.0
    return math.exp(1 - ref_len / hyp_len) if hyp_len > 0 else 0.0

def bleu_n(hyp, ref, n=4):
    """Sentence-level BLEU-n with add-1 smoothing."""
    h = tokenize(hyp)
    r = tokenize(ref)
    if len(h) == 0:
        return 0.0
    precisions = []
    for k in range(1, n+1):
        cp = clipped_precision(h, r, k)
        # add-1 smoothing
        cp = (cp * len(h) + 1) / (len(h) + 1) if len(h) > 0 else 0
        precisions.append(math.log(cp) if cp > 0 else -999)
    bp = brevity_penalty(len(h), len(r))
    score = bp * math.exp(sum(precisions) / n)
    return round(score, 4)

# ─── ROUGE helpers (pure Python) ──────────────────────────────────────────────

def rouge_n(hyp, ref, n=1):
    h = tokenize(hyp)
    r = tokenize(ref)
    hyp_ng = Counter(ngrams(h, n))
    ref_ng = Counter(ngrams(r, n))
    matches = sum(min(c, ref_ng[g]) for g, c in hyp_ng.items())
    recall    = matches / max(sum(ref_ng.values()), 1)
    precision = matches / max(sum(hyp_ng.values()), 1)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return round(precision, 4), round(recall, 4), round(f1, 4)

def lcs_length(a, b):
    """DP LCS length."""
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return 0
    # Use 1-D DP to save memory
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(curr[j-1], prev[j])
        prev = curr
    return prev[n]

def rouge_l(hyp, ref):
    h = tokenize(hyp)
    r = tokenize(ref)
    lcs = lcs_length(h, r)
    recall    = lcs / max(len(r), 1)
    precision = lcs / max(len(h), 1)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return round(precision, 4), round(recall, 4), round(f1, 4)

# ─── Correlation helpers (numpy only) ─────────────────────────────────────────

def pearson(x, y):
    x, y = np.array(x, float), np.array(y, float)
    n = len(x)
    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0, 1.0
    r = np.corrcoef(x, y)[0, 1]
    # t-test p-value
    t = r * math.sqrt(n - 2) / math.sqrt(max(1 - r**2, 1e-12))
    from scipy_stub import t_pvalue
    return round(float(r), 4), round(t_pvalue(t, n - 2), 4)

def rank_array(x):
    x = np.array(x, float)
    n = len(x)
    sorted_idx = np.argsort(x)
    ranks = np.empty(n)
    i = 0
    while i < n:
        j = i
        while j < n - 1 and x[sorted_idx[j]] == x[sorted_idx[j+1]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1
        for k in range(i, j+1):
            ranks[sorted_idx[k]] = avg_rank
        i = j + 1
    return ranks

def spearman(x, y):
    rx, ry = rank_array(x), rank_array(y)
    return pearson(rx, ry)

def kendall_tau(x, y):
    x, y = np.array(x, float), np.array(y, float)
    n = len(x)
    concordant = discordant = 0
    for i in range(n):
        for j in range(i+1, n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            prod = dx * dy
            if prod > 0:
                concordant += 1
            elif prod < 0:
                discordant += 1
    tau = (concordant - discordant) / (n * (n-1) / 2)
    # variance for z-test (no ties adjustment for simplicity)
    var = (2 * (2*n + 5)) / (9 * n * (n-1))
    z = tau / math.sqrt(var)
    p = 2 * (1 - _norm_cdf(abs(z)))
    return round(tau, 4), round(p, 4)

def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ─── t-distribution p-value (pure Python, for pearson/spearman) ───────────────
# Simple approximation using regularized incomplete beta function
def _betai(a, b, x):
    if x < 0 or x > 1:
        return 0.0
    if x == 0 or x == 1:
        return float(x == 1)
    # Continued fraction (Lentz) — enough precision for p-value reporting
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1-x) * b - lbeta) / a
    # Use symmetry if needed
    if x > (a + 1) / (a + b + 2):
        return 1 - _betai(b, a, 1 - x)
    # Lentz CF
    FPMIN = 1e-30
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    if abs(d) < FPMIN: d = FPMIN
    d = 1/d; h = d
    for m in range(1, 201):
        m2 = 2*m
        aa = m * (b-m) * x / ((qam+m2) * (a+m2))
        d = 1 + aa*d; c = 1 + aa/c
        if abs(d) < FPMIN: d = FPMIN
        if abs(c) < FPMIN: c = FPMIN
        d = 1/d; h *= d*c
        aa = -(a+m) * (qab+m) * x / ((a+m2) * (qap+m2))
        d = 1 + aa*d; c = 1 + aa/c
        if abs(d) < FPMIN: d = FPMIN
        if abs(c) < FPMIN: c = FPMIN
        d = 1/d; delta = d*c; h *= delta
        if abs(delta-1) < 3e-7:
            break
    return front * h

def _t_pvalue(t, df):
    x = df / (df + t*t)
    p = _betai(df/2, 0.5, x)
    return min(p, 1.0)

# Monkey-patch so pearson/spearman can call it
import types, sys
_stub = types.ModuleType("scipy_stub")
_stub.t_pvalue = _t_pvalue
sys.modules["scipy_stub"] = _stub

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def compute_er2score(result):
    """Compute precision, recall, F1 from pipeline detailed results."""
    eval_res = result.get("evaluation_results", {})
    gm, gu, pm, pu = 0, 0, 0, 0
    for field, data in eval_res.items():
        gm += len(data["ground_truth"]["matched"])
        gu += len(data["ground_truth"]["unmatched"])
        pm += len(data["prediction"]["matched"])
        pu += len(data["prediction"]["unmatched"])
    prec = pm / (pm + pu) if (pm + pu) > 0 else 0.0
    rec  = gm / (gm + gu) if (gm + gu) > 0 else 0.0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return round(prec, 4), round(rec, 4), round(f1, 4)

def correlate(metric_vals, error_vals, metric_name, cat_name):
    x = np.array(metric_vals, float)
    y = np.array(error_vals, float)
    if np.std(y) < 1e-9:
        return {
            "note": "zero variance in RadCliQ scores — correlation undefined",
            "pearson":    {"r": 0.0, "p": 1.0},
            "spearman":   {"r": 0.0, "p": 1.0},
            "kendall_tau":{"tau": 0.0, "p": 1.0},
        }
    pr, pp = pearson(x, y)
    sr, sp = spearman(x, y)
    kt, kp = kendall_tau(x, y)
    return {
        "pearson":    {"r": pr, "p": pp},
        "spearman":   {"r": sr, "p": sp},
        "kendall_tau":{"tau": kt, "p": kp},
    }

def main():
    print("=" * 70)
    print("TASK 3 — CT-RATE FULL EVALUATION")
    print("=" * 70)

    # 1. Load reports
    with open(REPORTS_JSON, encoding="utf-8") as f:
        reports = json.load(f)
    reports_by_id = {r["id"]: r for r in reports}

    # 2. Load ER2SCORE pipeline results
    with open(DETAILED_JSON, encoding="utf-8") as f:
        detailed = json.load(f)
    er2_by_id = {r["source_file"]: r for r in detailed}

    # 3. Compute all per-report metrics
    CATS = ["FD", "FO", "Loc", "Sev", "Trend", "Attr", "Total"]
    per_report = []

    print(f"\n{'ID':<45} | {'Prec':>6} | {'Rec':>6} | {'F1':>6} | {'BLEU1':>6} | {'BLEU4':>6} | {'R1-F1':>6} | {'RL-F1':>6} | FD FO Lo Sv Tr At Tot")
    print("-" * 135)

    for rid, rc in AI_RADCLIQ.items():
        rep = reports_by_id.get(rid)
        er2 = er2_by_id.get(rid)

        if rep is None or er2 is None:
            print(f"  SKIP (missing data): {rid}")
            continue

        gen = rep["generated"]
        gt  = rep["ground_truth"]

        # ER2SCORE
        prec, rec, f1 = compute_er2score(er2)

        # BLEU
        b1 = bleu_n(gen, gt, n=1)
        b2 = bleu_n(gen, gt, n=2)
        b4 = bleu_n(gen, gt, n=4)

        # ROUGE
        r1p, r1r, r1f = rouge_n(gen, gt, 1)
        r2p, r2r, r2f = rouge_n(gen, gt, 2)
        rlp, rlr, rlf = rouge_l(gen, gt)

        short_id = rid.split(",")[0].replace("report_generation_", "r")
        print(f"{short_id:<45} | {prec:>6.3f} | {rec:>6.3f} | {f1:>6.3f} | {b1:>6.3f} | {b4:>6.3f} | {r1f:>6.3f} | {rlf:>6.3f} | {rc['FD']:2} {rc['FO']:2} {rc['Loc']:2} {rc['Sev']:2} {rc['Trend']:2} {rc['Attr']:2} {rc['Total']:3}")

        per_report.append({
            "id": rid,
            "ER2SCORE_Precision": prec,
            "ER2SCORE_Recall":    rec,
            "ER2SCORE_F1":        f1,
            "BLEU_1": b1, "BLEU_2": b2, "BLEU_4": b4,
            "ROUGE_1_P": r1p, "ROUGE_1_R": r1r, "ROUGE_1_F1": r1f,
            "ROUGE_2_P": r2p, "ROUGE_2_R": r2r, "ROUGE_2_F1": r2f,
            "ROUGE_L_P": rlp, "ROUGE_L_R": rlr, "ROUGE_L_F1": rlf,
            **{f"RadCliQ_{c}": rc[c] for c in CATS},
        })

    n = len(per_report)
    print(f"\nTotal reports evaluated: {n}")

    # 4. Aggregate means
    print("\n" + "=" * 70)
    print("AGGREGATE MEANS")
    print("=" * 70)
    def mean(key):
        return round(np.mean([r[key] for r in per_report]), 4)

    metrics_summary = {
        "ER2SCORE_F1":   mean("ER2SCORE_F1"),
        "BLEU_1":        mean("BLEU_1"),
        "BLEU_2":        mean("BLEU_2"),
        "BLEU_4":        mean("BLEU_4"),
        "ROUGE_1_F1":    mean("ROUGE_1_F1"),
        "ROUGE_2_F1":    mean("ROUGE_2_F1"),
        "ROUGE_L_F1":    mean("ROUGE_L_F1"),
        "RadCliQ_Total": mean("RadCliQ_Total"),
    }
    for k, v in metrics_summary.items():
        print(f"  {k:<22}: {v:.4f}")

    # 5. Correlations
    print("\n" + "=" * 70)
    print("CORRELATIONS  (metric vs. RadCliQ error — negative = better metric)")
    print("=" * 70)

    METRIC_KEYS = ["ER2SCORE_F1", "BLEU_1", "BLEU_4", "ROUGE_1_F1", "ROUGE_L_F1"]
    ERROR_CATS  = ["FD", "FO", "Loc", "Sev", "Trend", "Attr", "Total"]

    all_correlations = {}
    for mk in METRIC_KEYS:
        all_correlations[mk] = {}
        metric_vals = [r[mk] for r in per_report]
        print(f"\n  ── {mk} ──")
        print(f"  {'Category':<8} | {'Pearson r':>10} {'p':>7} | {'Spearman r':>11} {'p':>7} | {'Kendall τ':>10} {'p':>7}")
        print(f"  {'-'*8}-+-{'-'*10}-{'-'*7}-+-{'-'*11}-{'-'*7}-+-{'-'*10}-{'-'*7}")
        for cat in ERROR_CATS:
            err_vals = [r[f"RadCliQ_{cat}"] for r in per_report]
            res = correlate(metric_vals, err_vals, mk, cat)
            all_correlations[mk][cat] = res
            if "note" in res:
                print(f"  {cat:<8} | {'zero variance':>33}")
            else:
                pr = res["pearson"]
                sr = res["spearman"]
                kt = res["kendall_tau"]
                print(f"  {cat:<8} | {pr['r']:>10.4f} {pr['p']:>7.4f} | {sr['r']:>11.4f} {sr['p']:>7.4f} | {kt['tau']:>10.4f} {kt['p']:>7.4f}")

    # 6. Save outputs
    import csv

    # CSV
    csv_path = os.path.join(OUT_DIR, "task3_full_results.csv")
    if per_report:
        fieldnames = list(per_report[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(per_report)

    # JSON
    json_path = os.path.join(OUT_DIR, "task3_full_results.json")
    output = {
        "n_reports": n,
        "aggregate_means": metrics_summary,
        "per_report": per_report,
        "correlations": all_correlations,
        "ai_radcliq_scores": AI_RADCLIQ,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅  Results saved:")
    print(f"    CSV  → {csv_path}")
    print(f"    JSON → {json_path}")
    return output

if __name__ == "__main__":
    results = main()
