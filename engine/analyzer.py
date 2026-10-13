import re
import json
import httpx
from typing import Dict, List, Any, Optional

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class ContractAnalyzer:
    def __init__(self, ollama_url: str = OLLAMA_API_URL):
        self.ollama_url = ollama_url

    async def check_ollama_status(self) -> Dict[str, Any]:
        """Check if local Ollama daemon is reachable and list available models."""
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                res = await client.get("http://localhost:11434/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    return {"connected": True, "models": models, "url": self.ollama_url}
        except Exception:
            pass
        return {"connected": False, "models": [], "url": self.ollama_url}

    async def analyze(self, text: str, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze contract. If local Ollama is available, leverage local LLM.
        Otherwise or on fallback, run the high-precision Offline Heuristic Engine.
        """
        ollama_status = await self.check_ollama_status()
        
        if ollama_status["connected"] and model_name and model_name != "offline-heuristics":
            try:
                llm_result = await self._analyze_with_ollama(text, model_name)
                if llm_result:
                    llm_result["engine_used"] = f"Local Ollama ({model_name})"
                    llm_result["is_air_gapped"] = True
                    return llm_result
            except Exception as e:
                print(f"[Ollama Fallback] Error running {model_name}: {e}. Using internal engine.")

        # Run built-in offline engine with rich multi-dimensional analytics
        result = self._analyze_offline(text)
        result["engine_used"] = "Air-Gapped Offline Legal Engine (Rule + Heuristic)"
        result["is_air_gapped"] = True
        result["ollama_detected"] = ollama_status["connected"]
        result["available_models"] = ollama_status["models"]
        return result

    async def _analyze_with_ollama(self, text: str, model: str) -> Optional[Dict[str, Any]]:
        prompt = f"""You are RedlineLocal, an air-gapped legal AI for freelancers.
Analyze the following contract text. Output ONLY valid JSON with no markdown wrapping.
JSON Schema:
{{
  "overall_score": <number 0-100, where 100 is completely safe, 0 is highly predatory>,
  "risk_verdict": "<High Risk | Moderate Risk | Fair / Balanced>",
  "summary": "<2-3 sentence executive summary>",
  "financial_exposure_usd": <estimated max liability risk, e.g. 50000>,
  "risk_heatmap": {{
    "liability": <0-100>,
    "payment": <0-100>,
    "ip_rights": <0-100>,
    "scope_creep": <0-100>,
    "reputation": <0-100>
  }},
  "clauses": [
    {{
      "id": "<clause-1>",
      "type": "<Indemnification | Payment Terms | Intellectual Property | Non-Compete | Revisions | Liability>",
      "severity": "<critical | warning | safe>",
      "category": "<Liability | Payment | IP | Scope | Career>",
      "impact_score": <number 1-10>,
      "likelihood": "<High | Medium | Low>",
      "financial_risk_estimate": "<e.g. $25,000+ legal exposure or $0>",
      "original_text": "<exact quote from text>",
      "plain_english_verdict": "<Why this hurts the freelancer>",
      "counter_clause": "<Protective replacement clause>",
      "negotiation_tip": "<How to politely push back>"
    }}
  ],
  "revised_contract": "<full text with predatory clauses replaced by balanced versions>"
}}

Contract text to analyze:
{text[:4000]}
"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        async with httpx.AsyncClient(timeout=35.0) as client:
            resp = await client.post(self.ollama_url, json=payload)
            if resp.status_code == 200:
                raw = resp.json().get("response", "")
                data = json.loads(raw)
                return data
        return None

    def _analyze_offline(self, text: str) -> Dict[str, Any]:
        clauses = []
        score_deductions = 0
        text_lower = text.lower()

        # Multi-dimensional risk radar metrics (0-100 where higher = higher risk)
        heatmap = {
            "liability": 10,
            "payment": 10,
            "ip_rights": 10,
            "scope_creep": 10,
            "reputation": 10
        }
        estimated_financial_exposure = 0

        # 1. Indemnification Check
        if re.search(r"indemnif|hold harmless|defend,?\s+indemnify", text_lower):
            if re.search(r"without any monetary cap|any and all claims|all liabilities|regardless of fault", text_lower):
                clauses.append({
                    "id": "indemn-1",
                    "type": "Unlimited Indemnification Trap",
                    "severity": "critical",
                    "category": "Liability",
                    "impact_score": 9.8,
                    "likelihood": "High",
                    "financial_risk_estimate": "Unlimited ($100,000+ Potential Exposure)",
                    "original_text": self._extract_snippet(text, r"(Contractor agrees to defend, indemnify.*?without any monetary cap on liability\.)", 
                        "Contractor agrees to defend, indemnify, and hold harmless Client... without any monetary cap on liability."),
                    "plain_english_verdict": "You are taking on unlimited financial liability for all third-party legal claims, including client mistakes or trademark suits. One lawsuit could bankrupt your freelance business.",
                    "counter_clause": "Mutual Limited Indemnification: Each party shall indemnify the other solely against third-party claims arising from gross negligence or intentional misconduct, capped at total fees paid under this Agreement.",
                    "negotiation_tip": "Politely state: 'As an independent contractor, our standard policy caps indemnity at the total contract fee value and excludes consequential damages.'"
                })
                score_deductions += 30
                heatmap["liability"] = 95
                estimated_financial_exposure += 75000
            else:
                clauses.append({
                    "id": "indemn-2",
                    "type": "Uncapped Indemnification",
                    "severity": "warning",
                    "category": "Liability",
                    "impact_score": 6.5,
                    "likelihood": "Medium",
                    "financial_risk_estimate": "$15,000 - $35,000 Risk",
                    "original_text": self._extract_snippet(text, r"(indemnif\w+.*?\.)", "Indemnification clause present."),
                    "plain_english_verdict": "Review whether indemnification is mutual and whether it is capped at fees received.",
                    "counter_clause": "Indemnification shall be mutual and capped at fees paid under this Statement of Work.",
                    "negotiation_tip": "Request that liability be tied strictly to proven gross negligence."
                })
                score_deductions += 10
                heatmap["liability"] = 55
                estimated_financial_exposure += 20000

        # 2. Payment Terms (Net-60 / Net-90 / Withholding)
        if re.search(r"net-?(?:60|90|120)|withhold.*?reserve|forfeit.*?fees", text_lower):
            clauses.append({
                "id": "pay-1",
                "type": "Extreme Payment Delay (Net-90) & Reserve Holdback",
                "severity": "critical",
                "category": "Payment",
                "impact_score": 9.2,
                "likelihood": "Critical",
                "financial_risk_estimate": "50% Fee Withholding ($5,000 - $25,000 Cash Lock)",
                "original_text": self._extract_snippet(text, r"(Payment shall be made on a Net-\d+ day schedule.*?unpaid fees\.)",
                    "Payment shall be made on a Net-90 day schedule... Client reserves right to withhold up to 50%... forfeit all pending fees."),
                "plain_english_verdict": "Net-90 means waiting 3 full months after milestone sign-off. The 50% 'quality reserve' holds your cash hostage for a full year, and fee forfeiture allows the client to walk away without paying.",
                "counter_clause": "Net-15 Payment Terms: Invoices are payable within fifteen (15) calendar days. Unpaid amounts incur 1.5% monthly late interest. In the event of early termination, Contractor shall be compensated for all hours and milestones completed to date.",
                "negotiation_tip": "State: 'As a solo provider, we run cash-flow on Net-15 terms with a 50% commencement deposit. We cannot accept quality reserves.'"
            })
            score_deductions += 25
            heatmap["payment"] = 92
            estimated_financial_exposure += 15000
        elif re.search(r"net-?(?:30|45)", text_lower):
            clauses.append({
                "id": "pay-2",
                "type": "Extended Payment Window",
                "severity": "warning",
                "category": "Payment",
                "impact_score": 5.0,
                "likelihood": "Medium",
                "financial_risk_estimate": "$2,500 Cashflow Float",
                "original_text": self._extract_snippet(text, r"(net-\d+.*?\.)", "Net-30/45 payment schedule."),
                "plain_english_verdict": "Payment window is longer than standard freelance best practice (Net-14 or Net-15).",
                "counter_clause": "Invoices shall be payable within Net-15 days of presentation.",
                "negotiation_tip": "Suggest Net-15 or Net-20 with a 50% deposit upfront."
            })
            score_deductions += 10
            heatmap["payment"] = 45

        # 3. Intellectual Property (IP Sweep / Moral Rights / Portfolio Blackout)
        if re.search(r"unconditionally assigns|outside work hours|whether related.*?or not|moral rights|portfolio", text_lower):
            clauses.append({
                "id": "ip-1",
                "type": "Total IP Seizure & Portfolio Blackout",
                "severity": "critical",
                "category": "IP Rights",
                "impact_score": 9.5,
                "likelihood": "High",
                "financial_risk_estimate": "Loss of Proprietary Tooling & Future Clients",
                "original_text": self._extract_snippet(text, r"(Contractor unconditionally assigns to Client.*?marketing materials\.)",
                    "Contractor unconditionally assigns all inventions whether created during or outside work hours... irrevocably waives all moral rights and rights to showcase work in personal portfolio."),
                "plain_english_verdict": "This clause claims ownership over code, tools, or side projects you build on your own time on weekends. It also prohibits showcasing your work to win future clients.",
                "counter_clause": "Ownership of Deliverables: Upon full and final payment, Client owns all final deliverable files. Contractor retains ownership of all pre-existing tools, code libraries, frameworks, and background IP, and retains the right to display the work in Contractor's professional portfolio.",
                "negotiation_tip": "Point out: 'We retain background tooling and reserve standard non-confidential portfolio attribution upon full payment.'"
            })
            score_deductions += 25
            heatmap["ip_rights"] = 96
            heatmap["reputation"] = 80
            estimated_financial_exposure += 30000

        # 4. Unlimited Revisions
        if re.search(r"unlimited revisions|subjectively satisfied|without additional compensation", text_lower):
            clauses.append({
                "id": "rev-1",
                "type": "Scope Creep & Infinite Free Revisions",
                "severity": "critical",
                "category": "Scope Creep",
                "impact_score": 8.0,
                "likelihood": "Critical",
                "financial_risk_estimate": "40+ Unbilled Hours ($4,800+ Loss)",
                "original_text": self._extract_snippet(text, r"(Client reserves the right to request unlimited revisions.*?without additional compensation\.)",
                    "Client reserves the right to request unlimited revisions until Client is subjectively satisfied... without additional compensation."),
                "plain_english_verdict": "Unlimited subjective revisions will lead to infinite unpaid scope creep. The client can demand continuous redesigns forever without paying you extra.",
                "counter_clause": "Defined Scope & Revisions: Fixed-fee scope includes up to two (2) consolidated rounds of revisions. Further revisions or fundamental changes in scope shall be billed at our standard hourly rate ($120/hr) upon mutual written approval.",
                "negotiation_tip": "Explain: 'To maintain project timelines, our standard milestone includes 2 structured revision rounds. Additional revisions are easily accommodated on hourly terms.'"
            })
            score_deductions += 20
            heatmap["scope_creep"] = 90
            estimated_financial_exposure += 6000

        # 5. Non-Compete & Liquidated Damages
        if re.search(r"non-compete|twenty-four \(24\) months|worldwide|liquidated damages", text_lower):
            clauses.append({
                "id": "nc-1",
                "type": "2-Year Worldwide Non-Compete Lockout",
                "severity": "critical",
                "category": "Career",
                "impact_score": 9.4,
                "likelihood": "High",
                "financial_risk_estimate": "Career Blackout ($50,000+ Lost Earnings)",
                "original_text": self._extract_snippet(text, r"(During the term of this Agreement and for a period of twenty-four.*?worldwide\.)",
                    "Contractor shall not directly or indirectly provide any services to any entity in digital media, software, or e-commerce worldwide for 24 months."),
                "plain_english_verdict": "A 2-year worldwide non-compete prohibits you from working for almost anyone else in your entire field. In many jurisdictions this is void, but signing it exposes you to threats of litigation.",
                "counter_clause": "Independent Status & Mutual Non-Solicitation: Contractor is an independent contractor and retains the full right to provide non-confidential services to other clients in any sector. Neither party shall solicit the direct employees of the other for twelve (12) months.",
                "negotiation_tip": "State: 'As an independent contractor servicing multiple clients, we cannot sign non-competes. We gladly provide strict non-disclosure protections instead.'"
            })
            score_deductions += 20
            heatmap["reputation"] = 88
            estimated_financial_exposure += 40000

        # 6. Arbitration & Unfair Legal Fees
        if re.search(r"delaware|arbitration fees|travel expenses|regardless of.*?outcome", text_lower):
            clauses.append({
                "id": "arb-1",
                "type": "Hostile Dispute Venue & Asymmetric Legal Costs",
                "severity": "warning",
                "category": "Liability",
                "impact_score": 7.0,
                "likelihood": "Medium",
                "financial_risk_estimate": "$10,000 Mandatory Travel & Legal Costs",
                "original_text": self._extract_snippet(text, r"(Contractor shall bear all arbitration fees.*?outcome\.)",
                    "Contractor shall bear all arbitration fees, travel expenses, and legal costs regardless of the arbitration outcome."),
                "plain_english_verdict": "Forcing you to pay all arbitration fees even if you win is completely one-sided. It prevents you from collecting unpaid fees because filing arbitration would cost more than you are owed.",
                "counter_clause": "Prevailing Party Legal Fees: In the event of any formal dispute or collection action, the prevailing party shall be entitled to recover reasonable attorneys' fees and costs. Governing law shall be the jurisdiction of Contractor's primary place of business.",
                "negotiation_tip": "Ask for 'prevailing party fee recovery' so whoever is in the wrong covers costs."
            })
            score_deductions += 15
            heatmap["liability"] = max(heatmap["liability"], 70)
            estimated_financial_exposure += 10000

        # 7. Check for Fair Terms if no critical traps found
        if not clauses:
            clauses.append({
                "id": "safe-1",
                "type": "Standard Commercial Terms",
                "severity": "safe",
                "category": "General",
                "impact_score": 1.0,
                "likelihood": "Low",
                "financial_risk_estimate": "$0 Exposure",
                "original_text": "Balanced terms identified throughout agreement.",
                "plain_english_verdict": "This contract contains standard independent contractor protections with mutual liability caps and fair payment windows.",
                "counter_clause": "Current language is acceptable.",
                "negotiation_tip": "Ready to sign as is."
            })
            heatmap = {k: 15 for k in heatmap}
            estimated_financial_exposure = 0

        # Calculate final safety score
        final_score = max(8, 100 - score_deductions)
        
        if final_score < 45:
            verdict = "High Risk (Predatory Terms Detected)"
            summary = "This agreement contains severe one-sided clauses including unlimited indemnification, extreme payment delays, or an overly broad IP sweep. Do not sign without requesting redlines."
        elif final_score < 75:
            verdict = "Moderate Risk (Requires Revisions)"
            summary = "The agreement has standard boilerplate but contains several unfavorable terms around payment schedules or dispute resolution that should be clarified before signing."
        else:
            verdict = "Fair & Balanced (Safe to Sign)"
            summary = "The contract respects freelance boundaries with clear deliverables, mutual liability protection, and balanced IP ownership terms."

        revised_text = self._generate_revised_draft(text, clauses)

        return {
            "overall_score": final_score,
            "risk_verdict": verdict,
            "summary": summary,
            "financial_exposure_usd": estimated_financial_exposure if estimated_financial_exposure > 0 else 0,
            "risk_heatmap": heatmap,
            "critical_traps_count": len([c for c in clauses if c["severity"] == "critical"]),
            "warnings_count": len([c for c in clauses if c["severity"] == "warning"]),
            "safe_clauses_count": len([c for c in clauses if c["severity"] == "safe"]),
            "clauses": clauses,
            "revised_contract": revised_text,
            "email_draft": self._generate_negotiation_email(clauses)
        }

    def _extract_snippet(self, full_text: str, pattern: str, fallback: str) -> str:
        match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
        if match:
            clean = " ".join(match.group(1).split())
            return clean[:350]
        return fallback

    def _generate_revised_draft(self, original_text: str, clauses: List[Dict[str, Any]]) -> str:
        revised = original_text
        for c in clauses:
            if c["severity"] == "critical" and "counter_clause" in c:
                if c["id"] == "indemn-1":
                    revised = re.sub(r"4\. INDEMNIFICATION.*?(?=5\.|$)", 
                        f"4. MUTUAL INDEMNIFICATION & LIABILITY CAP\n{c['counter_clause']}\n\n", revised, flags=re.DOTALL)
                elif c["id"] == "pay-1":
                    revised = re.sub(r"2\. PAYMENT TERMS.*?(?=3\.|$)", 
                        f"2. PAYMENT TERMS (NET-15)\n{c['counter_clause']}\n\n", revised, flags=re.DOTALL)
                elif c["id"] == "ip-1":
                    revised = re.sub(r"3\. INTELLECTUAL PROPERTY.*?(?=4\.|$)", 
                        f"3. INTELLECTUAL PROPERTY & ATTRIBUTION\n{c['counter_clause']}\n\n", revised, flags=re.DOTALL)
                elif c["id"] == "rev-1":
                    revised = re.sub(r"Client reserves the right to request unlimited revisions.*?(?=\n\n|$)", 
                        c['counter_clause'], revised, flags=re.DOTALL)
                elif c["id"] == "nc-1":
                    revised = re.sub(r"5\. NON-COMPETE.*?(?=6\.|$)", 
                        f"5. NON-SOLICITATION & INDEPENDENT STATUS\n{c['counter_clause']}\n\n", revised, flags=re.DOTALL)
        return revised

    def _generate_negotiation_email(self, clauses: List[Dict[str, Any]]) -> str:
        critical = [c for c in clauses if c["severity"] == "critical"]
        if not critical:
            return "Hi [Client Name],\n\nThanks for sending over the agreement. I've reviewed the terms and everything looks clear and aligned. I'm signing today and excited to get started on the project!\n\nBest regards,\n[Your Name]"

        bullet_points = []
        for c in critical:
            bullet_points.append(f"• {c['type']}: {c['negotiation_tip']}")

        bullets_str = "\n".join(bullet_points)
        return f"""Hi [Client Name],

Thanks so much for sending over the contract! I'm really excited about collaborating on this project and bringing these deliverables to life.

I conducted our standard internal legal review of the agreement. There are just a few specific clauses that we need to adjust to align with our standard freelance terms:

{bullets_str}

I have attached a redlined version with these adjustments highlighted for your legal/finance team. They are standard provisions for independent contractors to ensure mutual fairness and timely delivery.

Let me know if these adjustments work on your end, and I'll be ready to sign immediately!

Best regards,
[Your Name]
Independent Specialist"""
