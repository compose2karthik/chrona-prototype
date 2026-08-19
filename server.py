"""CHRONA Doctor Portal — Flask backend.

Serves the static doctor-portal frontend (index.html, byte-identical to the
provided design) and a small JSON API backing it: patients, documents,
cache-first Since-Last-Visit brief generation, and illustrative DDI checks.

Demonstration prototype. Synthetic data only. Not for clinical use.
Not a substitute for professional medical judgment.
"""

import html
import os
import re
import time
from datetime import datetime, timezone

from anthropic import Anthropic, APIError
from flask import Flask, jsonify, request, send_from_directory

import db
from interactions import check_interactions
from prompts import build_delta_brief_prompt, build_extraction_prompt
from seed_data import DOCTORS

MODEL_PRIMARY = "claude-sonnet-4-5"
MODEL_FALLBACK = "claude-haiku-4-5-20251001"

app = Flask(__name__, static_folder=".", static_url_path="")

db.init_db()
db.seed_if_empty()


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    return Anthropic(api_key=api_key) if api_key else None


# ---------------------------------------------------------------------------
# LLM helpers (extraction + delta brief), cache-first — same mechanism as
# the earlier Streamlit build, adapted to a plain Python backend.
# ---------------------------------------------------------------------------

def extract_json_object(text: str) -> dict:
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    match = re.search(r"\{.*\}", candidate, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response.")
    import json

    return json.loads(match.group(0))


def extract_json_array(text: str) -> list:
    import json

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
    import json

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


def brief_text_to_html(brief_text: str) -> str:
    """Render a brief as HTML using the mockup's existing `.cited` hover-tooltip
    styling — any sentence without a [Source: ...] tag is instead wrapped with
    a visible warning marker, per the citation-enforcement guardrail."""
    parts = []
    for sentence in split_sentences(brief_text):
        m = re.search(r"\[Source:\s*(.*?)\]", sentence)
        if m:
            cite = html.escape(m.group(1))
            clean = html.escape(re.sub(r"\s*\[Source:.*?\]", "", sentence).strip())
            parts.append(f'<span class="cited" data-cite="Source: {cite}">{clean}</span>')
        else:
            clean = html.escape(sentence)
            parts.append(
                f'<span style="border-bottom:2px dotted #c81e1e" title="No citation found in this statement">'
                f"⚠️ {clean}</span>"
            )
    return " ".join(parts)


def get_or_generate_summary(client, patient):
    documents = db.get_documents(patient["id"])
    if len(documents) < 2:
        return {"single_visit": True, "brief_html": None, "combined_medications": []}

    doc_hash = db.compute_doc_hash(documents)
    cached = db.get_cached_summary(patient["id"], doc_hash)
    if cached:
        return {
            "single_visit": False,
            "brief_html": brief_text_to_html(cached["brief_text"]),
            "combined_medications": cached["combined_medications"],
            "generated_at": cached["generated_at"],
            "generation_seconds": cached["generation_seconds"],
            "from_cache": True,
        }

    if client is None:
        return {"error": "No ANTHROPIC_API_KEY configured on the server."}

    start = time.time()
    extracted_records = [
        run_extraction(client, f"{d['specialty']}_{d['visit_date']}.txt", d["raw_text"]) for d in documents
    ]
    brief_text, combined_medications = run_delta_brief(client, extracted_records)
    elapsed = time.time() - start

    generated_at = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    db.save_summary(patient["id"], doc_hash, brief_text, combined_medications, generated_at, elapsed)
    return {
        "single_visit": False,
        "brief_html": brief_text_to_html(brief_text),
        "combined_medications": combined_medications,
        "generated_at": generated_at,
        "generation_seconds": round(elapsed, 1),
        "from_cache": False,
    }


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route("/api/doctors")
def api_doctors():
    return jsonify(DOCTORS)


@app.route("/api/patients")
def api_patients():
    return jsonify(db.list_patients())


@app.route("/api/patients/<patient_id>")
def api_patient_detail(patient_id):
    patient = db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "not found"}), 404
    return jsonify(patient)


@app.route("/api/patients/<patient_id>/documents")
def api_patient_documents(patient_id):
    return jsonify(db.get_documents(patient_id))


@app.route("/api/patients/<patient_id>/documents", methods=["POST"])
def api_add_document(patient_id):
    body = request.get_json(force=True)
    db.add_document(
        patient_id,
        body.get("visit_date", ""),
        body.get("specialty", "General"),
        body.get("doctor", "—"),
        body.get("facility", "—"),
        body.get("raw_text", ""),
    )
    return jsonify({"ok": True})


@app.route("/api/patients/<patient_id>/ddi")
def api_patient_ddi(patient_id):
    patient = db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "not found"}), 404
    med_names = [m["name"] for m in patient["medications"]]
    return jsonify(check_interactions(med_names))


@app.route("/api/patients/<patient_id>/brief", methods=["POST"])
def api_patient_brief(patient_id):
    patient = db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "not found"}), 404
    client = get_client()
    result = get_or_generate_summary(client, patient)
    return jsonify(result)


@app.route("/api/dashboard")
def api_dashboard():
    patients = db.list_patients()
    all_flags = []
    for p in patients:
        med_names = [m["name"] for m in p["medications"]]
        for f in check_interactions(med_names):
            all_flags.append({**f, "patient_id": p["id"], "patient_name": p["name"]})

    deltas = []
    for p in patients:
        docs = db.get_documents(p["id"])
        if not docs:
            continue
        latest = docs[-1]
        for lab in latest.get("labs", []):
            if "↑" in lab or "↓" in lab:
                deltas.append(
                    {
                        "patient_id": p["id"],
                        "patient_name": p["name"],
                        "lab": lab,
                        "visit_date": latest["visit_date"],
                        "specialty": latest["specialty"],
                    }
                )

    return jsonify(
        {
            "patient_count": len(patients),
            "ddi_alert_count": len(all_flags),
            "briefs_generated": db.count_summaries(),
            "ddi_flags": all_flags,
            "deltas": deltas,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
