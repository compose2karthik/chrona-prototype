# CHRONA Prototype

**Demonstration prototype. Synthetic data only. Not for clinical use. Not a
substitute for professional medical judgment.**

This is a thin vertical slice built to prove one mechanism: given two or
more documents from the same (fictional) patient across visits, the system
generates a cited, accurate "what changed" brief and flags one illustrative
drug interaction.

It is a capstone-project demo (DBA, Cohort 11, Group 5) for a Generative AI
venture concept called **CHRONA** — a longitudinal patient card aimed at
independent Indian specialty clinics. This prototype demonstrates the core
mechanism behind Patent Claim 1 (inter-visit delta briefing) and, partially,
Claim 4 (cross-specialist interaction detection) in miniature. It is **not**
the full product.

## What this demo does

- Loads three synthetic clinical documents for one fictional patient (a
  58-year-old woman with Type 2 diabetes and Stage 3 CKD, seen by three
  specialists who don't share records) — see `sample_data/`.
- Extracts structured clinical data from each document with an LLM.
- Generates a "Since-Last-Visit" brief comparing the earliest visit to the
  most recent visit(s), with every claim citing its source document.
- Flags one illustrative drug interaction (ACE inhibitor newly prescribed
  in cardiology, against the patient's existing regimen and CKD status)
  against a small, explicitly-labelled illustrative interaction list — not
  a licensed clinical drug-interaction database.
- Visually flags any generated sentence that lacks a source citation, and
  styles interaction flags as advisory (amber, "for clinician review"), not
  alarming.

## Explicitly out of scope

- Real document upload via WhatsApp/email/scanner, or vision-based
  extraction from scanned images
- A real vector database or retrieval pipeline
- ABDM/FHIR/EMR integration of any kind
- User accounts, login, multi-patient persistence, or a real database
- Any payment, billing, or subscription logic
- A licensed clinical drug-interaction database (RxNorm/CDSCO-mapped)

## Running locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and add your ANTHROPIC_API_KEY
streamlit run app.py
```

## Deploying (free tier)

**Streamlit Community Cloud**
1. Push this repo to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the
   repo, and deploy `app.py`.
3. In the app's Settings → Secrets, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

**Hugging Face Spaces** (alternative)
1. Create a new Space with SDK = Streamlit.
2. Push this repo's contents to the Space.
3. In Space Settings → Repository secrets, add `ANTHROPIC_API_KEY`.

## Repository structure

```
chrona-prototype/
├── app.py                  # Streamlit entrypoint
├── prompts.py               # All LLM prompts, kept separate from app logic
├── sample_data/              # Synthetic (fictional) sample documents
├── interactions.py          # Illustrative interaction-pair list
├── requirements.txt
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example  # Template only — real secrets.toml is gitignored
└── README.md
```

## Guardrails demonstrated (lightweight)

1. **Source citation enforcement** — any sentence in the generated brief
   without a `[Source: ...]` tag is flagged with a warning icon in the UI
   instead of being silently accepted.
2. **Advisory-only labelling** — interaction flags are styled as
   informational (amber, "for review"), never as directive or alarming.

These are two illustrative guardrail touches, not the full guardrail suite
from the CHRONA product design (which also includes PII masking, namespace
isolation, and consent-token gating — out of scope for this prototype).

## Data notice

Every patient, document, and clinical detail in this repository is
fabricated for demonstration purposes. No real patient data was used,
requested, or processed anywhere in this project.
