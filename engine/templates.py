"""
Curated legal document templates inspired by Genie AI (genieai.co).
Pre-vetted, balanced, jurisdiction-adaptable templates for freelancers & SMBs.
"""

TEMPLATES = [
    {
        "id": "freelance-sow",
        "category": "Services & Tech",
        "title": "Independent Contractor Agreement & SOW",
        "popular": True,
        "badge": "Most Popular",
        "jurisdiction": "US / UK / Global Compatible",
        "summary": "Protects developers, designers, and consultants with Net-15 payment terms, capped liability, 2 structured revision rounds, and portfolio attribution rights.",
        "variables": [
            {"id": "client_name", "label": "Client Organization", "default": "Acme Innovations Inc."},
            {"id": "contractor_name", "label": "Contractor / Agency Name", "default": "Alex Morgan Design Studio"},
            {"id": "service_desc", "label": "Services & Deliverables", "default": "UI/UX design, design system components, and production-ready Figma prototypes."},
            {"id": "project_fee", "label": "Fixed Milestone Fee ($)", "default": "6,500"},
            {"id": "revisions", "label": "Included Revision Rounds", "default": "2"}
        ],
        "template_text": """INDEPENDENT CONTRACTOR SERVICES AGREEMENT

This Agreement is made between {client_name} ("Client") and {contractor_name} ("Contractor").

1. SCOPE OF SERVICES
Contractor agrees to perform the following services: {service_desc}. Work includes up to {revisions} consolidated revision rounds. Any additional changes shall be billed at $120/hour upon written approval.

2. PAYMENT & EXPENSES
Total fixed project fee is ${project_fee} USD. A 50% commencement deposit is due upon signature. The remaining 50% balance is payable Net-15 days from final deliverable sign-off. Late balances incur 1.5% monthly interest.

3. INTELLECTUAL PROPERTY & ATTRIBUTION
Upon receipt of full payment, Client shall own all final deliverables. Contractor retains ownership of pre-existing background code, tools, and UI assets, and reserves the standard commercial right to showcase non-confidential deliverables in Contractor's professional portfolio.

4. MUTUAL LIMITATION OF LIABILITY
Neither party shall be liable for indirect, incidental, or consequential damages. Aggregate liability for any claim arising out of this Agreement is strictly capped at the total amount actually paid under this Agreement.
"""
    },
    {
        "id": "mutual-nda",
        "category": "Confidentiality",
        "title": "Mutual Non-Disclosure Agreement (NDA)",
        "popular": True,
        "badge": "Standard 2-Year",
        "jurisdiction": "Multi-Jurisdiction Safe",
        "summary": "Balanced 2-way confidentiality agreement that protects both parties without overreaching IP assignments, perpetuity traps, or unilateral gag orders.",
        "variables": [
            {"id": "party_a", "label": "Disclosing Party / Client", "default": "VentureScale Capital"},
            {"id": "party_b", "label": "Receiving Party / Specialist", "default": "Independent Technical Advisor"},
            {"id": "purpose", "label": "Discussion Purpose", "default": "Evaluating software architecture, roadmap consulting, and potential partnership."}
        ],
        "template_text": """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into by {party_a} and {party_b} ("Parties").

1. PURPOSE
The Parties wish to explore business and technical collaboration regarding: {purpose}.

2. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means proprietary information marked as confidential or that reasonably should be understood to be confidential. It excludes information already public, independently developed, or known prior to disclosure.

3. STANDARD OF CARE & DURATION
Each party agrees to hold the other's Confidential Information in strict confidence for a period of two (2) years from the date of disclosure.

4. NO IP ASSIGNMENT IN PRELIMINARY TALKS
Neither party transfers or assigns any patent, copyright, or intellectual property rights by virtue of preliminary discussions. No implied licenses are granted.
"""
    },
    {
        "id": "agency-subcontractor",
        "category": "Agency & Creative",
        "title": "Subcontractor Master Agreement",
        "popular": False,
        "badge": "Agency Grade",
        "jurisdiction": "US / International",
        "summary": "For agencies hiring freelance contributors with fair flow-down terms, milestone milestones, and direct client non-solicitation.",
        "variables": [
            {"id": "agency_name", "label": "Primary Agency", "default": "Eleven Creative Group"},
            {"id": "subcontractor_name", "label": "Subcontractor", "default": "Jordan Taylor"},
            {"id": "hourly_rate", "label": "Hourly Rate ($)", "default": "95"}
        ],
        "template_text": """AGENCY SUBCONTRACTOR AGREEMENT

This Subcontractor Agreement is made between {agency_name} ("Agency") and {subcontractor_name} ("Subcontractor").

1. INDEPENDENT STATUS
Subcontractor provides independent professional services to Agency on a milestone or hourly basis at ${hourly_rate}/hour. Subcontractor retains autonomy over method and timing of delivery.

2. PAYMENT GUARANTEE
Agency agrees to pay approved Subcontractor invoices within Net-15 days, regardless of whether Agency has received final collection from end-client ("No Pay-When-Paid" protection).

3. NON-SOLICITATION OF DIRECT CLIENTS
Subcontractor agrees not to directly solicit or divert Agency's active client accounts for twelve (12) months following project completion. Subcontractor remains free to accept non-solicited public business.
"""
    },
    {
        "id": "saas-terms",
        "category": "SaaS & Licensing",
        "title": "SaaS License & Software Terms",
        "popular": False,
        "badge": "B2B Safe",
        "jurisdiction": "Commercial Standard",
        "summary": "Lightweight B2B software terms covering SLA, data privacy, liability limitation, and subscription renewals.",
        "variables": [
            {"id": "company_name", "label": "SaaS Provider", "default": "CloudPilot Technologies"},
            {"id": "subscriber_name", "label": "Customer / Subscriber", "default": "Nexus Retail LLC"}
        ],
        "template_text": """SOFTWARE AS A SERVICE (SAAS) SUBSCRIBER TERMS

These Terms govern access provided by {company_name} ("Provider") to {subscriber_name} ("Subscriber").

1. SUBSCRIPTION GRANT
Provider grants Subscriber a non-exclusive, non-transferable license to access the hosted cloud platform during the active subscription period.

2. DATA SECURITY & OWNERSHIP
Subscriber retains all ownership and rights in and to Customer Data. Provider shall not use Customer Data to train shared artificial intelligence models without explicit opt-in consent.

3. SERVICE AVAILABILITY & LIABILITY
Provider provides 99.5% target uptime. In no event shall Provider's aggregate liability exceed fees paid by Subscriber in the preceding 12 months.
"""
    }
]
