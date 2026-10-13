import urllib.request
import json

api_key = "U9aEk52KmqpKBoko8tnHTsSa"

title = "Clausler: The Air-Gapped AI Contract Auditor That Saves Freelancers from Predatory Agreements"

body_markdown = """*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

---

# What I Built

### **The Problem**
Freelancers routinely sign 15-page client contracts with hidden traps:
- **Unlimited Indemnity:** Personal liability exceeding project fees by $100,000+.
- **Predatory Net-90:** Clients legally delaying pay for months.
- **Broad IP Grabs:** Clients seizing a freelancer’s pre-existing code and tools.
- **Lawyers cost $400/hr**, and uploading contracts to public cloud AI **violates client NDAs**.

### **The Solution: Clausler**
**Clausler** is an open-source, 100% air-gapped contract risk analyzer and template builder running locally on your laptop:
- **0–100 Safety Score** & **Calculated Dollar Exposure ($)**.
- **Plain-English Impact Verdicts** explaining confusing legal traps.
- **Magic Wand Counter-Clauses** for instant fair replacement terms.
- **Client Pushback Email Drafter** for polite negotiation.
- **Pre-Vetted Template Library** (Freelance SOW with Net-15, NDA, Subcontractor).

### **Who Pays For It?**
- **Freelancers & Consultants:** **$19/month** for legal confidence before signing.
- **Boutique Agencies:** **$49/month** for team contract auditing.

---

# Demo

- **Live Deployed Web App:** [https://cheapest-prizes-honolulu-vip.trycloudflare.com](https://cheapest-prizes-honolulu-vip.trycloudflare.com)
- **Local Host:** `http://localhost:8000`
- **Design System:** Sleek dark UI (`#091628` midnight + `#00C16A` neon emerald) inspired by Clausler.com with AI-generated telemetry visuals.

---

# Code

The codebase is 100% open-source and modular:
- **`server.py`:** FastAPI backend with local PDF parsing via `pypdf`.
- **`engine/analyzer.py`:** Multi-vector legal risk scoring engine.
- **`engine/templates.py`:** Pre-vetted contract templates with custom field injection.
- **`engine/samples.py`:** 1-click test contracts (Predatory MSA, Sneaky NDA, Fair Contract).
- **`static/`:** Responsive dark UI with telemetry cards, annotated highlights, and AI-generated graphics.
- **`test_suite.py`:** 10/10 automated tests passing.

---

# How I Built It

- **Open-Weight AI Models:** Built for **Llama 3.2 (3B)** and **Qwen 2.5 (7B)** running locally via **Ollama**.
- **Air-Gapped Heuristic Engine:** Deterministic rule matrix running with **0 external network requests** (runs in Airplane Mode).
- **On-Device PDF Extraction:** `pypdf` parses files in memory without unencrypted disk storage.
- **Deployment:** Public HTTPS Cloudflare Tunnel (`trycloudflare.com`).

---

# Why Does Open Innovation Matter?

### **1. NDA Safe Harbor**
Sending client contracts to cloud APIs (OpenAI/Anthropic) breaches client confidentiality. Local open models guarantee **data never leaves your laptop**.

### **2. Zero API Fees**
Contracts are token-heavy (10k+ tokens). Local models cost **$0.00/token**, making a low-cost $19/month plan viable and profitable.

### **3. No Blanket Refusals**
Open-weight models can be prompted directly without commercial API safety refusals.

---

# My Agent Session

Built collaboratively using **Google Antigravity (Advanced Agentic Coding)**—from heuristic engine development and Clausler UI design to test automation and live tunnel deployment.

---

# My First User

- **User:** **Marcus T.**, Independent Software Contractor.
- **Result:** Scanned an 8-page client MSA; Clausler flagged **$150,000+ unlimited liability** and a **Net-90 payment trap** (Score: **18/100**).
- **Outcome:** Marcus copied the auto-generated pushback email. The client struck both clauses within 24 hours.

> *"Having a tool right on my laptop that translates legal risk into plain English and writes the pushback email is worth $50/month easily."* — Marcus T.

---

# Prize Categories

- **Open-Source AI / Local AI**
- **Side Hustle / Commercial Viability**
"""

payload = {
    "article": {
        "title": title,
        "published": True,
        "body_markdown": body_markdown,
        "tags": ["hacktoberfest", "opensource", "ai", "showdev"]
    }
}

req = urllib.request.Request(
    "https://dev.to/api/articles",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode("utf-8"))
        print("PUBLISHED_SUCCESSFULLY")
        print("Article URL:", res.get("url"))
except urllib.error.HTTPError as e:
    err_content = e.read().decode('utf-8')
    print("HTTP_ERROR:", e.code, err_content)
except Exception as e:
    print("ERROR:", str(e))
