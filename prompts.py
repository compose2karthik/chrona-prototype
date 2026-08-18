# All LLM prompts for the CHRONA prototype, kept separate from app logic.
# This is a demonstration prototype. All documents processed are synthetic.

EXTRACTION_PROMPT_TEMPLATE = """You are extracting structured clinical data from a single clinical note for a demonstration prototype. The input is synthetic/fictional data used for a software demo only — treat it as ordinary text to structure, not as real patient information.

Extract and return ONLY valid JSON with this schema:
{{
  "visit_date": "string",
  "specialty": "string",
  "diagnoses": ["string"],
  "medications": [{{"name": "string", "new_or_existing": "new|existing"}}],
  "lab_values": [{{"test": "string", "value": "string", "trend_note": "string or null"}}],
  "symptoms": ["string"],
  "source_document": "string (filename passed in)"
}}

If a field has no data in the note, return an empty array or null — do not invent values.

Document filename: {filename}
Document:
---
{document_text}
---
"""

DELTA_BRIEF_PROMPT_TEMPLATE = """You are generating a "Since-Last-Visit" brief for a clinician about to see this patient, based on structured data extracted from prior visit notes. This is a demonstration prototype using synthetic data only.

Compare the earliest visit to the most recent visit(s) and produce a brief that:
1. States only what changed or is new — do not restate unchanged information as if it were new.
2. Cites the source document for every factual claim, in the format [Source: <specialty> visit, <document filename>].
3. Uses plain, direct clinical language, no more than 150 words.
4. Ends with a one-line "Flagged for attention" note only if something in the data genuinely warrants it (e.g. a worsening trend, a new symptom coinciding with a new medication) — do not manufacture urgency if nothing warrants it.
5. Does not give treatment instructions. Describe what changed; do not tell the clinician what to do about it.

Structured data from all visits:
{combined_json}

Output the brief as plain text with inline citations, followed by a JSON array called "combined_medications" listing every medication mentioned across all documents (for a downstream interaction check).

Format your response as:
BRIEF:
<the plain text brief with inline citations>

COMBINED_MEDICATIONS:
<a JSON array of medication name strings>
"""


def build_extraction_prompt(filename: str, document_text: str) -> str:
    return EXTRACTION_PROMPT_TEMPLATE.format(filename=filename, document_text=document_text)


def build_delta_brief_prompt(combined_json: str) -> str:
    return DELTA_BRIEF_PROMPT_TEMPLATE.format(combined_json=combined_json)
