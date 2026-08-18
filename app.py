"""CHRONA Doctor Portal — Streamlit demo entrypoint.

Demonstration prototype. Synthetic data only. Not for clinical use.
Not a substitute for professional medical judgment.
"""

import json
import re
import time
from datetime import datetime, timezone

import streamlit as st
from anthropic import Anthropic, APIError

import db
from interactions import check_interactions
from prompts import build_delta_brief_prompt, build_extraction_prompt
from seed_data import DOCTORS

MODEL_PRIMARY = "claude-sonnet-4-5"
MODEL_FALLBACK = "claude-haiku-4-5-20251001"

st.set_page_config(page_title="CHRONA Doctor Portal", page_icon="🩺", layout="wide")

PALETTE = {
    "primary": "#1a56db",
    "primary_dark": "#1341b0",
    "primary_light": "#e8f0fe",
    "success": "#057a55",
    "success_light": "#def7ec",
    "warning": "#c27803",
    "warning_light": "#fdf6b2",
    "danger": "#c81e1e",
    "danger_light": "#fde8e8",
    "purple": "#7e3af2",
    "purple_light": "#edebfe",
    "gray_500": "#6b7280",
    "gray_700": "#374151",
    "gray_900": "#111827",
}


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

db.init_db()
db.seed_if_empty()

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; max-width: 1200px; }
    .chrona-badge { display:inline-block; font-size:11px; font-weight:700; padding:2px 10px;
        border-radius:12px; margin-left:6px; }
    .chrona-patient-card { border:1px solid #e5e7eb; border-radius:10px; padding:12px 16px;
        margin-bottom:8px; }
    .chrona-tag { background:#f3f4f6; border-radius:16px; padding:3px 10px; font-size:12px;
        margin-right:6px; display:inline-block; margin-bottom:4px; }
    .chrona-vital-chip { background:#f9fafb; border:1px solid #e5e7eb; border-radius:8px;
        padding:8px 12px; display:inline-block; margin-right:8px; margin-bottom:8px; min-width:90px; }
    .chrona-vital-label { font-size:10px; color:#9ca3af; font-weight:700; text-transform:uppercase; }
    .chrona-vital-val { font-size:18px; font-weight:800; }
    .chrona-header-banner { background:linear-gradient(135deg,#0f2045,#1a56db); border-radius:12px;
        padding:20px 24px; color:#fff; margin-bottom:16px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_client():
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    except Exception:
        api_key = None
    return Anthropic(api_key=api_key) if api_key else None


def compliance_banner():
    st.warning(
        "**Demonstration prototype. Synthetic data only. Not for clinical use. "
        "Not a substitute for professional medical judgment.**"
    )


def badge_html(text, bg, color):
    return f'<span class="chrona-badge" style="background:{bg};color:{color}">{text}</span>'


def status_color(status):
    return {"ok": PALETTE["success"], "warn": PALETTE["warning"], "alert": PALETTE["danger"]}.get(status, PALETTE["gray_700"])


# ---------------------------------------------------------------------------
# LLM helpers (extraction + delta brief), cache-first
# ---------------------------------------------------------------------------

def extract_json_object(text: str) -> dict:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    match = re.search(r"\{.*\}", candidate, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response.")
    return json.loads(match.group(0))


def extract_json_array(text: str) -> list:
    fenced = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    match = re.search(r"\[.*\]", candidate, re.DOTALL)
    if not match:
        return []
    return json.loads(match.group(0))


def call_claude(client, prompt, model=MODEL_PRIMARY):
    try:
        response = client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
        return response.content[0].text
    except APIError:
        if model == MODEL_PRIMARY:
            return call_claude(client, prompt, model=MODEL_FALLBACK)
        raise


def run_extraction(client, filename, document_text):
    prompt = build_extraction_prompt(filename, document_text)
    raw = call_claude(client, prompt)
    data = extract_json_object(raw)
    data.setdefault("source_document", filename)
    return data


def run_delta_brief(client, extracted_records):
    combined_json = json.dumps(extracted_records, indent=2)
    prompt = build_delta_brief_prompt(combined_json)
    raw = call_claude(client, prompt)
    brief_match = re.search(r"BRIEF:\s*(.*?)\s*COMBINED_MEDICATIONS:", raw, re.DOTALL)
    brief_text = brief_match.group(1).strip() if brief_match else raw.strip()
    meds_match = re.search(r"COMBINED_MEDICATIONS:\s*(.*)", raw, re.DOTALL)
    combined_medications = extract_json_array(meds_match.group(1)) if meds_match else []
    return brief_text, combined_medications


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def render_brief_with_citation_check(brief_text):
    for sentence in split_sentences(brief_text):
        has_citation = bool(re.search(r"\[Source:.*?\]", sentence))
        if has_citation:
            st.markdown(f"- {sentence}")
        else:
            st.markdown(f"- :warning: *(no citation found)* {sentence}")


def get_or_generate_summary(client, patient):
    documents = db.get_documents(patient["id"])
    if len(documents) < 2:
        return {"brief_text": None, "combined_medications": [], "single_visit": True}, documents

    doc_hash = db.compute_doc_hash(documents)
    cached = db.get_cached_summary(patient["id"], doc_hash)
    if cached:
        cached["from_cache"] = True
        return cached, documents

    if client is None:
        return None, documents

    start = time.time()
    extracted_records = [
        run_extraction(client, f"{d['specialty']}_{d['visit_date']}.txt", d["raw_text"]) for d in documents
    ]
    brief_text, combined_medications = run_delta_brief(client, extracted_records)
    elapsed = time.time() - start

    generated_at = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    db.save_summary(patient["id"], doc_hash, brief_text, combined_medications, generated_at, elapsed)
    return {
        "brief_text": brief_text,
        "combined_medications": combined_medications,
        "generated_at": generated_at,
        "generation_seconds": elapsed,
        "from_cache": False,
        "single_visit": False,
    }, documents


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

if "doctor_username" not in st.session_state:
    st.session_state.doctor_username = None
if "view" not in st.session_state:
    st.session_state.view = "dashboard"
if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = "priya"

if not st.session_state.doctor_username:
    compliance_banner()
    st.title("🩺 CHRONA Doctor Portal")
    st.caption("Longitudinal Intelligence for Specialty Care · One Patient. One Card.")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="e.g. doctor1")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign in to Doctor Portal", type="primary")

    if submitted:
        account = DOCTORS.get(username)
        if account and account["password"] == password:
            st.session_state.doctor_username = username
            st.rerun()
        else:
            st.error("Incorrect username or password. Please try again.")

    st.info(
        "**Demo credentials — pick any of these test accounts:**\n\n"
        + "\n".join(
            f"- `{u}` / `{a['password']}` — {a['name']} ({a['specialty']})"
            for u, a in DOCTORS.items()
        )
    )
    st.caption("CHRONA v1.0 · Horizon 1 Pilot · DBA Capstone Group 5 · August 2026")
    st.stop()

doctor = DOCTORS[st.session_state.doctor_username]

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown(f"### 🩺 CHRONA")
    st.caption("Specialty Care")
    st.markdown(f"**{doctor['name']}**  \n{doctor['specialty']} · 🟢 Online")
    st.divider()

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.view = "dashboard"
        st.rerun()
    if st.button("👥 My Patients", use_container_width=True):
        st.session_state.view = "patients"
        st.rerun()
    if st.button("🗂️ Patient Card", use_container_width=True):
        st.session_state.view = "patient-card"
        st.rerun()
    if st.button("⚠️ Safety Alerts", use_container_width=True):
        st.session_state.view = "alerts"
        st.rerun()

    st.divider()
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.doctor_username = None
        st.rerun()

    st.caption("CHRONA · Horizon 1 Pilot  \nRegulatory: SaMD pathway (CDSCO) — demo only")

compliance_banner()

patients = db.list_patients()
patients_by_id = {p["id"]: p for p in patients}


# ---------------------------------------------------------------------------
# Dashboard view
# ---------------------------------------------------------------------------

def all_patient_ddi_flags():
    results = []
    for p in patients:
        med_names = [m["name"] for m in p["medications"]]
        flags = check_interactions(med_names)
        for f in flags:
            results.append((p, f))
    return results


if st.session_state.view == "dashboard":
    st.title("Dashboard")
    st.caption(f"{len(patients)} patients on file · Cardiology")

    ddi_flags = all_patient_ddi_flags()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Patients on File", len(patients))
    col2.metric("DDI Alerts", len(ddi_flags))
    col3.metric("Briefs Generated", db.count_summaries())
    col4.metric("ADR Reports (session)", len(st.session_state.get("adr_submissions", [])))

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Patient Queue")
        for p in patients:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"**{p['name']}**  \n{p['meta_short']}")
                if c2.button("Open", key=f"open_{p['id']}"):
                    st.session_state.selected_patient_id = p["id"]
                    st.session_state.view = "patient-card"
                    st.rerun()

    with right:
        st.subheader("🔴 Safety Alerts")
        st.caption("Advisory · confirm to acknowledge")
        if ddi_flags:
            for p, f in ddi_flags[:5]:
                st.markdown(f"**{f['title']}**  \n{p['name']} · Severity {f['severity']}")
                st.caption(f"{f['matched_a']} ↔ {f['matched_b']}")
        else:
            st.caption("No interaction flags on file.")


# ---------------------------------------------------------------------------
# Patients list view
# ---------------------------------------------------------------------------

elif st.session_state.view == "patients":
    st.title("My Patients")
    st.caption(f"{len(patients)} patients · Cardiology")
    search = st.text_input("🔍 Search patients…")

    filtered = [p for p in patients if search.lower() in p["name"].lower() or search.lower() in p["meta_short"].lower()] if search else patients

    for p in filtered:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{p['name']}**  \n{p['meta_short']} · {p['badge']}")
            if c2.button("Open Card", key=f"list_open_{p['id']}"):
                st.session_state.selected_patient_id = p["id"]
                st.session_state.view = "patient-card"
                st.rerun()


# ---------------------------------------------------------------------------
# Alerts view (all patients)
# ---------------------------------------------------------------------------

elif st.session_state.view == "alerts":
    st.title("Safety Alerts — All Patients")
    st.info("All alerts are advisory only. CHRONA's cross-specialist safety check has surfaced these flags. Clinician confirmation is required before any alert is recorded or acted upon.")

    ddi_flags = all_patient_ddi_flags()
    if not ddi_flags:
        st.caption("No interaction flags on file.")
    for p, f in ddi_flags:
        with st.container(border=True):
            st.markdown(f"**{p['name']} · {f['title']}**")
            st.caption(f"{f['matched_a']} ↔ {f['matched_b']} · Severity {f['severity']} (illustrative)")
            if st.button("Open patient card", key=f"alert_open_{p['id']}_{f['title']}"):
                st.session_state.selected_patient_id = p["id"]
                st.session_state.view = "patient-card"
                st.rerun()


# ---------------------------------------------------------------------------
# Patient card view
# ---------------------------------------------------------------------------

elif st.session_state.view == "patient-card":
    patient = patients_by_id.get(st.session_state.selected_patient_id, patients[0])

    tags_html = "".join(
        f'<span class="chrona-tag" style="background:rgba(255,255,255,.15);color:#fff">{t}</span>'
        for t in patient["conditions_tags"]
    )
    banner_html = (
        f'<div class="chrona-header-banner">'
        f'<div style="font-size:22px;font-weight:800">{patient["name"]}</div>'
        f'<div style="font-size:13px;color:rgba(255,255,255,.75)">'
        f'{patient["age"]} years · {patient["gender"]} &nbsp;·&nbsp; DOB: {patient["dob"]} &nbsp;·&nbsp; {patient["location"]}'
        f"</div>"
        f'<div style="margin-top:10px">{tags_html}</div>'
        f'<div style="margin-top:10px;font-size:11px;color:rgba(255,255,255,.6)">CHRONA ID: <strong>{patient["chr_id"]}</strong></div>'
        f"</div>"
    )
    st.markdown(banner_html, unsafe_allow_html=True)

    tab_overview, tab_slv, tab_timeline, tab_ddi, tab_adr = st.tabs(
        ["📋 Overview", "🔄 Since Last Visit", "📈 Timeline", "⚠️ DDI Alerts", "📋 ADR Report"]
    )

    # ---- Overview ----
    with tab_overview:
        st.markdown("**Vitals**")

        def _vital_chip(label, val, unit, status, trend):
            trend_html = f'<div style="font-size:10px;color:{status_color(status)}">{trend}</div>' if trend else ""
            return (
                f'<div class="chrona-vital-chip">'
                f'<div class="chrona-vital-label">{label}</div>'
                f'<div class="chrona-vital-val" style="color:{status_color(status)}">{val} '
                f'<span style="font-size:11px;color:#9ca3af">{unit}</span></div>'
                f"{trend_html}"
                f"</div>"
            )

        vitals_html = "".join(_vital_chip(*v) for v in patient["vitals"])
        st.markdown(vitals_html, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🧬 Active Conditions**")
            for name, status, val in patient["active_conditions"]:
                st.markdown(f"- {name} — :{'red' if status=='alert' else 'orange' if status=='warn' else 'green'}[{val}]")
        with col2:
            st.markdown("**🔬 Latest Labs**")
            for name, val, status in patient["latest_labs"]:
                st.markdown(f"- {name} — :{'red' if status=='alert' else 'orange' if status=='warn' else 'green'}[{val}]")

        st.markdown("**💊 Current Medications — All Prescribers** &nbsp; `⚡ CHRONA Cross-Specialist View`")
        new_tag = ' <span style="color:#ef4444;font-size:10px">NEW</span>'
        med_rows = "".join(
            f"<tr><td><strong>{m['name']}</strong>{new_tag if m['new'] else ''}</td>"
            f"<td>{m['dose']}</td><td>{m['since']}</td><td>{m['prescriber']}</td>"
            f"<td><span style='font-size:10px;background:#e0e7ff;color:#3730a3;padding:2px 6px;border-radius:4px'>{m['specialty']}</span></td></tr>"
            for m in patient["medications"]
        )
        st.markdown(
            f"""<table style="width:100%;font-size:13px">
            <tr style="color:#9ca3af;font-size:11px;text-transform:uppercase">
                <th style="text-align:left">Medication</th><th style="text-align:left">Dose</th>
                <th style="text-align:left">Since</th><th style="text-align:left">Prescriber</th><th style="text-align:left">Specialty</th>
            </tr>{med_rows}</table>""",
            unsafe_allow_html=True,
        )

        st.markdown("**🏥 Care Team**")
        for label, val in patient["care_team"]:
            st.markdown(f"- {label}: **{val}**")

    # ---- Since Last Visit ----
    with tab_slv:
        st.info(
            "**AI-Generated · Advisory Only.** Every statement is grounded in a source document. "
            "No clinical action is taken automatically — clinician confirmation is required."
        )
        client = get_client()

        if st.button("⚡ Generate Since-Last-Visit Brief", key="gen_brief", type="primary"):
            with st.spinner("Checking cache and generating if needed…"):
                result, documents = get_or_generate_summary(client, patient)
            st.session_state[f"summary_{patient['id']}"] = result

        result = st.session_state.get(f"summary_{patient['id']}")
        if result is None:
            documents = db.get_documents(patient["id"])
            if len(documents) >= 2:
                doc_hash = db.compute_doc_hash(documents)
                cached = db.get_cached_summary(patient["id"], doc_hash)
                if cached:
                    cached["from_cache"] = True
                    result = cached

        if result is not None and result.get("single_visit"):
            st.caption("This is the patient's only visit on file — no since-last-visit comparison available yet.")
        elif result is not None and result.get("brief_text"):
            source_tag = "📦 served from cache (no API call)" if result.get("from_cache") else f"⚡ freshly generated in {result.get('generation_seconds', 0):.1f}s"
            st.caption(f"Generated {result.get('generated_at', '')} · {source_tag}")
            render_brief_with_citation_check(result["brief_text"])
            if result.get("combined_medications"):
                with st.expander("Medications the AI extracted from these notes (for verification)"):
                    st.write(", ".join(result["combined_medications"]))
        elif client is None:
            st.error("No ANTHROPIC_API_KEY configured — add it in Streamlit secrets to generate briefs.")
        else:
            st.caption("Click **Generate Since-Last-Visit Brief** to produce a cited summary of what changed.")

        with st.expander("➕ Add a new document for this patient (report, visit note, prescription)"):
            st.caption("Adding a document invalidates the cache — the next generation will call the LLM again.")
            new_specialty = st.text_input("Specialty", key=f"new_spec_{patient['id']}")
            new_date = st.text_input("Visit date (YYYY-MM-DD)", key=f"new_date_{patient['id']}")
            new_text = st.text_area("Document text (synthetic only)", key=f"new_text_{patient['id']}", height=150)
            if st.button("Add document", key=f"add_doc_{patient['id']}") and new_text and new_date:
                db.add_document(patient["id"], new_date, new_specialty or "General", "—", "—", new_text)
                st.session_state.pop(f"summary_{patient['id']}", None)
                st.success("Document added. Generate the brief again to see the updated delta.")
                st.rerun()

    # ---- Timeline ----
    with tab_timeline:
        st.caption("CHRONA Health Graph — assembled from all specialist visits, labs, and prescriptions on file.")
        documents = db.get_documents(patient["id"])
        for d in reversed(documents):
            with st.container(border=True):
                st.markdown(f"**{d['visit_date']} · {d['specialty']}** — {d['doctor']}, {d['facility']}")
                if d["labs"]:
                    st.markdown(" ".join(f"`{lab}`" for lab in d["labs"]))
                with st.expander("View note"):
                    st.text(d["raw_text"])

    # ---- DDI Alerts ----
    with tab_ddi:
        st.warning(
            "**Advisory Only — Clinician Confirmation Required.** These flags come from CHRONA's illustrative "
            "cross-specialist interaction list (Section 7.3) — not a licensed clinical database (RxNorm/CDSCO-mapped). "
            "No action is recorded unless explicitly confirmed."
        )
        med_names = [m["name"] for m in patient["medications"]]
        flags = check_interactions(med_names)
        if not flags:
            st.success("✅ No illustrative cross-specialist interactions detected for this patient's current medication list.")
        for i, f in enumerate(flags):
            with st.container(border=True):
                st.markdown(f"##### {f['title']}  \n`Severity {f['severity']} (illustrative)`")
                st.caption(f"{f['matched_a']} ↔ {f['matched_b']}")
                st.markdown(f"**Mechanism:** {f['mechanism']}")
                st.markdown(f"**Why flagged:** {f['why_flagged']}")
                st.markdown(f"**Note:** {f['note']}")
                c1, c2 = st.columns(2)
                if c1.button("✓ Acknowledge & Document", key=f"ack_{patient['id']}_{i}"):
                    st.success("Acknowledged and documented (session only, not persisted in this demo).")
                if c2.button("Dismiss", key=f"dismiss_{patient['id']}_{i}"):
                    st.caption("Dismissed (session only, not persisted in this demo).")

    # ---- ADR Report ----
    with tab_adr:
        st.info(
            "Confirmed ADRs would route to India's Pharmacovigilance Programme (PvPI) and CDSCO in the full product. "
            "**This is a mock form — nothing is actually submitted anywhere.**"
        )
        with st.form(f"adr_form_{patient['id']}"):
            st.text_input("Patient (pre-filled)", value=f"{patient['name']} · {patient['chr_id']}", disabled=True)
            st.text_input("Reporting Doctor", value=f"{doctor['name']} · {doctor['specialty']}", disabled=True)
            drug = st.selectbox("Suspected Drug", [m["name"] for m in patient["medications"]])
            reaction = st.text_area("Adverse Reaction Description")
            col1, col2 = st.columns(2)
            onset = col1.date_input("Onset Date")
            severity = col2.selectbox("Severity", ["Mild", "Moderate", "Severe", "Life-threatening", "Fatal"])
            outcome = st.selectbox("Outcome", ["Recovered / Resolved", "Recovering", "Not yet recovered", "Recovered with sequelae", "Fatal", "Unknown"])
            notes = st.text_area("Additional Clinical Notes")
            submitted = st.form_submit_button("📋 Generate Mock PvPI Report Preview")

        if submitted:
            ref = f"PvPI-DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            st.session_state.setdefault("adr_submissions", []).append(ref)
            st.success(f"Mock report generated — reference **{ref}** (demo only, nothing was actually submitted).")
            st.code(
                f"FORM 12B — Suspected ADR Report (MOCK)\n"
                f"Patient: {patient['name']} · {patient['chr_id']}\n"
                f"Reporter: {doctor['name']} ({doctor['specialty']})\n"
                f"Suspected Drug: {drug}\n"
                f"Reaction: {reaction or '[not entered]'}\n"
                f"Onset: {onset} · Severity: {severity} · Outcome: {outcome}\n"
                f"Notes: {notes or '[none]'}\n"
                f"Routed to: [DEMO ONLY — not actually routed to PvPI/CDSCO]",
                language="text",
            )
