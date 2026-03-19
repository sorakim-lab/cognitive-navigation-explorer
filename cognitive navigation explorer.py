import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import time
from datetime import datetime

st.set_page_config(
    page_title="Cognitive Navigation Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f4f5f7;
    color: #1A1A1A;
}
.stApp { background-color: #f4f5f7; }
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"],
#MainMenu, footer { display: none !important; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1300px; }

.scenario-box {
    background: #111827;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid #3D7EFF;
}
.scenario-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.5rem;
}
.scenario-text {
    font-size: 1rem;
    color: #f3f4f6;
    line-height: 1.7;
}
.task-text {
    font-size: 0.88rem;
    color: #fbbf24;
    margin-top: 0.8rem;
    font-weight: 500;
}

.doc-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 0.75rem;
}
.doc-card:hover {
    border-color: #3D7EFF;
    box-shadow: 0 4px 12px rgba(61,126,255,0.12);
}
.doc-card.active {
    border-color: #3D7EFF;
    background: #eff6ff;
}
.doc-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.3rem;
}
.doc-tag {
    display: inline-block;
    background: #f3f4f6;
    border-radius: 20px;
    padding: 0.15rem 0.6rem;
    font-size: 0.68rem;
    font-weight: 500;
    color: #6b7280;
    margin-right: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}
.doc-tag.ref { background: #fff7ed; color: #d97706; }
.doc-tag.sop { background: #eff6ff; color: #2563eb; }
.doc-tag.protocol { background: #f0fdf4; color: #16a34a; }

.doc-content {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    min-height: 400px;
}
.doc-content-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.3rem;
    font-family: 'Inter', sans-serif;
}
.doc-content-meta {
    font-size: 0.75rem;
    color: #9ca3af;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #f3f4f6;
}
.doc-section {
    margin-bottom: 1rem;
}
.doc-section-title {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.4rem;
}
.doc-section-body {
    font-size: 0.88rem;
    color: #374151;
    line-height: 1.7;
}
.cross-ref {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.82rem;
    color: #92400e;
    margin-top: 0.75rem;
}
.cross-ref-icon { margin-right: 0.4rem; }

.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    flex: 1;
    border: 1px solid #e5e7eb;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 12px 12px 0 0;
}
.metric-card.blue  { --accent: #3D7EFF; }
.metric-card.orange { --accent: #FF9500; }
.metric-card.red   { --accent: #FF3B30; }
.metric-card.green { --accent: #34C759; }
.metric-value {
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
}

.insight {
    background: #f9fafb;
    border-left: 3px solid #3D7EFF;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #6b7280;
    font-style: italic;
    margin-top: 1rem;
    line-height: 1.6;
}

.section-header {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.8rem;
    margin-top: 1.5rem;
}

.visit-badge {
    display: inline-block;
    background: #eff6ff;
    border-radius: 20px;
    padding: 0.15rem 0.55rem;
    font-size: 0.68rem;
    font-weight: 600;
    color: #2563eb;
    font-family: 'JetBrains Mono', monospace;
    margin-left: 0.4rem;
}
.visit-badge.loopback { background: #fef2f2; color: #dc2626; }
</style>
""", unsafe_allow_html=True)

# ── Document database ──────────────────────────────────────────────────────
DOCS = {
    "SOP_ELISA_Test_Method": {
        "title": "SOP: ELISA Test Method",
        "code": "SOP-QC-001",
        "version": "v3.2",
        "tag": "sop",
        "sections": {
            "1. Purpose": "This SOP describes the procedure for performing ELISA testing of drug product samples to verify conformance with established specifications.",
            "2. Scope": "Applicable to all QC analysts performing ELISA assays in the quality control laboratory.",
            "3. Acceptance Criteria": "Results must fall within ±15% of the reference standard. Out-of-specification (OOS) results must be handled according to SOP-QC-004.",
            "4. Analyst Requirements": "All analysts must hold valid training certification for this method. Refer to SOP-QC-007 for training and qualification requirements.",
            "5. Equipment": "Microplate reader, pipettes (calibrated), incubator. Equipment qualification status must be confirmed prior to testing. See SOP-QC-005.",
            "6. Reagents": "All reagents must be within expiry date. Refer to Analytical Method Protocol AMP-ELISA-02 for detailed reagent specifications.",
        },
        "cross_refs": [
            ("SOP_OOS_Procedure", "OOS results → SOP-QC-004"),
            ("SOP_Analyst_Training", "Analyst qualification → SOP-QC-007"),
            ("Analytical_Method_Protocol", "Reagent specifications → AMP-ELISA-02"),
            ("SOP_Equipment_Qualification", "Equipment status → SOP-QC-005"),
        ]
    },
    "SOP_OOS_Procedure": {
        "title": "SOP: Out-of-Specification (OOS) Investigation Procedure",
        "code": "SOP-QC-004",
        "version": "v2.1",
        "tag": "sop",
        "sections": {
            "1. Purpose": "To define the procedure for investigating out-of-specification (OOS) laboratory results.",
            "2. Phase 1 — Laboratory Investigation": "The analyst must first conduct a Phase 1 investigation to rule out laboratory error. This includes review of calculations, instrument performance, and sample handling.",
            "3. Analyst Qualification Check": "Verify that the analyst performing the test holds current certification. Training records are maintained per SOP-QC-007.",
            "4. Method Verification": "Confirm that the method used is current and validated. See Analytical Method Protocol AMP-ELISA-02 for method validation status.",
            "5. Phase 2 — Full Investigation": "If Phase 1 does not identify a root cause, a full investigation must be initiated per SOP-QC-006 (Deviation Handling).",
            "6. Documentation": "All investigation steps must be documented in the OOS report form. Reference specification limits in Reference_Specification_Doc.",
        },
        "cross_refs": [
            ("SOP_Analyst_Training", "Analyst certification → SOP-QC-007"),
            ("Analytical_Method_Protocol", "Method validation status → AMP-ELISA-02"),
            ("SOP_Deviation_Handling", "Full investigation → SOP-QC-006"),
            ("Reference_Specification_Doc", "Specification limits → REF-SPEC-003"),
        ]
    },
    "SOP_Deviation_Handling": {
        "title": "SOP: Deviation Handling and CAPA",
        "code": "SOP-QC-006",
        "version": "v4.0",
        "tag": "sop",
        "sections": {
            "1. Purpose": "To establish a systematic process for identifying, documenting, and resolving deviations from established procedures.",
            "2. Deviation Classification": "Deviations are classified as Critical, Major, or Minor based on impact assessment. ELISA OOS results are classified as Major unless product safety is impacted.",
            "3. Root Cause Analysis": "Root cause analysis must address all potential contributing factors including: personnel, method, materials, equipment, and environment.",
            "4. Personnel Factor": "Review analyst training status per SOP-QC-007. Confirm method comprehension and recent performance history.",
            "5. Equipment Factor": "Confirm qualification status of all equipment used. Calibration records for pipettes must be verified. See SOP-QC-005.",
            "6. Environment Factor": "Temperature and humidity logs for the laboratory on the day of testing must be reviewed.",
            "7. CAPA": "Corrective and Preventive Actions must be documented and approved within 30 business days.",
        },
        "cross_refs": [
            ("SOP_Analyst_Training", "Personnel factor → SOP-QC-007"),
            ("SOP_Equipment_Qualification", "Equipment factor → SOP-QC-005"),
            ("SOP_ELISA_Test_Method", "Method reference → SOP-QC-001"),
        ]
    },
    "Analytical_Method_Protocol": {
        "title": "Analytical Method Protocol: ELISA",
        "code": "AMP-ELISA-02",
        "version": "v1.4",
        "tag": "protocol",
        "sections": {
            "1. Method Overview": "Validated ELISA method for quantitative determination of drug substance in finished product. Method validation completed 2023-08-15.",
            "2. Validation Status": "Current. Last method verification: 2024-11-03. Next scheduled review: 2025-11-03.",
            "3. Reagent Specifications": "Primary antibody: Lot expiry must be ≥ 6 months from date of use. Secondary antibody: Store at 2–8°C, discard if turbid. Substrate solution: Prepare fresh on day of use. Do not use after 4 hours.",
            "4. Reference Standard": "Reference standard must be within validity period. See Reference_Specification_Doc for acceptance criteria and storage conditions.",
            "5. Critical Parameters": "Incubation temperature: 37°C ± 1°C. Incubation time: 60 min ± 5 min. Plate reader wavelength: 450 nm.",
            "6. Known Interference": "Results may be affected if laboratory temperature deviates from 20–25°C during plate preparation. Monitor room temperature logs.",
        },
        "cross_refs": [
            ("Reference_Specification_Doc", "Reference standard → REF-SPEC-003"),
            ("SOP_ELISA_Test_Method", "Method SOP → SOP-QC-001"),
        ]
    },
    "Reference_Specification_Doc": {
        "title": "Reference Specification Document",
        "code": "REF-SPEC-003",
        "version": "v2.0",
        "tag": "ref",
        "sections": {
            "1. Product Specifications": "Acceptance criteria for ELISA assay: 85.0% – 115.0% of label claim. Results outside this range are classified as OOS.",
            "2. Reference Standard": "Reference standard validity: 12 months from opening. Storage: –20°C ± 5°C. Current lot expiry: 2025-09-30.",
            "3. Environmental Conditions": "Testing must be conducted at 20–25°C, 30–60% relative humidity. Deviations from these conditions must be documented.",
            "4. Analyst Qualification": "Analysts must complete method-specific qualification before performing independent testing. Records maintained per SOP-QC-007.",
            "5. Equipment Calibration": "Pipettes must be calibrated every 6 months. Plate reader wavelength accuracy verified annually. Current calibration status: see SOP-QC-005.",
        },
        "cross_refs": [
            ("SOP_OOS_Procedure", "OOS handling → SOP-QC-004"),
            ("SOP_Analyst_Training", "Analyst records → SOP-QC-007"),
            ("SOP_Equipment_Qualification", "Calibration records → SOP-QC-005"),
        ]
    },
    "SOP_Analyst_Training": {
        "title": "SOP: Analyst Training and Qualification",
        "code": "SOP-QC-007",
        "version": "v2.3",
        "tag": "sop",
        "sections": {
            "1. Purpose": "To define the training and qualification requirements for QC analysts performing analytical testing.",
            "2. Initial Qualification": "New analysts must complete: (1) GMP training, (2) method-specific training, (3) supervised practice runs ≥ 3 times, (4) qualification test with passing score ≥ 80%.",
            "3. Requalification": "Analysts must requalify every 24 months or following: extended leave (>3 months), significant method change, or OOS investigation finding.",
            "4. Training Records": "Training records are maintained in the QMS system. Current qualification status can be verified by supervisor or QA.",
            "5. OOS Events": "If an analyst is involved in an OOS event, supervisor review of training status is mandatory before resuming independent testing.",
        },
        "cross_refs": [
            ("SOP_OOS_Procedure", "OOS event response → SOP-QC-004"),
            ("SOP_ELISA_Test_Method", "Method reference → SOP-QC-001"),
        ]
    },
    "SOP_Equipment_Qualification": {
        "title": "SOP: Equipment Qualification and Calibration",
        "code": "SOP-QC-005",
        "version": "v3.1",
        "tag": "sop",
        "sections": {
            "1. Purpose": "To define qualification and calibration requirements for analytical equipment used in QC testing.",
            "2. Pipette Calibration": "All pipettes must be calibrated every 6 months by an approved service provider. Out-of-calibration pipettes must be removed from service immediately.",
            "3. Plate Reader Qualification": "Wavelength accuracy: verified annually. Current qualification status: QUALIFIED. Last qualification date: 2024-06-12. Next due: 2025-06-12.",
            "4. Incubator Qualification": "Temperature uniformity verified quarterly. Last qualification: 2024-10-01. Next due: 2025-01-01.",
            "5. Out-of-Qualification Equipment": "Any equipment found to be out-of-qualification must be quarantined and a deviation raised per SOP-QC-006.",
            "6. Records": "All calibration and qualification records are stored in the equipment logbook and QMS system.",
        },
        "cross_refs": [
            ("SOP_Deviation_Handling", "OOQ deviation → SOP-QC-006"),
            ("SOP_ELISA_Test_Method", "Equipment requirements → SOP-QC-001"),
        ]
    },
}

# ── Session state init ─────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = "intro"
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "current_doc" not in st.session_state:
    st.session_state.current_doc = None
if "nav_log" not in st.session_state:
    st.session_state.nav_log = []
if "doc_visit_times" not in st.session_state:
    st.session_state.doc_visit_times = {}
if "doc_visit_count" not in st.session_state:
    st.session_state.doc_visit_count = {}
if "last_visit_start" not in st.session_state:
    st.session_state.last_visit_start = None
if "session_start" not in st.session_state:
    st.session_state.session_start = None

def navigate_to(doc_key):
    now = time.time()
    # record time spent on previous doc
    if st.session_state.current_doc and st.session_state.last_visit_start:
        time_spent = round(now - st.session_state.last_visit_start, 1)
        prev = st.session_state.current_doc
        if prev not in st.session_state.doc_visit_times:
            st.session_state.doc_visit_times[prev] = []
        st.session_state.doc_visit_times[prev].append(time_spent)

    # determine action type
    visit_count = st.session_state.doc_visit_count.get(doc_key, 0)
    if visit_count == 0:
        action = "forward"
    else:
        action = "loopback"

    # determine if cross_reference
    if st.session_state.current_doc:
        cross_refs = [r[0] for r in DOCS[st.session_state.current_doc]["cross_refs"]]
        if doc_key in cross_refs:
            action = "cross_reference" if visit_count == 0 else "loopback"

    # log
    st.session_state.nav_log.append({
        "user_id": st.session_state.user_id,
        "from_doc": st.session_state.current_doc,
        "to_doc": doc_key,
        "action_type": action,
        "visit_count": visit_count + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })

    # update state
    st.session_state.doc_visit_count[doc_key] = visit_count + 1
    st.session_state.current_doc = doc_key
    st.session_state.last_visit_start = now

# ── INTRO MODE ─────────────────────────────────────────────────────────────
if st.session_state.mode == "intro":
    st.markdown("""
    <div style="max-width:720px; margin:60px auto; text-align:center;">
      <div style="font-size:0.7rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#9ca3af; margin-bottom:1rem;">
        HCI Research · Regulated Work Environments
      </div>
      <div style="font-size:2.2rem; font-weight:700; color:#111827; margin-bottom:0.5rem; font-family:'Inter',sans-serif; letter-spacing:-0.03em;">
        Cognitive Navigation Explorer
      </div>
      <div style="font-size:1rem; color:#6b7280; margin-bottom:2rem; line-height:1.7;">
        A research prototype that tracks cognitive navigation pathways during GMP document exploration.<br>
        Your navigation path, loopbacks, and cross-reference patterns are recorded automatically.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        uid = st.text_input("Enter participant ID (e.g. P01)", placeholder="P01")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start →", use_container_width=True, type="primary"):
            if uid.strip():
                st.session_state.user_id = uid.strip()
                st.session_state.mode = "explore"
                st.session_state.session_start = time.time()
                st.rerun()
            else:
                st.warning("Please enter a participant ID.")

# ── EXPLORE MODE ───────────────────────────────────────────────────────────
elif st.session_state.mode == "explore":

    # Scenario box
    st.markdown("""
    <div class="scenario-box">
      <div class="scenario-label">🔬 Scenario</div>
      <div class="scenario-text">
        An ELISA assay result has exceeded the specification limit (OOS event).
        You are required to identify the relevant procedures and documents needed to conduct a root cause investigation.
      </div>
      <div class="task-text">
        👉 Task: Find the documents and procedures that apply to this situation. No hints will be provided.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("<div class='section-header'>📂 Document List — click to open</div>", unsafe_allow_html=True)

        for doc_key, doc in DOCS.items():
            visit_count = st.session_state.doc_visit_count.get(doc_key, 0)
            is_active = st.session_state.current_doc == doc_key

            tag_class = doc["tag"]
            tag_label = {"sop": "SOP", "protocol": "Protocol", "ref": "Reference"}[tag_class]
            active_style = "border-color: #3D7EFF; background: #eff6ff;" if is_active else ""

            badge_html = ""
            if visit_count > 1:
                badge_html = f'<div style="margin-top:6px;"><span class="visit-badge loopback">↩ {visit_count}x visited</span></div>'
            elif visit_count == 1:
                badge_html = '<div style="margin-top:6px;"><span class="visit-badge">✓ visited</span></div>'

            st.markdown(f"""
            <div class="doc-card" style="{active_style}">
              <div class="doc-title">{doc['title']}</div>
              <span class="doc-tag {tag_class}">{tag_label}</span>
              <span class="doc-tag">{doc['code']}</span>
              {badge_html}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Open", key=f"btn_{doc_key}", use_container_width=True):
                navigate_to(doc_key)
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Done — View Results", use_container_width=True, type="primary"):
            if st.session_state.current_doc and st.session_state.last_visit_start:
                time_spent = round(time.time() - st.session_state.last_visit_start, 1)
                prev = st.session_state.current_doc
                if prev not in st.session_state.doc_visit_times:
                    st.session_state.doc_visit_times[prev] = []
                st.session_state.doc_visit_times[prev].append(time_spent)
            st.session_state.mode = "result"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True):
            for key in ["mode", "user_id", "current_doc", "nav_log",
                        "doc_visit_times", "doc_visit_count",
                        "last_visit_start", "session_start"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    with col_right:
        if st.session_state.current_doc is None:
            st.markdown("""
            <div style="background:#FFFFFF; border-radius:14px; padding:3rem 2rem;
                        border:1px solid #e5e7eb; text-align:center; color:#9ca3af;">
              <div style="font-size:2rem; margin-bottom:1rem;">📄</div>
              <div style="font-size:0.9rem;">Select a document from the list on the left to view its contents.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            doc = DOCS[st.session_state.current_doc]
            visit_count = st.session_state.doc_visit_count.get(st.session_state.current_doc, 0)

            visit_info = ""
            if visit_count > 1:
                visit_info = f'<span style="color:#dc2626; font-size:0.75rem; font-family:monospace;">↩ Visit #{visit_count} (loopback)</span>'
            elif visit_count == 1:
                visit_info = f'<span style="color:#16a34a; font-size:0.75rem; font-family:monospace;">✓ First visit</span>'

            st.markdown(f"""
            <div class="doc-content">
              <div class="doc-content-title">{doc['title']}</div>
              <div class="doc-content-meta">{doc['code']} · {doc['version']} · {visit_info}</div>
            """, unsafe_allow_html=True)

            for section_title, section_body in doc["sections"].items():
                st.markdown(f"""
                <div class="doc-section">
                  <div class="doc-section-title">{section_title}</div>
                  <div class="doc-section-body">{section_body}</div>
                </div>
                """, unsafe_allow_html=True)

            if doc["cross_refs"]:
                st.markdown("<div class='doc-section-title' style='margin-top:1rem;'>🔗 Cross-references</div>", unsafe_allow_html=True)
                for ref_key, ref_label in doc["cross_refs"]:
                    st.markdown(f"""
                    <div class="cross-ref">
                      <span class="cross-ref-icon">↗</span>{ref_label}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"→ {DOCS[ref_key]['title']}", key=f"xref_{st.session_state.current_doc}_{ref_key}"):
                        navigate_to(ref_key)
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ── RESULT MODE ────────────────────────────────────────────────────────────
elif st.session_state.mode == "result":

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-size:0.7rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#9ca3af; margin-bottom:0.4rem;">
        Navigation Complete
      </div>
      <div style="font-size:1.6rem; font-weight:700; color:#111827; font-family:'Inter',sans-serif; letter-spacing:-0.02em;">
        Cognitive Navigation Analysis
      </div>
      <div style="font-size:0.88rem; color:#6b7280; margin-top:0.3rem;">
        Participant <strong>{}</strong> · Total navigations: <strong>{}</strong>
      </div>
    </div>
    """.format(
        st.session_state.user_id,
        len(st.session_state.nav_log)
    ), unsafe_allow_html=True)

    log = st.session_state.nav_log
    df = pd.DataFrame(log)

    if df.empty:
        st.warning("탐색 기록이 없습니다.")
    else:
        # metrics
        total_nav = len(df)
        loopback_n = len(df[df["action_type"] == "loopback"])
        crossref_n = len(df[df["action_type"] == "cross_reference"])
        forward_n  = len(df[df["action_type"] == "forward"])
        docs_visited = df["to_doc"].nunique()

        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-card green">
            <div class="metric-value">{total_nav}</div>
            <div class="metric-label">Total Navigations</div>
          </div>
          <div class="metric-card blue">
            <div class="metric-value">{forward_n}</div>
            <div class="metric-label">Forward</div>
          </div>
          <div class="metric-card orange">
            <div class="metric-value">{crossref_n}</div>
            <div class="metric-label">Cross-reference</div>
          </div>
          <div class="metric-card red">
            <div class="metric-value">{loopback_n}</div>
            <div class="metric-label">Loopback</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-header'>🗺️ Navigation Path Network</div>", unsafe_allow_html=True)

            G = nx.DiGraph()
            color_map = {
                "forward": "#3D7EFF",
                "cross_reference": "#FF9500",
                "loopback": "#FF3B30",
            }

            for _, row in df.iterrows():
                if row["from_doc"] is None:
                    continue
                src = row["from_doc"].replace("SOP_", "").replace("_", "\n")
                dst = row["to_doc"].replace("SOP_", "").replace("_", "\n")
                if G.has_edge(src, dst):
                    G[src][dst]["weight"] += 1
                else:
                    G.add_edge(src, dst, weight=1, action=row["action_type"])

            if len(G.nodes()) > 0:
                pos = nx.spring_layout(G, seed=42, k=2.5)
                fig, ax = plt.subplots(figsize=(7, 5))
                fig.patch.set_facecolor('#FFFFFF')
                ax.set_facecolor('#f9fafb')

                edge_colors = [color_map.get(G[u][v]["action"], "#d1d5db") for u, v in G.edges()]
                edge_widths = [0.8 + G[u][v]["weight"] * 0.6 for u, v in G.edges()]

                nx.draw_networkx_edges(G, pos, ax=ax,
                    edge_color=edge_colors, width=edge_widths, alpha=0.75,
                    arrows=True, arrowsize=14,
                    connectionstyle='arc3,rad=0.1',
                    min_source_margin=20, min_target_margin=20)
                nx.draw_networkx_nodes(G, pos, ax=ax,
                    node_color="#111827", node_size=1800, alpha=0.9)
                nx.draw_networkx_labels(G, pos, ax=ax,
                    font_size=6, font_color='white', font_weight='500')

                legend_elements = [
                    mpatches.Patch(color="#3D7EFF", label="Forward"),
                    mpatches.Patch(color="#FF9500", label="Cross-reference"),
                    mpatches.Patch(color="#FF3B30", label="Loopback"),
                ]
                ax.legend(handles=legend_elements, loc='lower left',
                          frameon=True, framealpha=0.9, fontsize=7.5,
                          facecolor='white', edgecolor='#e5e7eb')
                ax.axis('off')
                fig.tight_layout()
                st.pyplot(fig)
                plt.close()

                st.markdown("""
                <div class="insight">
                  Each arrow represents a navigation between documents.
                  <span style="color:#FF3B30">Red</span> = loopback (revisit),
                  <span style="color:#FF9500">Orange</span> = cross-reference navigation,
                  <span style="color:#3D7EFF">Blue</span> = first visit to new document.
                  Thicker arrows indicate more frequent navigation.
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-header'>📊 Document Visit Count</div>", unsafe_allow_html=True)

            visit_counts = df["to_doc"].value_counts()
            short_names = [k.replace("SOP_", "").replace("_", " ") for k in visit_counts.index]
            colors = ["#FF3B30" if v > 1 else "#3D7EFF" for v in visit_counts.values]

            fig, ax = plt.subplots(figsize=(6, 4))
            bars = ax.barh(short_names, visit_counts.values,
                           color=colors, height=0.5, edgecolor='none')
            for bar, val in zip(bars, visit_counts.values):
                ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                        str(val), va='center', ha='left', fontsize=8.5,
                        color='#6b7280', fontfamily='monospace')
            ax.set_xlabel("Visit count")
            ax.set_title("Document visit count (red = loopback occurred)", fontsize=9,
                         color='#4b5563', pad=8, loc='left')
            ax.spines['bottom'].set_visible(True)
            ax.spines['bottom'].set_color('#e5e7eb')
            ax.set_xlim(0, visit_counts.max() * 1.2)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.markdown("<div class='section-header' style='margin-top:1.5rem;'>⏱ Average Time per Document</div>", unsafe_allow_html=True)
            if st.session_state.doc_visit_times:
                time_data = {
                    k.replace("SOP_", "").replace("_", " "): round(np.mean(v), 1)
                    for k, v in st.session_state.doc_visit_times.items()
                }
                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.barh(list(time_data.keys()), list(time_data.values()),
                        color='#6b7280', height=0.5, edgecolor='none', alpha=0.7)
                ax.set_xlabel("Average time spent (seconds)")
                ax.set_title("Average time per document", fontsize=9, color='#4b5563', pad=8, loc='left')
                ax.spines['bottom'].set_visible(True)
                ax.spines['bottom'].set_color('#e5e7eb')
                fig.tight_layout()
                st.pyplot(fig)
                plt.close()

        st.markdown("<div class='section-header'>🔢 Navigation Sequence Log</div>", unsafe_allow_html=True)
        display_df = df[["timestamp", "from_doc", "to_doc", "action_type", "visit_count"]].copy()
        display_df.columns = ["Time", "From", "To", "Action type", "Visit #"]
        display_df["From"] = display_df["From"].fillna("—").str.replace("SOP_","").str.replace("_"," ")
        display_df["To"] = display_df["To"].str.replace("SOP_","").str.replace("_"," ")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("<div class='section-header'>💬 Post-task Questions</div>", unsafe_allow_html=True)

        with st.form("post_task"):
            q1 = st.text_area("Q1. Where did you feel most confused or uncertain?", height=80)
            q2 = st.radio("Q2. How difficult was it to find the information you needed?",
                          ["Very easy", "Easy", "Neutral", "Difficult", "Very difficult"])
            q3 = st.radio("Q3. Did you find yourself revisiting the same document repeatedly?",
                          ["Yes", "No"])
            q4 = st.text_area("Q4. Any suggestions for improvement? (optional)", height=60)
            submitted = st.form_submit_button("Submit →", use_container_width=True, type="primary")
            if submitted:
                st.success("Response recorded. Thank you!")
                st.markdown(f"""
                **Response summary**
                - Q1: {q1}
                - Q2: {q2}
                - Q3: {q3}
                - Q4: {q4 if q4 else '—'}
                """)

        st.markdown("<div class='section-header'>💾 Export Data</div>", unsafe_allow_html=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"nav_log_{st.session_state.user_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

        if st.button("↩ Return to start"):
            for key in ["mode", "user_id", "current_doc", "nav_log",
                        "doc_visit_times", "doc_visit_count",
                        "last_visit_start", "session_start"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        if st.button("🏠 Home", use_container_width=False):
            for key in ["mode", "user_id", "current_doc", "nav_log",
                        "doc_visit_times", "doc_visit_count",
                        "last_visit_start", "session_start"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.caption("Cognitive Navigation Explorer · HCI Research Prototype · Sora Kim")
