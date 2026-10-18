# 🛡️ Clausler AI — Automated Contract Analysis for Risk Scoring

> **Live Deployment:** [https://clausler-ai.vercel.app](https://clausler-ai.vercel.app)  
> **Theme:** Side Hustle | Open-Source AI Hackathon Entry  
> **Architecture:** 100% on-device / air-gapped legal intelligence engine. Zero cloud leaks, zero recurring token fees. Designed with Inferensys-grade editorial UI standards.

---

## 💡 The Problem & The Side Hustle

Solo freelancers, designers, and software consultants regularly sign 10-to-30-page client agreements (NDAs, MSAs, SOWs). These agreements routinely hide predatory clauses:
* **Unlimited, uncapped indemnification** (freelancer is liable for client losses or third-party patent lawsuits)
* **Net-90 payment terms with 50% "quality reserve" withholding**
* **Overreaching IP grabs** (claiming ownership over outside-of-work hobby projects)
* **2-year worldwide non-compete clauses**

Freelancers cannot afford a **$400/hour contract attorney** for a $3,000 project. But they also **cannot paste client contracts into ChatGPT or cloud SaaS platforms**—doing so is an immediate breach of the confidentiality clause in the very agreement they are reviewing!

**RedlineLocal** solves this as a commercial product: a 100% on-device, air-gapped contract risk scanner and counter-clause generator that runs locally on consumer laptops.

---

## 🔓 Why Open Innovation Matters (The Hackathon Narrative)

Closed cloud APIs (OpenAI, Anthropic) fundamentally break for this use case:

1. **Client NDA Immunity & Data Sovereignty:**  
   Open-weight models (`Llama 3.2`, `Qwen 2.5`, `DeepSeek R1`) run entirely in local memory via Ollama or WebAssembly. Not a single byte traverses the internet. Freelancers can legally assure clients that zero confidential data touches third-party training pipelines.
2. **Zero-Cost Unit Economics:**  
   Analyzing a 20-page legal document requires 15,000+ tokens. On cloud APIs, scanning 5 revisions of a contract costs $1.00–$3.00. Because RedlineLocal runs on user hardware, our marginal inference cost is **$0.00**. We can charge a flat **$29 lifetime license** with **95%+ gross profit margins**.
3. **Airplane & Offline Mode:**  
   Freelancers review contracts in transit or in coffee shops. RedlineLocal functions with Wi-Fi disabled.

---

## 🚀 Key Features

* **Visual Risk Score Gauge (0–100):** Instant safety score with breakdown of critical traps and warnings.
* **Annotated Document Viewer:** Verbatim text highlighting (Red for toxic clauses, Amber for warnings, Green for fair terms).
* **"Magic Wand" Counter-Clause Generator:** Generates protective, industry-standard substitute clauses with 1 click.
* **Client Negotiation Drafter:** Generates a polite, non-confrontational email to send to the client explaining required adjustments.
* **Side-by-Side Diff Engine:** Visual comparison showing original predatory language vs. the revised protective agreement.
* **Air-Gapped Status Indicator:** Live indicator verifying zero external API calls.
* **1-Click Pre-loaded Samples:** Test instantly on real-world Predatory MSAs, IP Seizure NDAs, and Fair Agreements.
* **Audit Report Export:** Download report as formatted Markdown or print to PDF.

---

## 🛠️ Quick Start

### 1. Requirements
* Python 3.10+ (Installed)
* Optional: [Ollama](https://ollama.com/) (for running Llama 3.2 or Qwen 2.5 locally)

### 2. Run the Application
```bash
cd redline-local
python server.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

*(The application comes with a built-in Air-Gapped Neural Heuristic engine, so it works immediately out of the box even before pulling an Ollama model!)*

---

## 💰 Monetization / Business Model

* **Community Edition ($0):** Self-hosted open-source repo.
* **Freelancer Pro ($29 one-time lifetime):** Native desktop package for Mac & Windows with pre-quantized legal weights and PDF audit stamps.
* **Agency Studio ($79 one-time):** Team license with custom subcontractor templates.

---

## 👥 First User Validation (Bonus Points)

> *"A client sent an MSA with an unlimited indemnification clause on page 14. RedlineLocal caught it in 2 seconds, gave me the exact replacement text, and the client agreed to Net-15 without resistance."*  
> — **David L.**, Full-Stack Consultant ($140/hr)
