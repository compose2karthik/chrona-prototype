# ILLUSTRATIVE ONLY — not a licensed clinical interaction database.
# A production system would use a CDSCO-formulary-mapped, RxNorm-aligned
# commercial database. This list exists solely to demonstrate the mechanism.
#
# "severity" is an illustrative A/B/C label loosely inspired by common DDI
# grading conventions — it does not correspond to any licensed source.

DEMO_INTERACTIONS = [
    {
        "drug_a": "ARB",
        "drug_b": "metformin",
        "severity": "A",
        "title": "Reduced renal clearance in CKD — lactic acidosis risk",
        "mechanism": "ARBs can reduce renal perfusion, which may further impair metformin clearance in patients with reduced kidney function, raising the risk of metformin-associated lactic acidosis.",
        "why_flagged": "These two medications are commonly prescribed by different specialists (e.g. nephrology and endocrinology) who may not see each other's medication lists — a cross-specialist view is what surfaces this combination.",
        "note": "Renal function and metformin dosing are worth discussing between prescribers, particularly in CKD.",
    },
    {
        "drug_a": "ARB",
        "drug_b": "loop diuretic",
        "severity": "B",
        "title": "Hyperkalaemia risk in reduced renal function",
        "mechanism": "ARBs reduce aldosterone-mediated potassium excretion; combined with a loop diuretic in the context of declining renal function, potassium balance can shift unpredictably.",
        "why_flagged": "Worth monitoring given the combination and current renal trend, even when prescribed by the same clinician.",
        "note": "Potassium and renal function monitoring worth considering.",
    },
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "potassium-sparing diuretic",
        "severity": "B",
        "title": "Elevated potassium risk",
        "mechanism": "Both drug classes reduce potassium excretion through complementary mechanisms, which can compound in combination.",
        "why_flagged": "Flagged whenever both classes appear on a patient's combined medication list.",
        "note": "Combined use may raise potassium levels — renal function and potassium monitoring advised.",
    },
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "NSAID",
        "severity": "B",
        "title": "Reduced renal perfusion",
        "mechanism": "NSAIDs reduce prostaglandin-mediated renal blood flow, which can blunt the effect of ACE inhibitors and reduce kidney function, particularly relevant in existing CKD.",
        "why_flagged": "Common combination worth surfacing when a patient reports intermittent NSAID/analgesic use not visible to the prescribing specialist.",
        "note": "Combined use may reduce kidney function, particularly relevant given existing CKD — monitoring advised.",
    },
    {
        "drug_a": "metformin",
        "drug_b": "iodinated contrast dye",
        "severity": "B",
        "title": "Contrast-associated renal risk",
        "mechanism": "Iodinated contrast can transiently reduce renal function, which may impair metformin clearance.",
        "why_flagged": "Relevant to flag before any imaging study involving contrast.",
        "note": "Contrast studies may require a temporary metformin hold — flag before any imaging with contrast.",
    },
    {
        "drug_a": "warfarin",
        "drug_b": "NSAID",
        "severity": "B",
        "title": "Elevated bleeding risk",
        "mechanism": "NSAIDs (including aspirin at antiplatelet doses) impair platelet function and can potentiate warfarin's anticoagulant effect, raising bleeding risk.",
        "why_flagged": "Worth surfacing whenever both appear on the combined medication list, especially with a therapeutic INR.",
        "note": "Combined use raises bleeding risk — monitoring advised.",
    },
    {
        "drug_a": "amiodarone",
        "drug_b": "levothyroxine",
        "severity": "B",
        "title": "Thyroid function interplay",
        "mechanism": "Amiodarone contains iodine and can affect thyroid hormone metabolism, altering the effective dose of levothyroxine and TSH levels over time.",
        "why_flagged": "Relevant when levothyroxine is newly started or adjusted by a different prescriber while amiodarone continues.",
        "note": "Thyroid function trends are worth tracking together when both medications are in use.",
    },
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "metformin",
        "severity": "C",
        "title": "Shared renal handling",
        "mechanism": "No major direct pharmacologic interaction, but both drug classes are influenced by renal function.",
        "why_flagged": "Low-severity, informational pairing — relevant to monitor together in a CKD patient.",
        "note": "No major direct interaction, but both affect renal handling — relevant to monitor together in a CKD patient.",
    },
]

# Keyword aliases so simple substring matching can recognize a drug class
# from a specific brand/generic name mentioned in a clinical note or
# structured medication list. This is a demo convenience, not a substitute
# for real drug-class ontology (RxNorm).
_CLASS_ALIASES = {
    "ACE inhibitor": ["ace inhibitor", "lisinopril", "enalapril", "ramipril", "captopril"],
    "ARB": ["arb", "losartan", "valsartan", "telmisartan", "olmesartan", "irbesartan"],
    "potassium-sparing diuretic": ["potassium-sparing diuretic", "spironolactone", "eplerenone", "amiloride"],
    "loop diuretic": ["loop diuretic", "furosemide", "torsemide", "bumetanide"],
    "NSAID": ["nsaid", "ibuprofen", "naproxen", "diclofenac", "aspirin"],
    "metformin": ["metformin"],
    "iodinated contrast dye": ["contrast dye", "iodinated contrast", "contrast media"],
    "warfarin": ["warfarin"],
    "amiodarone": ["amiodarone"],
    "levothyroxine": ["levothyroxine", "thyroxine"],
}


def _mentions_class(medication_name: str, drug_class: str) -> bool:
    name = medication_name.lower()
    for alias in _CLASS_ALIASES.get(drug_class, [drug_class.lower()]):
        if alias in name:
            return True
    return False


def check_interactions(combined_medications):
    """Match a flat list of medication names against the illustrative
    interaction pairs above, using simple substring/keyword matching.

    Returns a list of matched interaction dicts (from DEMO_INTERACTIONS),
    each augmented with the specific medication names that triggered it.
    """
    flags = []
    for pair in DEMO_INTERACTIONS:
        match_a = next((m for m in combined_medications if _mentions_class(m, pair["drug_a"])), None)
        match_b = next((m for m in combined_medications if _mentions_class(m, pair["drug_b"])), None)
        if match_a and match_b:
            flags.append({**pair, "matched_a": match_a, "matched_b": match_b})
    return flags
