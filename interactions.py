# ILLUSTRATIVE ONLY — not a licensed clinical interaction database.
# A production system would use a CDSCO-formulary-mapped, RxNorm-aligned
# commercial database. This list exists solely to demonstrate the mechanism.

DEMO_INTERACTIONS = [
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "potassium-sparing diuretic",
        "note": "Combined use may raise potassium levels — renal function and potassium monitoring advised.",
    },
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "NSAID",
        "note": "Combined use may reduce kidney function, particularly relevant given existing CKD — monitoring advised.",
    },
    {
        "drug_a": "metformin",
        "drug_b": "iodinated contrast dye",
        "note": "Contrast studies may require temporary metformin hold — flag before any imaging with contrast.",
    },
    {
        "drug_a": "warfarin",
        "drug_b": "NSAID",
        "note": "Combined use raises bleeding risk — monitoring advised.",
    },
    {
        "drug_a": "ACE inhibitor",
        "drug_b": "metformin",
        "note": "No major direct interaction, but both affect renal handling — relevant to monitor together in a CKD patient.",
    },
]

# Keyword aliases so simple substring matching can recognize a drug class
# from a specific brand/generic name mentioned in a clinical note. This is
# a demo convenience, not a substitute for real drug-class ontology (RxNorm).
_CLASS_ALIASES = {
    "ACE inhibitor": ["ace inhibitor", "lisinopril", "enalapril", "ramipril", "captopril"],
    "potassium-sparing diuretic": ["potassium-sparing diuretic", "spironolactone", "eplerenone", "amiloride"],
    "NSAID": ["nsaid", "ibuprofen", "naproxen", "diclofenac", "aspirin"],
    "metformin": ["metformin"],
    "iodinated contrast dye": ["contrast dye", "iodinated contrast", "contrast media"],
    "warfarin": ["warfarin"],
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
