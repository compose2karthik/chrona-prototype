"""CHRONA Prototype — Streamlit demo entrypoint.

Demonstration prototype. Synthetic data only. Not for clinical use.
Not a substitute for professional medical judgment.
"""

import json
import re
from pathlib import Path

import streamlit as st
from anthropic import Anthropic, APIError

from interactions import check_interactions
from prompts import build_delta_brief_prompt, build_extraction_prompt

MODEL_PRIMARY = "claude-sonnet-4-5"
MODEL_FALLBACK = "claude-haiku-4-5-20251001"

SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"
DEFAULT_FILES = [
    "patient_visit1_endocrinology.txt",
    "patient_visit2_nephrology.txt",
    "patient_visit2_cardiology.txt",
]

st.set_page_config(page_title="CHRONA Prototype", page_icon="🩺", layout="centered")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_default_documents():
    docs = {}
    for filename in DEFAULT_FILES:
        docs[filename] = (SAMPLE_DATA_DIR / filename).read_text()
    return docs


def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


def extract_json_object(text: str) -> dict:
    """Pull the first {...} JSON object out of a possibly fenced LLM response."""
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


def call_claude(client: Anthropic, prompt: str, model: str = MODEL_PRIMARY) -> str:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except APIError:
        if model == MODEL_PRIMARY:
            return call_claude(client, prompt, model=MODEL_FALLBACK)
        raise


def run_extraction(client: Anthropic, filename: str, document_text: str) -> dict:
    prompt = build_extraction_prompt(filename, document_text)
    raw = call_claude(client, prompt)
    data = extract_json_object(raw)
    data.setdefault("source_document", filename)
    return data


def run_delta_brief(client: Anthropic, extracted_records: list) -> tuple:
    combined_json = json.dumps(extracted_records, indent=2)
    prompt = build_delta_brief_prompt(combined_json)
    raw = call_claude(client, prompt)

    brief_match = re.search(r"BRIEF:\s*(.*?)\s*COMBINED_MEDICATIONS:", raw, re.DOTALL)
    brief_text = brief_match.group(1).strip() if brief_match else raw.strip()

    meds_match = re.search(r"COMBINED_MEDICATIONS:\s*(.*)", raw, re.DOTALL)
    combined_medications = extract_json_array(meds_match.group(1)) if meds_match else []

    return brief_text, combined_medications


def split_sentences(text: str) -> list:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def render_brief_with_citation_check(brief_text: str):
    for sentence in split_sentences(brief_text):
        has_citation = bool(re.search(r"\[Source:.*?\]", sentence))
        if has_citation:
            st.markdown(f"- {sentence}")
        else:
            st.markdown(f"- :warning: *(no citation found)* {sentence}")


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.warning(
    "**Demonstration prototype. Synthetic data only. Not for clinical use. "
    "Not a substitute for professional medical judgment.**"
)

st.title("CHRONA Prototype")
st.write(
    "CHRONA generates a cited **\"Since-Last-Visit\" brief** by comparing a patient's "
    "documents across visits, so a clinician can see what changed — with every claim "
    "traceable to its source document — instead of re-reading full notes from scratch. "
    "This demo also flags illustrative drug interactions across specialists who don't "
    "share records. All data below is synthetic and fictional."
)

if "documents" not in st.session_state:
    st.session_state.documents = load_default_documents()
if "brief_text" not in st.session_state:
    st.session_state.brief_text = None
if "combined_medications" not in st.session_state:
    st.session_state.combined_medications = None

st.subheader("Patient documents (synthetic)")

for filename, text in st.session_state.documents.items():
    with st.expander(filename):
        st.text(text)

with st.expander("Use your own synthetic document instead"):
    st.caption(
        "Paste plain text for a synthetic (fictional) clinical note only. "
        "Do not paste real patient information."
    )
    custom_name = st.text_input("Document name", key="custom_name")
    custom_text = st.text_area("Document text", key="custom_text", height=150)
    if st.button("Add document") and custom_name and custom_text:
        st.session_state.documents[custom_name] = custom_text
        st.rerun()

col1, col2 = st.columns([1, 1])
generate_clicked = col1.button("Generate Since-Last-Visit Brief", type="primary")
reset_clicked = col2.button("Reset")

if reset_clicked:
    st.session_state.documents = load_default_documents()
    st.session_state.brief_text = None
    st.session_state.combined_medications = None
    st.rerun()

if generate_clicked:
    client = get_client()
    if client is None:
        st.error(
            "No ANTHROPIC_API_KEY configured. Add it to Streamlit secrets "
            "(`.streamlit/secrets.toml` locally, or the app's Secrets panel when deployed)."
        )
    else:
        with st.spinner("Extracting structured data from each document..."):
            try:
                extracted_records = [
                    run_extraction(client, filename, text)
                    for filename, text in st.session_state.documents.items()
                ]
            except Exception as exc:  # noqa: BLE001 — surface any extraction failure to the user
                st.error(f"Extraction failed: {exc}")
                extracted_records = None

        if extracted_records is not None:
            with st.spinner("Generating Since-Last-Visit brief..."):
                try:
                    brief_text, combined_medications = run_delta_brief(client, extracted_records)
                    st.session_state.brief_text = brief_text
                    st.session_state.combined_medications = combined_medications
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Brief generation failed: {exc}")

if st.session_state.brief_text:
    st.subheader("Since-Last-Visit brief")
    render_brief_with_citation_check(st.session_state.brief_text)

    st.subheader("Safety panel — illustrative drug interaction check")
    st.caption(
        "Illustrative subset only — not a licensed clinical interaction database "
        "(e.g. RxNorm/CDSCO-mapped). Demonstrates the mechanism only."
    )
    meds = st.session_state.combined_medications or []
    if meds:
        st.write("Combined medication list detected: " + ", ".join(meds))
    flags = check_interactions(meds)
    if flags:
        for flag in flags:
            st.markdown(
                f"""
<div style="background-color:#FFF3CD;border-left:6px solid #FFA500;
padding:12px;border-radius:4px;margin-bottom:8px;">
<strong>⚠️ Illustrative interaction flag — for clinician review</strong><br/>
<strong>{flag['matched_a']}</strong> + <strong>{flag['matched_b']}</strong><br/>
{flag['note']}<br/>
<em>Not a substitute for a licensed drug-interaction database.</em>
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("No illustrative interaction matches found in the combined medication list.")

st.divider()
st.caption(
    "CHRONA is a demonstration prototype for a DBA capstone project (Cohort 11, Group 5). "
    "It uses synthetic data only and is not a medical device. See README for details."
)
