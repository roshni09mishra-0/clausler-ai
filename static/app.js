// Clausler Local AI Logic - Exact Clausler Contract Risk Analyzer Workflow

let currentAnalysis = null;
let currentContractText = "";
let availableTemplates = [];
let selectedTemplateId = "freelance-sow";

document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  await loadTemplates();
  setupEventListeners();

  // Load predatory sample so audit panel is immediately functional
  loadSampleContract("predatory", true);
});

async function loadTemplates() {
  try {
    const res = await fetch("/api/templates");
    if (res.ok) {
      const data = await res.json();
      availableTemplates = data.templates || [];
      renderTemplateFields(selectedTemplateId);
    }
  } catch (err) {
    console.warn("Template fetch notice:", err);
  }
}

function selectTemplate(templateId) {
  selectedTemplateId = templateId;
  
  // Highlight active card
  document.querySelectorAll(".template-card").forEach(c => {
    c.classList.remove("border-2", "border-primary", "bg-primary/10");
    c.classList.add("border", "border-slate-800");
  });
  
  const activeCard = event.currentTarget;
  if (activeCard) {
    activeCard.classList.remove("border", "border-slate-800");
    activeCard.classList.add("border-2", "border-primary", "bg-primary/10");
  }

  renderTemplateFields(templateId);
  document.getElementById("templateBuilder").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function renderTemplateFields(templateId) {
  const tmpl = availableTemplates.find(t => t.id === templateId);
  if (!tmpl) return;

  document.getElementById("builderTitle").textContent = `Customizing: ${tmpl.title}`;
  const container = document.getElementById("templateFormFields");
  container.innerHTML = "";

  (tmpl.variables || []).forEach(v => {
    const fieldDiv = document.createElement("div");
    fieldDiv.className = "flex flex-col gap-1.5";
    fieldDiv.innerHTML = `
      <label class="text-xs font-semibold text-slate-300">${escapeHtml(v.label)}</label>
      <input type="text" id="field-${v.id}" value="${escapeHtml(v.default)}" class="w-full bg-[#091628] border border-slate-700 rounded-lg p-2.5 text-xs text-white font-medium focus:outline-none focus:border-primary transition-colors">
    `;
    container.appendChild(fieldDiv);
  });
}

function setupEventListeners() {
  const contractInput = document.getElementById("contractInput");
  const charCount = document.getElementById("charCount");
  const btnScan = document.getElementById("btnScan");
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const btnGenerateTemplate = document.getElementById("btnGenerateTemplate");

  contractInput.addEventListener("input", () => {
    updateWordCount(contractInput.value);
  });

  document.querySelectorAll(".sample-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const sampleId = btn.dataset.sample;
      loadSampleContract(sampleId, true);
    });
  });

  if (btnGenerateTemplate) {
    btnGenerateTemplate.addEventListener("click", async () => {
      const tmpl = availableTemplates.find(t => t.id === selectedTemplateId);
      if (!tmpl) return;

      const vars = {};
      (tmpl.variables || []).forEach(v => {
        const inp = document.getElementById(`field-${v.id}`);
        vars[v.id] = inp ? inp.value : v.default;
      });

      btnGenerateTemplate.disabled = true;
      btnGenerateTemplate.textContent = "Assembling Draft...";

      try {
        const res = await fetch("/api/templates/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            template_id: selectedTemplateId,
            variables: vars
          })
        });

        if (res.ok) {
          const data = await res.json();
          document.getElementById("contractInput").value = data.generated_text;
          updateWordCount(data.generated_text);
          renderAnalysis(data.audit);
          document.getElementById("studio").scrollIntoView({ behavior: "smooth" });
        }
      } catch (err) {
        alert("Generation error: " + err.message);
      } finally {
        btnGenerateTemplate.disabled = false;
        btnGenerateTemplate.innerHTML = `<i data-lucide="sparkles" class="w-3.5 h-3.5 text-slate-950"></i><span>Assemble & Audit Draft</span>`;
        if (window.lucide) lucide.createIcons();
      }
    });
  }

  btnScan.addEventListener("click", () => {
    const text = contractInput.value.trim();
    if (!text) {
      alert("Please paste or upload a contract first.");
      return;
    }
    runAnalysis(text);
  });

  dropZone.addEventListener("click", () => fileInput.click());
  
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("border-primary", "bg-primary/5");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("border-primary", "bg-primary/5");
  });

  dropZone.addEventListener("drop", async (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-primary", "bg-primary/5");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files[0]) {
      handleFileUpload(fileInput.files[0]);
    }
  });

  setupTabs();

  document.getElementById("btnCopyEmail").addEventListener("click", () => {
    const text = document.getElementById("emailDraftArea").value;
    navigator.clipboard.writeText(text);
    const label = document.getElementById("copyEmailText");
    label.textContent = "Copied!";
    setTimeout(() => { label.textContent = "Copy Email"; }, 2000);
  });

  document.getElementById("btnExportMarkdown").addEventListener("click", exportMarkdownReport);
  document.getElementById("btnPrintReport").addEventListener("click", () => window.print());
}

function updateWordCount(text) {
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  document.getElementById("charCount").textContent = `${words} words`;
}

async function loadSampleContract(sampleId, autoRun = false) {
  try {
    const res = await fetch(`/api/sample/${sampleId}`);
    if (res.ok) {
      const data = await res.json();
      const textarea = document.getElementById("contractInput");
      textarea.value = data.text;
      currentContractText = data.text;
      updateWordCount(data.text);
      
      if (autoRun) {
        runAnalysis(data.text);
      }
    }
  } catch (err) {
    console.error("Failed to load sample:", err);
  }
}

async function handleFileUpload(file) {
  const scanStatus = document.getElementById("scanStatusText");
  scanStatus.textContent = `Extracting ${file.name}...`;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("model_name", "offline-heuristics");

  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      const result = await res.json();
      if (result.extracted_text) {
        document.getElementById("contractInput").value = result.extracted_text;
        currentContractText = result.extracted_text;
        updateWordCount(result.extracted_text);
      }
      renderAnalysis(result);
    } else {
      const err = await res.json();
      alert(`Upload error: ${err.detail || "Could not read file."}`);
    }
  } catch (err) {
    alert(`File processing error: ${err.message}`);
  } finally {
    scanStatus.textContent = "Air-gapped: 0 external requests";
  }
}

async function runAnalysis(text) {
  const scanStatus = document.getElementById("scanStatusText");
  const btnScan = document.getElementById("btnScan");

  btnScan.disabled = true;
  btnScan.textContent = "Auditing Locally...";
  scanStatus.textContent = "Scanning for predatory terms & liability traps...";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        model_name: "offline-heuristics"
      })
    });

    if (res.ok) {
      const result = await res.json();
      renderAnalysis(result);
    } else {
      const err = await res.json();
      alert(`Audit failed: ${err.detail || "Server error"}`);
    }
  } catch (err) {
    alert(`Connection error: ${err.message}`);
  } finally {
    btnScan.disabled = false;
    btnScan.innerHTML = `<i data-lucide="shield-alert" class="w-4 h-4 text-slate-950"></i><span>Run Risk Audit</span>`;
    scanStatus.textContent = "Audit complete.";
    if (window.lucide) lucide.createIcons();
  }
}

function renderAnalysis(data) {
  currentAnalysis = data;
  currentContractText = document.getElementById("contractInput").value;

  updateScoreRadar(
    data.overall_score || 25,
    data.risk_verdict || "High Risk",
    data.summary || "Severe traps detected.",
    data.critical_traps_count || 0,
    data.warnings_count || 0,
    data.safe_clauses_count || 0,
    data.financial_exposure_usd || 0
  );

  renderAnnotatedDocument(currentContractText, data.clauses || []);
  renderClauseCards(data.clauses || []);

  if (data.email_draft) {
    document.getElementById("emailDraftArea").value = data.email_draft;
  }

  renderDiffView(data.clauses || []);
}

function updateScoreRadar(score, verdict, summary, traps, warnings, safe, exposure) {
  const scoreVal = document.getElementById("scoreValue");
  const scoreCircle = document.getElementById("scoreCircle");
  const verdictBadge = document.getElementById("riskVerdictBadge");
  const summaryText = document.getElementById("riskSummaryText");

  scoreVal.textContent = score;
  summaryText.textContent = summary;
  document.getElementById("statTraps").textContent = `${traps} Red Flags`;
  document.getElementById("findingsCount").textContent = (traps + warnings + safe);

  const exposureElem = document.getElementById("statExposure");
  if (exposureElem) {
    exposureElem.textContent = exposure > 0 ? `$${exposure.toLocaleString()}` : "$0";
  }

  scoreCircle.setAttribute("stroke-dasharray", `${score}, 100`);

  if (score < 45) {
    scoreCircle.setAttribute("class", "text-red-500 transition-all duration-1000 ease-out");
    verdictBadge.className = "inline-block px-2.5 py-0.5 rounded-full bg-red-950 text-red-300 border border-red-800 text-[11px] font-bold uppercase tracking-wider mb-1";
    verdictBadge.textContent = verdict;
  } else if (score < 75) {
    scoreCircle.setAttribute("class", "text-amber-500 transition-all duration-1000 ease-out");
    verdictBadge.className = "inline-block px-2.5 py-0.5 rounded-full bg-amber-950 text-amber-300 border border-amber-800 text-[11px] font-bold uppercase tracking-wider mb-1";
    verdictBadge.textContent = verdict;
  } else {
    scoreCircle.setAttribute("class", "text-primary transition-all duration-1000 ease-out");
    verdictBadge.className = "inline-block px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-primary/50 text-[11px] font-bold uppercase tracking-wider mb-1";
    verdictBadge.textContent = verdict;
  }
}

function renderAnnotatedDocument(text, clauses) {
  const container = document.getElementById("docViewerContainer");
  const target = document.getElementById("annotatedText");
  container.classList.remove("hidden");

  let escaped = escapeHtml(text);

  clauses.forEach((c) => {
    if (c.original_text && c.original_text.length > 10) {
      const snippet = escapeHtml(c.original_text);
      const severityClass = c.severity === "critical" ? "clause-critical" : (c.severity === "warning" ? "clause-warning" : "clause-safe");
      
      if (escaped.includes(snippet)) {
        escaped = escaped.replace(snippet, `<mark id="mark-${c.id}" class="clause-highlight ${severityClass}" onclick="selectClause('${c.id}')">${snippet}</mark>`);
      } else {
        const words = snippet.split(" ").slice(0, 5).join(" ");
        if (words && escaped.includes(words)) {
          escaped = escaped.replace(words, `<mark id="mark-${c.id}" class="clause-highlight ${severityClass}" onclick="selectClause('${c.id}')">${words} [...]</mark>`);
        }
      }
    }
  });

  target.innerHTML = escaped;
}

function renderClauseCards(clauses) {
  const list = document.getElementById("clausesList");
  list.innerHTML = "";

  if (clauses.length === 0) {
    list.innerHTML = `<div class="p-4 text-xs text-slate-400">No risky clauses identified in this document.</div>`;
    return;
  }

  clauses.forEach((c, index) => {
    const card = document.createElement("div");
    card.id = `card-${c.id}`;
    card.className = "clausler-card p-4.5 cursor-pointer border border-slate-700/80 hover:border-primary/50 transition-all";
    card.onclick = () => selectClause(c.id);

    const isCritical = c.severity === "critical";
    const badgeColor = isCritical ? "bg-red-950/70 text-red-300 border-red-800" : (c.severity === "warning" ? "bg-amber-950/70 text-amber-300 border-amber-800" : "bg-emerald-950/70 text-emerald-300 border-primary/50");

    card.innerHTML = `
      <div class="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-clausler-cardBorder">
        <div class="flex items-center gap-1.5">
          <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full border ${badgeColor}">
            ${c.type || "Contract Term"}
          </span>
          <span class="text-[10px] text-slate-500">#${index + 1}</span>
        </div>
        ${c.financial_risk_estimate ? `
          <span class="text-[10px] font-bold text-primary font-mono">${escapeHtml(c.financial_risk_estimate)}</span>
        ` : ''}
      </div>

      <div class="p-3 rounded-lg bg-[#091628] border border-slate-700/80 text-xs font-mono text-slate-300 mb-3 leading-relaxed">
        "${escapeHtml(c.original_text || '')}"
      </div>

      <div class="mb-3">
        <div class="text-[10px] font-bold uppercase text-slate-400 mb-1">Plain-English Impact:</div>
        <p class="text-xs text-slate-200 leading-relaxed font-sans">${escapeHtml(c.plain_english_verdict || '')}</p>
      </div>

      ${c.counter_clause ? `
        <div class="pt-2.5 border-t border-clausler-cardBorder">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] font-bold uppercase text-primary flex items-center gap-1.5">
              <i data-lucide="sparkles" class="w-3.5 h-3.5 text-primary"></i>
              <span>Protective Counter-Clause:</span>
            </span>
            <button onclick="event.stopPropagation(); copyCounterClause('${c.id}', this)" class="text-[10px] font-semibold text-slate-300 hover:text-white px-2 py-0.5 rounded bg-slate-800 border border-slate-700 transition-colors">
              Copy
            </button>
          </div>
          <div class="p-3 rounded-lg bg-emerald-950/30 border border-primary/30 text-emerald-200 text-xs font-mono leading-relaxed">
            ${escapeHtml(c.counter_clause)}
          </div>
        </div>
      ` : ''}

      ${c.negotiation_tip ? `
        <div class="mt-2.5 text-xs text-slate-400 leading-snug">
          <strong class="text-white">Negotiation Tip:</strong> ${escapeHtml(c.negotiation_tip)}
        </div>
      ` : ''}
    `;

    list.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

function selectClause(clauseId) {
  document.querySelectorAll(".clausler-card").forEach(c => c.classList.remove("ring-2", "ring-primary"));
  const card = document.getElementById(`card-${clauseId}`);
  if (card) {
    card.classList.add("ring-2", "ring-primary");
    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  document.querySelectorAll("mark.clause-highlight").forEach(m => m.classList.remove("active"));
  const mark = document.getElementById(`mark-${clauseId}`);
  if (mark) {
    mark.classList.add("active");
    mark.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  if (currentAnalysis && currentAnalysis.clauses) {
    const clause = currentAnalysis.clauses.find(c => c.id === clauseId);
    if (clause) {
      document.getElementById("diffOriginal").textContent = clause.original_text || "";
      document.getElementById("diffRevised").textContent = clause.counter_clause || "";
    }
  }
}

function copyCounterClause(clauseId, btn) {
  if (!currentAnalysis || !currentAnalysis.clauses) return;
  const clause = currentAnalysis.clauses.find(c => c.id === clauseId);
  if (clause && clause.counter_clause) {
    navigator.clipboard.writeText(clause.counter_clause);
    const originalText = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = originalText; }, 1500);
  }
}

function renderDiffView(clauses) {
  const critical = clauses.find(c => c.severity === "critical") || clauses[0];
  if (critical) {
    document.getElementById("diffOriginal").textContent = critical.original_text || "";
    document.getElementById("diffRevised").textContent = critical.counter_clause || "";
  }
}

function setupTabs() {
  const tabFindings = document.getElementById("tabFindings");
  const tabEmail = document.getElementById("tabEmail");
  const tabDiff = document.getElementById("tabDiff");

  const viewFindings = document.getElementById("viewFindings");
  const viewEmail = document.getElementById("viewEmail");
  const viewDiff = document.getElementById("viewDiff");

  function activateTab(activeTab, activeView) {
    [tabFindings, tabEmail, tabDiff].forEach(t => {
      t.className = "tab-btn pb-2 text-xs font-semibold text-slate-400 hover:text-white border-b-2 border-transparent transition-colors flex items-center gap-1.5";
    });
    activeTab.className = "tab-btn pb-2 text-xs font-bold text-primary border-b-2 border-primary transition-colors flex items-center gap-1.5";

    [viewFindings, viewEmail, viewDiff].forEach(v => v.classList.add("hidden"));
    activeView.classList.remove("hidden");
    activeView.classList.add("flex");
  }

  tabFindings.addEventListener("click", () => activateTab(tabFindings, viewFindings));
  tabEmail.addEventListener("click", () => activateTab(tabEmail, viewEmail));
  tabDiff.addEventListener("click", () => activateTab(tabDiff, viewDiff));
}

function exportMarkdownReport() {
  if (!currentAnalysis) {
    alert("Please run an audit first to generate report.");
    return;
  }

  const d = currentAnalysis;
  let md = `# CLAUSLER CONTRACT RISK REPORT\n\n`;
  md += `**Contract Safety Rating:** ${d.overall_score || 0} / 100\n`;
  md += `**Verdict:** ${d.risk_verdict || "Audited"}\n`;
  md += `**Calculated Exposure:** $${(d.financial_exposure_usd || 0).toLocaleString()}\n`;
  md += `**Summary:** ${d.summary || ""}\n\n`;
  md += `## FLAGGED TERMS & RISKS\n\n`;

  (d.clauses || []).forEach((c, i) => {
    md += `### ${i + 1}. [${(c.severity || "risk").toUpperCase()}] ${c.type || "Clause"}\n`;
    md += `> "${c.original_text || ""}"\n\n`;
    md += `**Plain-English Impact:** ${c.plain_english_verdict || ""}\n\n`;
    if (c.counter_clause) {
      md += `**Protective Counter-Clause:**\n\`\`\`\n${c.counter_clause}\n\`\`\`\n\n`;
    }
  });

  if (d.email_draft) {
    md += `## CLIENT PUSHBACK EMAIL DRAFT\n\n\`\`\`\n${d.email_draft}\n\`\`\`\n`;
  }

  const blob = new Blob([md], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `clausler-risk-report-${Date.now()}.md`;
  a.click();
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
