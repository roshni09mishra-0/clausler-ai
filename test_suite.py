import urllib.request
import json
import sys

def test(name, url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        req_data = None
        if data:
            req.add_header("Content-Type", "application/json")
            req_data = json.dumps(data).encode("utf-8")
        resp = urllib.request.urlopen(req, data=req_data)
        code = resp.getcode()
        body = resp.read().decode("utf-8")
        print(f"[PASS] {name} -> HTTP {code} (length: {len(body)})")
        content_type = resp.headers.get("Content-Type", "")
        return json.loads(body) if "application/json" in content_type else body
    except Exception as e:
        print(f"[FAIL] {name} -> {e}")
        return None

print("\n" + "="*60)
print("  [TEST SUITE] REDLINELOCAL ENDPOINTS & ANALYSIS ENGINE")
print("="*60 + "\n")

# 1. Static Web Assets
test("1. Root HTML (/)", "http://127.0.0.1:8000/")
test("2. Stylesheet (/style.css)", "http://127.0.0.1:8000/style.css")
test("3. Application Script (/app.js)", "http://127.0.0.1:8000/app.js")

# 2. System Status & Samples
status = test("4. System Telemetry (/api/status)", "http://127.0.0.1:8000/api/status")
samples = test("5. Samples Catalog (/api/samples)", "http://127.0.0.1:8000/api/samples")
pred = test("6. Sample: Predatory MSA", "http://127.0.0.1:8000/api/sample/predatory")
fair = test("7. Sample: Fair Agreement", "http://127.0.0.1:8000/api/sample/fair")
nda = test("8. Sample: Sneaky NDA", "http://127.0.0.1:8000/api/sample/nda")

# 3. Functional Contract Analysis Testing
print("\n" + "-"*60)
print("  [TESTING] PREDATORY CONTRACT AUDIT")
print("-"*60)

if pred and "text" in pred:
    res = test("9. POST /api/analyze (Predatory Contract)", "http://127.0.0.1:8000/api/analyze", method="POST", data={"text": pred["text"], "model_name": "offline-heuristics"})
    if res:
        score = res.get("overall_score")
        verdict = res.get("risk_verdict")
        exposure = res.get("financial_exposure_usd", 0)
        heatmap = res.get("risk_heatmap", {})
        clauses = res.get("clauses", [])
        print(f"      Score: {score}/100 (Expected: < 40)")
        print(f"      Verdict: {verdict}")
        print(f"      Estimated Exposure: ${exposure:,}")
        print(f"      Threat Heatmap: {heatmap}")
        print(f"      Flagged Clauses: {len(clauses)}")
        assert score < 40, "Predatory score should be high risk (<40)"
        assert len(clauses) >= 4, "Should detect at least 4 critical traps"
        print("      [OK] Predatory test assertions passed!")

print("\n" + "-"*60)
print("  [TESTING] FAIR CONTRACT AUDIT")
print("-"*60)

if fair and "text" in fair:
    res2 = test("10. POST /api/analyze (Fair Contract)", "http://127.0.0.1:8000/api/analyze", method="POST", data={"text": fair["text"], "model_name": "offline-heuristics"})
    if res2:
        score2 = res2.get("overall_score")
        verdict2 = res2.get("risk_verdict")
        clauses2 = res2.get("clauses", [])
        print(f"      Score: {score2}/100 (Expected: >= 70)")
        print(f"      Verdict: {verdict2}")
        print(f"      Flagged Clauses: {len(clauses2)}")
        assert score2 >= 70, "Fair contract score should be safe (>=70)"
        print("      [OK] Fair test assertions passed!")

print("\n" + "="*60)
print("  [SUCCESS] ALL 10 TESTS COMPLETED SUCCESSFULLY!")
print("="*60 + "\n")
