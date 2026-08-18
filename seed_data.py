"""Synthetic seed data for the CHRONA Doctor Portal demo.

Every patient, document, lab value, and medication below is fabricated for
demonstration purposes only. No real patient data is used anywhere here.
"""

DOCTORS = {
    "doctor1": {"password": "123", "name": "Dr. Arjun Mehta", "specialty": "Cardiology", "initials": "AM"},
    "doctor2": {"password": "123", "name": "Dr. Kavita Rao", "specialty": "Endocrinology", "initials": "KR"},
    "doctor3": {"password": "123", "name": "Dr. Pradeep Singh", "specialty": "Nephrology", "initials": "PS"},
}

# ---------------------------------------------------------------------------
# Patients: display metadata, vitals, structured medications, care team
# ---------------------------------------------------------------------------

PATIENTS = [
    {
        "id": "priya",
        "name": "Mrs. Priya Sharma",
        "initials": "PS",
        "age": 58,
        "gender": "Female",
        "dob": "14 Mar 1968",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0042",
        "color": "#ec4899,#8b5cf6",
        "meta_short": "58F · Type 2 DM, CKD St.3, HTN",
        "badge": "Follow-up",
        "conditions_tags": ["🩺 Type 2 Diabetes Mellitus", "🫘 CKD Stage 3", "❤️ Hypertension", "⚠️ Polypharmacy Risk"],
        "vitals": [
            ("BP", "138/84", "mmHg", "warn", "↓ improving"),
            ("HR", "78", "bpm", "ok", None),
            ("eGFR", "38", "ml/min", "alert", "↓ was 42"),
            ("HbA1c", "8.1", "%", "alert", "↑ was 7.2%"),
            ("Weight", "71", "kg", "ok", None),
            ("SpO2", "97", "%", "ok", None),
        ],
        "active_conditions": [
            ("Type 2 Diabetes Mellitus", "warn", "Active"),
            ("Chronic Kidney Disease Stage 3", "alert", "Progressing"),
            ("Essential Hypertension", "warn", "Controlled"),
            ("Dyslipidaemia", "ok", "Stable"),
            ("Anaemia of CKD", "warn", "Monitoring"),
        ],
        "latest_labs": [
            ("Serum Creatinine", "1.82 mg/dL ↑", "alert"),
            ("eGFR (CKD-EPI)", "38 ml/min/1.73m² ↓", "alert"),
            ("HbA1c", "8.1% ↑", "alert"),
            ("Serum Potassium", "5.1 mEq/L (high)", "warn"),
            ("LDL Cholesterol", "88 mg/dL", "ok"),
            ("Haemoglobin", "10.2 g/dL", "warn"),
        ],
        "medications": [
            {"name": "Metformin", "dose": "500 mg BD", "since": "Jan 2024", "prescriber": "Dr. Kavita Rao", "specialty": "Endocrinology", "new": False},
            {"name": "Glimepiride", "dose": "2 mg OD (morning)", "since": "Jul 2026", "prescriber": "Dr. Kavita Rao", "specialty": "Endocrinology", "new": True},
            {"name": "Insulin Glargine", "dose": "10 U HS", "since": "Mar 2025", "prescriber": "Dr. Kavita Rao", "specialty": "Endocrinology", "new": False},
            {"name": "Losartan", "dose": "50 mg OD", "since": "Aug 2025", "prescriber": "Dr. Pradeep Singh", "specialty": "Nephrology", "new": False},
            {"name": "Furosemide", "dose": "40 mg OD", "since": "Sep 2025", "prescriber": "Dr. Pradeep Singh", "specialty": "Nephrology", "new": False},
            {"name": "Atorvastatin", "dose": "40 mg OD (night)", "since": "Feb 2024", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Aspirin", "dose": "75 mg OD", "since": "Feb 2024", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Bisoprolol", "dose": "5 mg OD", "since": "Feb 2024", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Endocrinologist", "Dr. Kavita Rao · Diabetes Care Centre, Pune"),
            ("Nephrologist", "Dr. Pradeep Singh · Kidney Institute, Pune"),
            ("Last visit (any)", "12 Aug 2026 · Nephrology"),
            ("Next scheduled", "25 Sep 2026 · Endocrinology"),
        ],
    },
    {
        "id": "ramesh",
        "name": "Mr. Ramesh Kumar",
        "initials": "RK",
        "age": 64,
        "gender": "Male",
        "dob": "02 Nov 1961",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0043",
        "color": "#3b82f6,#06b6d4",
        "meta_short": "64M · Hypertension, CAD",
        "badge": "First Visit",
        "conditions_tags": ["❤️ Coronary Artery Disease", "🩸 Hypertension"],
        "vitals": [
            ("BP", "148/92", "mmHg", "alert", None),
            ("HR", "82", "bpm", "ok", None),
            ("LDL", "162", "mg/dL", "alert", None),
            ("Weight", "84", "kg", "ok", None),
        ],
        "active_conditions": [
            ("Coronary Artery Disease", "alert", "New diagnosis"),
            ("Essential Hypertension", "warn", "Uncontrolled"),
        ],
        "latest_labs": [
            ("LDL Cholesterol", "162 mg/dL ↑", "alert"),
            ("Troponin I", "Negative", "ok"),
            ("Fasting Glucose", "104 mg/dL", "ok"),
        ],
        "medications": [
            {"name": "Amlodipine", "dose": "5 mg OD", "since": "Jul 2026", "prescriber": "Referring physician", "specialty": "General Medicine", "new": False},
            {"name": "Atorvastatin", "dose": "40 mg OD (night)", "since": "Aug 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": True},
            {"name": "Aspirin", "dose": "75 mg OD", "since": "Aug 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": True},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology (first visit)"),
            ("Next scheduled", "18 Sep 2026 · Cardiology"),
        ],
    },
    {
        "id": "sunita",
        "name": "Mrs. Sunita Nair",
        "initials": "SN",
        "age": 52,
        "gender": "Female",
        "dob": "22 Jan 1974",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0044",
        "color": "#10b981,#3b82f6",
        "meta_short": "52F · Heart Failure (EF 40%)",
        "badge": "Follow-up",
        "conditions_tags": ["❤️ Heart Failure (EF 40%)", "🩺 Type 2 Diabetes Mellitus"],
        "vitals": [
            ("BP", "112/70", "mmHg", "ok", None),
            ("HR", "88", "bpm", "warn", "↑ was 74"),
            ("EF", "40", "%", "warn", None),
            ("Weight", "68", "kg", "warn", "↑ 2kg in 2 weeks"),
        ],
        "active_conditions": [
            ("Heart Failure with reduced EF", "warn", "Stable, monitor weight"),
            ("Type 2 Diabetes Mellitus", "ok", "Controlled"),
        ],
        "latest_labs": [
            ("NT-proBNP", "890 pg/mL ↑", "warn"),
            ("Serum Sodium", "134 mEq/L", "warn"),
            ("HbA1c", "6.8%", "ok"),
        ],
        "medications": [
            {"name": "Sacubitril-Valsartan", "dose": "50 mg BD", "since": "Mar 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Furosemide", "dose": "20 mg OD", "since": "Mar 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Ibuprofen", "dose": "400 mg PRN", "since": "Aug 2026", "prescriber": "Orthopedic (outside)", "specialty": "Orthopedics", "new": True},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology"),
            ("Next scheduled", "18 Sep 2026 · Cardiology"),
        ],
    },
    {
        "id": "anand",
        "name": "Mr. Anand Venkatesan",
        "initials": "AV",
        "age": 71,
        "gender": "Male",
        "dob": "09 Apr 1955",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0045",
        "color": "#f59e0b,#ef4444",
        "meta_short": "71M · Post-MI, Diabetes",
        "badge": "DDI Alert",
        "conditions_tags": ["❤️ Post-Myocardial Infarction", "🩺 Type 2 Diabetes Mellitus", "🩸 Atrial Fibrillation"],
        "vitals": [
            ("BP", "126/78", "mmHg", "ok", None),
            ("HR", "68", "bpm", "ok", None),
            ("INR", "2.1", "", "warn", None),
        ],
        "active_conditions": [
            ("Post-MI (Feb 2026)", "warn", "Stable"),
            ("Atrial Fibrillation", "warn", "Rate-controlled"),
            ("Type 2 Diabetes Mellitus", "ok", "Controlled"),
        ],
        "latest_labs": [
            ("INR", "2.1 (therapeutic)", "warn"),
            ("Haemoglobin", "12.8 g/dL", "ok"),
            ("HbA1c", "7.0%", "ok"),
        ],
        "medications": [
            {"name": "Warfarin", "dose": "5 mg OD", "since": "Feb 2026", "prescriber": "Haematology (outside)", "specialty": "Haematology", "new": False},
            {"name": "Aspirin", "dose": "75 mg OD", "since": "Feb 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Metformin", "dose": "500 mg BD", "since": "2020", "prescriber": "Diabetologist (outside)", "specialty": "Endocrinology", "new": False},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology"),
            ("Next scheduled", "18 Sep 2026 · Cardiology"),
        ],
    },
    {
        "id": "meera",
        "name": "Ms. Meera Thakkar",
        "initials": "MT",
        "age": 45,
        "gender": "Female",
        "dob": "30 Jun 1981",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0046",
        "color": "#8b5cf6,#ec4899",
        "meta_short": "45F · Arrhythmia, Hypothyroidism",
        "badge": "Review",
        "conditions_tags": ["💓 Arrhythmia", "🦋 Hypothyroidism"],
        "vitals": [
            ("BP", "118/76", "mmHg", "ok", None),
            ("HR", "62", "bpm", "ok", None),
            ("TSH", "4.2", "mU/L", "warn", "↑ was 2.1"),
        ],
        "active_conditions": [
            ("Paroxysmal Atrial Fibrillation", "warn", "Rate-controlled"),
            ("Hypothyroidism", "warn", "Newly borderline"),
        ],
        "latest_labs": [
            ("TSH", "4.2 mU/L ↑", "warn"),
            ("Free T4", "1.0 ng/dL", "ok"),
        ],
        "medications": [
            {"name": "Amiodarone", "dose": "200 mg OD", "since": "May 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Levothyroxine", "dose": "50 mcg OD", "since": "Jul 2026", "prescriber": "Endocrinologist (outside)", "specialty": "Endocrinology", "new": True},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology"),
            ("Next scheduled", "15 Sep 2026 · Cardiology"),
        ],
    },
    {
        "id": "gopal",
        "name": "Mr. Gopal Joshi",
        "initials": "GJ",
        "age": 55,
        "gender": "Male",
        "dob": "17 Dec 1970",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0047",
        "color": "#06b6d4,#10b981",
        "meta_short": "55M · Valvular HD",
        "badge": "First Visit",
        "conditions_tags": ["💓 Valvular Heart Disease"],
        "vitals": [
            ("BP", "124/80", "mmHg", "ok", None),
            ("HR", "74", "bpm", "ok", None),
        ],
        "active_conditions": [
            ("Mitral Regurgitation (moderate)", "warn", "New diagnosis"),
        ],
        "latest_labs": [
            ("Echo EF", "58%", "ok"),
        ],
        "medications": [
            {"name": "Bisoprolol", "dose": "2.5 mg OD", "since": "Aug 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": True},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology (first visit)"),
            ("Next scheduled", "18 Nov 2026 · Cardiology"),
        ],
    },
    {
        "id": "lakshmi",
        "name": "Mrs. Lakshmi Venkat",
        "initials": "LV",
        "age": 60,
        "gender": "Female",
        "dob": "05 Sep 1965",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0048",
        "color": "#f472b6,#a78bfa",
        "meta_short": "60F · Atrial Fibrillation",
        "badge": "Follow-up",
        "conditions_tags": ["💓 Atrial Fibrillation", "🩸 Hypertension"],
        "vitals": [
            ("BP", "132/82", "mmHg", "warn", None),
            ("HR", "90", "bpm", "warn", "↑ was 76"),
        ],
        "active_conditions": [
            ("Atrial Fibrillation", "warn", "Rate control suboptimal"),
            ("Essential Hypertension", "warn", "Controlled"),
        ],
        "latest_labs": [
            ("TSH", "2.0 mU/L", "ok"),
        ],
        "medications": [
            {"name": "Diltiazem", "dose": "120 mg OD", "since": "Jan 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Losartan", "dose": "50 mg OD", "since": "Jan 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology"),
            ("Next scheduled", "18 Sep 2026 · Cardiology"),
        ],
    },
    {
        "id": "suresh",
        "name": "Mr. Suresh Rajan",
        "initials": "SR",
        "age": 67,
        "gender": "Male",
        "dob": "11 Feb 1959",
        "location": "Pune, Maharashtra",
        "chr_id": "CHR-2026-0049",
        "color": "#fb923c,#f43f5e",
        "meta_short": "67M · Hypertensive CKD",
        "badge": "Follow-up",
        "conditions_tags": ["🫘 CKD Stage 3", "🩸 Hypertension"],
        "vitals": [
            ("BP", "144/88", "mmHg", "warn", None),
            ("eGFR", "44", "ml/min", "warn", "↓ was 48"),
        ],
        "active_conditions": [
            ("Chronic Kidney Disease Stage 3", "warn", "Slowly progressing"),
            ("Essential Hypertension", "warn", "Uncontrolled"),
        ],
        "latest_labs": [
            ("eGFR", "44 ml/min/1.73m² ↓", "warn"),
            ("Serum Potassium", "4.8 mEq/L", "ok"),
        ],
        "medications": [
            {"name": "Enalapril", "dose": "10 mg OD", "since": "Feb 2026", "prescriber": "Dr. Arjun Mehta", "specialty": "Cardiology", "new": False},
            {"name": "Ibuprofen", "dose": "400 mg PRN", "since": "Aug 2026", "prescriber": "Self-medicated (patient report)", "specialty": "N/A", "new": True},
        ],
        "care_team": [
            ("Cardiologist", "Dr. Arjun Mehta · Apollo Clinic, Pune"),
            ("Last visit (any)", "18 Aug 2026 · Cardiology"),
            ("Next scheduled", "18 Sep 2026 · Cardiology"),
        ],
    },
]

# ---------------------------------------------------------------------------
# Documents: raw synthetic visit notes used as LLM source material for the
# extraction + Since-Last-Visit delta-brief prompts. Each entry also carries
# a short "labs" list used for the Timeline tab display.
# ---------------------------------------------------------------------------

DOCUMENTS = [
    # ---- Priya Sharma (flagship, 4 visits) ----
    {
        "patient_id": "priya", "visit_date": "2026-02-01", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["LDL 142", "BP 152/96"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — First Consultation Note
Patient: Mrs. Priya Sharma, Female, 58 years
Visit Date: 2026-02-01
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Referred by nephrology for cardiovascular risk assessment in the context of
Type 2 Diabetes Mellitus and Chronic Kidney Disease Stage 3.

Examination: Blood pressure 152/96 mmHg. Heart rate 80 bpm, regular. ECG
normal sinus rhythm.

Labs: LDL Cholesterol 142 mg/dL (elevated).

Assessment: Dyslipidaemia with elevated cardiovascular risk given diabetes
and CKD.

Plan: Starting Atorvastatin 40 mg once daily (night) and Aspirin 75 mg once
daily for cardiovascular risk reduction. Bisoprolol 5 mg once daily added
for rate control. Follow up in 4 months.
""",
    },
    {
        "patient_id": "priya", "visit_date": "2026-06-14", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["BP 145/90", "ECG Normal", "HbA1c 7.2%"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mrs. Priya Sharma, Female, 58 years
Visit Date: 2026-06-14
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Routine follow-up. Patient reports no chest pain or palpitations.

Examination: Blood pressure 145/90 mmHg, improved from 152/96 at prior
visit. ECG normal sinus rhythm.

Labs reviewed: HbA1c 7.2% (from endocrinology, stable).

Current Medications: Atorvastatin 40 mg OD, Aspirin 75 mg OD, Bisoprolol 5
mg OD (all continued, unchanged).

Assessment: Blood pressure trending down. Cardiovascular status stable.

Plan: Continue current regimen. Follow up in 3 months or sooner if
referred by other specialists.
""",
    },
    {
        "patient_id": "priya", "visit_date": "2026-07-25", "specialty": "Endocrinology",
        "doctor": "Dr. Kavita Rao", "facility": "Diabetes Care Centre, Pune",
        "labs": ["HbA1c 8.1%", "Glimepiride ADDED"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Endocrinology Clinic — Consultation Note
Patient: Mrs. Priya Sharma, Female, 58 years
Visit Date: 2026-07-25
Specialty: Endocrinology
Physician: Dr. Kavita Rao

Chief Complaint: Routine follow-up for Type 2 Diabetes Mellitus.

Labs Reviewed: HbA1c 8.1%, above target (prior reading 7.2% in June 2026).
Fasting blood sugar 156 mg/dL.

Current Medications: Metformin 500 mg BD (existing, continued), Insulin
Glargine 10 U at bedtime (existing, continued).

Assessment: Glycemic control has worsened since last review.

Plan: Adding Glimepiride 2 mg once daily (morning) to the regimen given
HbA1c above target. Counselled on diet and exercise. Recheck HbA1c in 6-8
weeks. Continue Metformin and Insulin Glargine at current doses.
""",
    },
    {
        "patient_id": "priya", "visit_date": "2026-08-12", "specialty": "Nephrology",
        "doctor": "Dr. Pradeep Singh", "facility": "Kidney Institute, Pune",
        "labs": ["eGFR 38 ↓", "K+ 5.1 ↑", "Creatinine 1.82 ↑"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Nephrology Clinic — Consultation Note
Patient: Mrs. Priya Sharma, Female, 58 years
Visit Date: 2026-08-12
Specialty: Nephrology
Physician: Dr. Pradeep Singh

Chief Complaint: Routine follow-up for Chronic Kidney Disease Stage 3.

Labs Reviewed: Estimated glomerular filtration rate (eGFR) is now 38
mL/min/1.73m2, down from 42 mL/min/1.73m2 recorded in May 2026. Serum
creatinine 1.82 mg/dL, up from 1.64 mg/dL. Serum potassium 5.1 mEq/L
(borderline high, up from 4.6 mEq/L in June).

Current Medications (confirmed continued): Losartan 50 mg once daily,
Furosemide 40 mg once daily. Patient confirms she is also taking Metformin
500 mg BD per endocrinology and was recently started on Glimepiride by
endocrinology.

Assessment: Interval decline in eGFR, now consistent with CKD Stage 3b.
Serum potassium trending upward, likely related to Losartan in the
context of declining renal function.

Plan: Continue Losartan at current dose for now; will reassess at next
visit. Advised low-sodium, low-potassium diet. Repeat renal panel in 4-6
weeks. Recommend renal function and potassium monitoring given the
patient's combined medication list across specialists, particularly given
Metformin use at this eGFR level.
""",
    },

    # ---- Ramesh Kumar (first visit, referral note + cardiology visit) ----
    {
        "patient_id": "ramesh", "visit_date": "2026-08-01", "specialty": "General Medicine",
        "doctor": "Dr. S. Iyer", "facility": "Referring Clinic, Pune",
        "labs": ["BP 150/94", "LDL 158"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
General Medicine — Referral Note
Patient: Mr. Ramesh Kumar, Male, 64 years
Visit Date: 2026-08-01
Specialty: General Medicine
Physician: Dr. S. Iyer

Patient presents with uncontrolled hypertension and new-onset exertional
chest discomfort. Blood pressure 150/94 mmHg. LDL cholesterol 158 mg/dL.

Started Amlodipine 5 mg once daily for blood pressure control.

Referred to cardiology for further evaluation of chest discomfort and
cardiovascular risk assessment.
""",
    },
    {
        "patient_id": "ramesh", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["LDL 162 ↑", "Troponin negative", "BP 148/92"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — First Consultation Note
Patient: Mr. Ramesh Kumar, Male, 64 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Exertional chest discomfort, referred from general
medicine. Known coronary artery disease risk factors.

Examination: Blood pressure 148/92 mmHg. Heart rate 82 bpm. Troponin I
negative. LDL cholesterol 162 mg/dL (elevated).

Current Medications: Amlodipine 5 mg once daily (existing, started by
referring physician).

Assessment: Coronary artery disease risk, blood pressure still elevated
despite Amlodipine.

Plan: Starting Atorvastatin 40 mg once daily (night) and Aspirin 75 mg
once daily. Advised stress test. Follow up in 4 weeks.
""",
    },

    # ---- Sunita Nair (heart failure, follow-up) ----
    {
        "patient_id": "sunita", "visit_date": "2026-06-20", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["EF 40%", "NT-proBNP 520", "Weight 66kg"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mrs. Sunita Nair, Female, 52 years
Visit Date: 2026-06-20
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Routine follow-up, Heart Failure with reduced ejection
fraction (EF 40%).

Examination: Weight 66 kg. Blood pressure 110/72 mmHg. Heart rate 74 bpm.
No peripheral edema.

Labs: NT-proBNP 520 pg/mL (stable).

Current Medications: Sacubitril-Valsartan 50 mg BD, Furosemide 20 mg OD
(both continued, unchanged).

Assessment: Heart failure stable on current regimen.

Plan: Continue current medications. Weigh daily at home, report weight
gain over 2kg. Follow up in 2 months.
""",
    },
    {
        "patient_id": "sunita", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["NT-proBNP 890 ↑", "Weight 68kg ↑", "HR 88 ↑"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mrs. Sunita Nair, Female, 52 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Follow-up, Heart Failure with reduced ejection fraction.
Patient reports mild weight gain over the past two weeks.

Examination: Weight 68 kg, up 2 kg since June visit. Blood pressure 112/70
mmHg. Heart rate 88 bpm, up from 74 bpm. Trace bilateral ankle edema
noted.

Labs: NT-proBNP 890 pg/mL, up from 520 pg/mL in June. Serum sodium 134
mEq/L (mildly low).

Current Medications: Sacubitril-Valsartan 50 mg BD, Furosemide 20 mg OD
(both continued). Patient reports she has been taking over-the-counter
Ibuprofen 400 mg as needed for knee pain since early August, prescribed by
an outside orthopedic clinic.

Assessment: Mild interval weight gain and rising NT-proBNP, possibly early
decompensation. Recent NSAID use noted.

Plan: Advised to stop Ibuprofen and discuss alternative pain management.
Continue current heart failure regimen. Weigh daily, follow up in 2 weeks
or sooner if symptoms worsen.
""",
    },

    # ---- Anand Venkatesan (post-MI, DDI alert) ----
    {
        "patient_id": "anand", "visit_date": "2026-02-10", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["Troponin elevated", "ECG STEMI changes"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Post-MI Discharge Note
Patient: Mr. Anand Venkatesan, Male, 71 years
Visit Date: 2026-02-10
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Patient admitted with acute myocardial infarction, managed with PCI.
Discharged on Aspirin 75 mg once daily and Bisoprolol.

New diagnosis of atrial fibrillation noted during admission; started on
Warfarin 5 mg once daily by the haematology consult team for
anticoagulation, target INR 2-3.

Existing medication: Metformin 500 mg BD for Type 2 Diabetes Mellitus
(long-standing, prescribed by outside diabetologist).

Plan: Follow up in cardiology clinic in 6 months. INR monitoring per
haematology.
""",
    },
    {
        "patient_id": "anand", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["INR 2.1", "Hb 12.8", "HbA1c 7.0%"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mr. Anand Venkatesan, Male, 71 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Routine follow-up, post-MI and atrial fibrillation on
anticoagulation.

Examination: Blood pressure 126/78 mmHg. Heart rate 68 bpm, regular.

Labs: INR 2.1 (within therapeutic range). Haemoglobin 12.8 g/dL, no
evidence of bleeding. HbA1c 7.0%, well controlled.

Current Medications confirmed: Warfarin 5 mg OD (haematology), Aspirin 75
mg OD (this clinic), Metformin 500 mg BD (outside diabetologist) — all
continued unchanged since last visit.

Assessment: Stable on current regimen. Combined Warfarin and Aspirin use
noted for continued monitoring given bleeding risk.

Plan: Continue current medications. Repeat INR in 4 weeks. Follow up in 3
months.
""",
    },

    # ---- Meera Thakkar (arrhythmia + hypothyroidism, DDI review) ----
    {
        "patient_id": "meera", "visit_date": "2026-05-15", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["TSH 2.1", "ECG PAF"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Consultation Note
Patient: Ms. Meera Thakkar, Female, 45 years
Visit Date: 2026-05-15
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Palpitations, diagnosed with paroxysmal atrial
fibrillation.

Labs: TSH 2.1 mU/L (normal at this time).

Plan: Starting Amiodarone 200 mg once daily for rhythm control. Baseline
thyroid function normal. Follow up in 3 months, will recheck thyroid
function given known amiodarone effect on thyroid.
""",
    },
    {
        "patient_id": "meera", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["TSH 4.2 ↑", "Free T4 1.0"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Ms. Meera Thakkar, Female, 45 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Follow-up, atrial fibrillation on Amiodarone.

Labs: TSH 4.2 mU/L, up from 2.1 mU/L in May (upper-normal/borderline).
Free T4 1.0 ng/dL.

Current Medications: Amiodarone 200 mg OD (continued, this clinic).
Patient reports an outside endocrinologist started Levothyroxine 50 mcg
once daily in July 2026 after an outside thyroid panel.

Assessment: Rising TSH trend since starting Amiodarone, now on
Levothyroxine per outside endocrinologist. Rhythm well controlled,
patient asymptomatic.

Plan: Continue Amiodarone. Recheck thyroid function in 6 weeks to assess
Levothyroxine dose adequacy given Amiodarone's known thyroid effects.
""",
    },

    # ---- Gopal Joshi (first visit, valvular disease) ----
    {
        "patient_id": "gopal", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["Echo EF 58%", "Murmur grade 2/6"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — First Consultation Note
Patient: Mr. Gopal Joshi, Male, 55 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Incidental murmur detected on routine physical.

Examination: Grade 2/6 systolic murmur at the apex. Echocardiogram shows
moderate mitral regurgitation, ejection fraction 58% (preserved).

Assessment: New diagnosis of moderate mitral regurgitation.

Plan: Starting Bisoprolol 2.5 mg once daily for symptom management.
Advised routine dental prophylaxis precautions. Repeat echocardiogram in 6
months to monitor progression.
""",
    },

    # ---- Lakshmi Venkat (atrial fibrillation, follow-up) ----
    {
        "patient_id": "lakshmi", "visit_date": "2026-06-01", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["BP 128/80", "HR 76"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mrs. Lakshmi Venkat, Female, 60 years
Visit Date: 2026-06-01
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Routine follow-up, atrial fibrillation and hypertension.

Examination: Blood pressure 128/80 mmHg. Heart rate 76 bpm, controlled.

Current Medications: Diltiazem 120 mg OD, Losartan 50 mg OD (both
continued, unchanged).

Assessment: Rate and blood pressure well controlled.

Plan: Continue current regimen. Follow up in 2-3 months.
""",
    },
    {
        "patient_id": "lakshmi", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["BP 132/82 ↑", "HR 90 ↑"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mrs. Lakshmi Venkat, Female, 60 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Follow-up, atrial fibrillation and hypertension. Patient
reports occasional palpitations over the past month.

Examination: Blood pressure 132/82 mmHg. Heart rate 90 bpm, up from 76 bpm
at last visit — rate control appears suboptimal.

Current Medications: Diltiazem 120 mg OD, Losartan 50 mg OD (both
continued, unchanged since June).

Assessment: Rate control less optimal than at last visit; palpitations
reported.

Plan: Consider Diltiazem dose adjustment at next review. Ambulatory ECG
monitoring advised. Follow up in 4 weeks.
""",
    },

    # ---- Suresh Rajan (hypertensive CKD, follow-up) ----
    {
        "patient_id": "suresh", "visit_date": "2026-05-20", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["eGFR 48", "K+ 4.5"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mr. Suresh Rajan, Male, 67 years
Visit Date: 2026-05-20
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Routine follow-up, hypertension with Chronic Kidney
Disease Stage 3.

Labs: eGFR 48 mL/min/1.73m2. Serum potassium 4.5 mEq/L (normal).

Current Medications: Enalapril 10 mg OD (continued, unchanged).

Assessment: Blood pressure and renal function stable.

Plan: Continue current regimen. Follow up in 3 months.
""",
    },
    {
        "patient_id": "suresh", "visit_date": "2026-08-18", "specialty": "Cardiology",
        "doctor": "Dr. Arjun Mehta", "facility": "Apollo Clinic, Pune",
        "labs": ["eGFR 44 ↓", "K+ 4.8", "BP 144/88 ↑"],
        "raw_text": """SYNTHETIC DEMO DATA — FICTIONAL PATIENT
Cardiology Clinic — Follow-up Consultation Note
Patient: Mr. Suresh Rajan, Male, 67 years
Visit Date: 2026-08-18
Specialty: Cardiology
Physician: Dr. Arjun Mehta

Chief Complaint: Follow-up, hypertension with Chronic Kidney Disease Stage
3.

Examination: Blood pressure 144/88 mmHg, up from prior visits — poorly
controlled today.

Labs: eGFR 44 mL/min/1.73m2, down from 48 in May. Serum potassium 4.8
mEq/L (upper-normal).

Current Medications: Enalapril 10 mg OD (continued). Patient reports
self-medicating with over-the-counter Ibuprofen 400 mg as needed for
recent joint pain since early August, not previously discussed with this
clinic.

Assessment: Blood pressure control worse and mild interval eGFR decline;
recent NSAID use noted, which may be contributing to both.

Plan: Advised to stop over-the-counter Ibuprofen and use paracetamol
instead for pain. Recheck renal function and blood pressure in 4 weeks.
""",
    },
]
