import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from pypdf import PdfReader

from engine.analyzer import ContractAnalyzer
from engine.samples import (
    PREDATORY_FREELANCE_AGREEMENT,
    SNEAKY_NDA_AGREEMENT,
    FAIR_STANDARD_AGREEMENT
)
from engine.templates import TEMPLATES

app = FastAPI(title="RedlineLocal - Accessible Contracts OS inspired by Genie AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = ContractAnalyzer()

class AnalyzeRequest(BaseModel):
    text: str
    model_name: Optional[str] = "offline-heuristics"

class GenerateTemplateRequest(BaseModel):
    template_id: str
    variables: Dict[str, str]

@app.get("/api/status")
async def get_status():
    ollama_info = await analyzer.check_ollama_status()
    return {
        "status": "online",
        "air_gapped": True,
        "outbound_requests_allowed": False,
        "ollama": ollama_info,
        "supported_models": [
            {"id": "offline-heuristics", "name": "⚡ Neural Heuristic Engine (Instant, 0 setup)"},
            {"id": "llama3.2:3b", "name": "🦙 Llama 3.2 3B (Local Ollama)"},
            {"id": "qwen2.5:7b", "name": "🐉 Qwen 2.5 7B (Local Ollama)"},
            {"id": "deepseek-r1:8b", "name": "🧠 DeepSeek R1 8B (Local Ollama)"}
        ]
    }

@app.get("/api/templates")
async def list_templates():
    return {"templates": TEMPLATES}

@app.post("/api/templates/generate")
async def generate_template(req: GenerateTemplateRequest):
    tmpl = next((t for t in TEMPLATES if t["id"] == req.template_id), None)
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")
    
    text = tmpl["template_text"]
    for k, v in req.variables.items():
        text = text.replace(f"{{{k}}}", v)
    
    # Run instant audit on the generated draft
    audit = await analyzer.analyze(text, model_name="offline-heuristics")
    
    return {
        "template_id": tmpl["id"],
        "title": tmpl["title"],
        "generated_text": text,
        "audit": audit
    }

@app.get("/api/samples")
async def list_samples():
    return {
        "samples": [
            {
                "id": "predatory",
                "title": "Master Services Agreement (Predatory)",
                "description": "Net-90, 50% withholding, unlimited indemnification, IP seizure, 2-year non-compete.",
                "badge": "🚨 High Risk"
            },
            {
                "id": "nda",
                "title": "Unilateral IP Grab NDA",
                "description": "Perpetual confidentiality, assignment of ideas created in discussions, $100k liquidated damages.",
                "badge": "⚠️ Warning"
            },
            {
                "id": "fair",
                "title": "Balanced Freelance Agreement",
                "description": "Net-15, 2 revision rounds, limited liability cap, portfolio attribution rights.",
                "badge": "✅ Fair & Balanced"
            }
        ]
    }

@app.get("/api/sample/{sample_id}")
async def get_sample(sample_id: str):
    if sample_id == "predatory":
        return {"id": "predatory", "title": "Predatory Freelance Agreement", "text": PREDATORY_FREELANCE_AGREEMENT}
    elif sample_id == "nda":
        return {"id": "nda", "title": "Sneaky Enterprise NDA", "text": SNEAKY_NDA_AGREEMENT}
    elif sample_id == "fair":
        return {"id": "fair", "title": "Standard Balanced Agreement", "text": FAIR_STANDARD_AGREEMENT}
    else:
        raise HTTPException(status_code=404, detail="Sample not found")

@app.post("/api/analyze")
async def analyze_contract(req: AnalyzeRequest):
    if not req.text or len(req.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Contract text too short to analyze.")
    result = await analyzer.analyze(req.text, model_name=req.model_name)
    return result

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), model_name: Optional[str] = Form("offline-heuristics")):
    contents = await file.read()
    filename = file.filename.lower()
    text = ""
    
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(contents))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    else:
        try:
            text = contents.decode("utf-8", errors="ignore")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in uploaded file.")

    result = await analyzer.analyze(text, model_name=model_name)
    result["filename"] = file.filename
    result["extracted_text"] = text
    return result

static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path, exist_ok=True)

app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*65)
    print("  [REDLINELOCAL] - AIR-GAPPED FREELANCE CONTRACT OS")
    print("  [GENIE AI STYLE] - Templates, Plain-English, Onboarding")
    print("  [LOCAL SERVER]  - http://localhost:8000")
    print("="*65 + "\n")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
