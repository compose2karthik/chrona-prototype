"""SQLite persistence layer for the CHRONA Doctor Portal demo.

Stores synthetic patients/documents (seeded from seed_data.py) and caches
generated Since-Last-Visit briefs per patient, keyed by a hash of that
patient's current documents — so a brief is only regenerated via the LLM
when a new report/visit/prescription actually changes the underlying data.
"""

import hashlib
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "chrona.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    data_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    visit_date TEXT NOT NULL,
    specialty TEXT NOT NULL,
    doctor TEXT,
    facility TEXT,
    raw_text TEXT NOT NULL,
    labs_json TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    doc_hash TEXT NOT NULL,
    brief_text TEXT NOT NULL,
    combined_medications_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    generation_seconds REAL,
    UNIQUE (patient_id, doc_hash),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def is_seeded() -> bool:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) AS n FROM patients").fetchone()
    conn.close()
    return row["n"] > 0


def seed_if_empty():
    if is_seeded():
        return
    from seed_data import DOCUMENTS, PATIENTS

    conn = get_connection()
    for patient in PATIENTS:
        conn.execute(
            "INSERT INTO patients (id, data_json) VALUES (?, ?)",
            (patient["id"], json.dumps(patient)),
        )
    for doc in DOCUMENTS:
        conn.execute(
            "INSERT INTO documents (patient_id, visit_date, specialty, doctor, facility, raw_text, labs_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                doc["patient_id"],
                doc["visit_date"],
                doc["specialty"],
                doc.get("doctor"),
                doc.get("facility"),
                doc["raw_text"],
                json.dumps(doc.get("labs", [])),
            ),
        )
    conn.commit()
    conn.close()


def list_patients():
    conn = get_connection()
    rows = conn.execute("SELECT data_json FROM patients").fetchall()
    conn.close()
    return [json.loads(r["data_json"]) for r in rows]


def get_patient(patient_id: str):
    conn = get_connection()
    row = conn.execute("SELECT data_json FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return json.loads(row["data_json"]) if row else None


def get_documents(patient_id: str):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, patient_id, visit_date, specialty, doctor, facility, raw_text, labs_json "
        "FROM documents WHERE patient_id = ? ORDER BY visit_date ASC",
        (patient_id,),
    ).fetchall()
    conn.close()
    docs = []
    for r in rows:
        d = dict(r)
        d["labs"] = json.loads(d.pop("labs_json") or "[]")
        docs.append(d)
    return docs


def add_document(patient_id: str, visit_date: str, specialty: str, doctor: str, facility: str, raw_text: str, labs=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO documents (patient_id, visit_date, specialty, doctor, facility, raw_text, labs_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (patient_id, visit_date, specialty, doctor, facility, raw_text, json.dumps(labs or [])),
    )
    conn.commit()
    conn.close()


def compute_doc_hash(documents) -> str:
    parts = [f"{d['visit_date']}|{d['specialty']}|{d['raw_text']}" for d in documents]
    joined = "\n---\n".join(sorted(parts))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def get_cached_summary(patient_id: str, doc_hash: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT brief_text, combined_medications_json, generated_at, generation_seconds "
        "FROM summaries WHERE patient_id = ? AND doc_hash = ?",
        (patient_id, doc_hash),
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "brief_text": row["brief_text"],
        "combined_medications": json.loads(row["combined_medications_json"]),
        "generated_at": row["generated_at"],
        "generation_seconds": row["generation_seconds"],
    }


def save_summary(patient_id: str, doc_hash: str, brief_text: str, combined_medications, generated_at: str, generation_seconds: float):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO summaries "
        "(patient_id, doc_hash, brief_text, combined_medications_json, generated_at, generation_seconds) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (patient_id, doc_hash, brief_text, json.dumps(combined_medications), generated_at, generation_seconds),
    )
    conn.commit()
    conn.close()


def count_summaries() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) AS n FROM summaries").fetchone()
    conn.close()
    return row["n"]
