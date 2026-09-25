# PII Redaction Tool

A Python-based Personally Identifiable Information (PII) detection and redaction system for Microsoft Word (`.docx`) documents.

The tool scans a DOCX document, detects sensitive information, and replaces detected PII with synthetic alternatives while attempting to preserve the original document structure and formatting.

The project uses a **hybrid detection approach** combining regular expressions, rule-based detection, validation logic, and optional spaCy Named Entity Recognition (NER).

---

## Features

The system detects and anonymizes the following PII categories:

| PII Type | Detection Method |
|---|---|
| Full Names | NER + rule-based detection |
| Email Addresses | Regex |
| Phone Numbers | Regex + validation |
| Company Names | NER + organization rules |
| Physical / Mailing Addresses | Pattern and context rules |
| Social Security Numbers (SSNs) | Regex |
| Credit Card Numbers | Regex + validation |
| Dates of Birth | Regex + contextual rules |
| IP Addresses | Regex + IP validation |

Instead of simply deleting sensitive information, the system replaces detected values with **synthetic alternatives**.

For example:

```text
Rashi Patil
→ John Doe

rashi.patil@gmail.com
→ john.doe@example.com

+91 9876543210
→ +91 1234567890
```

Replacement values are deterministic during a run. If the same entity appears multiple times in a document, the system reuses the same synthetic replacement.

---

# Project Structure

```text
PII_Redaction_Tool/
│
├── src/
│   ├── main.py
│   ├── document_processor.py
│   ├── pii_detector.py
│   ├── anonymizer.py
│   ├── replacement_store.py
│   ├── validators.py
│   │
│   └── detectors/
│       ├── email_detector.py
│       ├── phone_detector.py
│       ├── person_detector.py
│       ├── company_detector.py
│       ├── address_detector.py
│       ├── ssn_detector.py
│       ├── credit_card_detector.py
│       ├── dob_detector.py
│       └── ip_detector.py
│
├── evaluation/
│   ├── evaluator.py
│   ├── evaluate.py
│   ├── evaluate_synthetic.py
│   ├── generate_synthetic_docx.py
│   └── synthetic_cases.py
│
├── tests/
│   └── ...
│
├── output/
│   ├── Red_Herring_Prospectus_Redacted.docx
│   └── Synthetic_PII_Test_Dataset_100_Records_Redacted.docx
│
├── Synthetic_PII_Test_Dataset_100_Records.docx
├── Synthetic_PII_Test_Dataset_100_Records_Redacted.docx
├── Evaluation_Report.docx
├── requirements.txt
└── README.md
```

The exact location of generated files may vary depending on the output path supplied when running the program.

---

# How the System Works

The redaction pipeline follows these steps:

```text
Input DOCX
    │
    ▼
Document Extraction
    │
    ▼
Text Normalization
    │
    ▼
PII Detection
    │
    ├── Regex Detectors
    ├── Rule-Based Detectors
    ├── NER Detection
    └── Validation Rules
    │
    ▼
Entity Resolution
    │
    ▼
Synthetic Replacement Generation
    │
    ▼
DOCX Reconstruction
    │
    ▼
Redacted DOCX
```

The architecture separates detection, validation, anonymization, document processing, and evaluation so that additional PII types can be added without rewriting the entire application.

---

# Requirements

Before running the project, install:

- Python 3.10 or later
- pip
- Git (optional, required only when cloning the repository)

Check your Python installation:

```bash
python --version
```

On some systems, use:

```bash
python3 --version
```

Check pip:

```bash
pip --version
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Aayush-Crypt/PII_Redaction_Tool.git
```

Move into the project directory:

```bash
cd YOUR_REPOSITORY_NAME
```

If you downloaded the repository as a ZIP instead, extract it and open a terminal inside the extracted project directory.

---

## 2. Create a Virtual Environment

Using a virtual environment is recommended so project dependencies do not interfere with other Python installations.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can temporarily allow it for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, the terminal should normally show something similar to:

```text
(.venv)
```

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses libraries required for DOCX processing, PII detection, anonymization, and evaluation.

---

## 5. Install the spaCy English Model

If spaCy-based NER is enabled, install the English model:

```bash
python -m spacy download en_core_web_sm
```

Verify that it loads successfully:

```bash
python -c "import spacy; spacy.load('en_core_web_sm'); print('spaCy model loaded successfully')"
```

If you do not want to use spaCy, the project can also run using the rule/regex-based detection path with the `--no-spacy` option.

---

# Running the PII Redaction Tool

The main entry point is:

```text
src.main
```

General syntax:

```bash
python -m src.main INPUT_FILE OUTPUT_FILE
```

---

## Example: Redact the Red Herring Prospectus

Place the source document in the project directory, or provide its full path.

Run:

```bash
python -m src.main "Red Herring Prospectus.docx" "output/Red_Herring_Prospectus_Redacted.docx" --report "output/redaction_run.json"
```

The application will:

1. Open the DOCX.
2. Extract text from supported document elements.
3. Detect PII.
4. Generate synthetic replacement values.
5. Replace detected PII.
6. Save a new redacted DOCX.
7. Write run statistics to the JSON report.

The original file is not intended to be modified in place.

Expected output:

```text
output/Red_Herring_Prospectus_Redacted.docx
```

Run statistics:

```text
output/redaction_run.json
```

---

# Running Without spaCy

The application can run without the spaCy NER model:

```bash
python -m src.main "Red Herring Prospectus.docx" "output/Red_Herring_Prospectus_Redacted.docx" --report "output/redaction_run.json" --no-spacy
```

In this mode, detection relies primarily on regex, contextual rules, and validators.

NER-based person and organization detection may be more limited when spaCy is disabled.

---

# Running the Tool on Any DOCX

The redaction pipeline is not tied specifically to the supplied prospectus.

For another file:

```bash
python -m src.main "my_document.docx" "output/my_document_redacted.docx" --report "output/my_document_report.json"
```

For example:

```bash
python -m src.main "customer_records.docx" "output/customer_records_redacted.docx" --report "output/customer_records_run.json"
```

---

# Synthetic Evaluation Dataset

In addition to evaluating the supplied document, the project contains a synthetic evaluation dataset with **100 tabular records**.

The synthetic dataset was created to test the redaction pipeline against a larger and more varied collection of known PII values.

It contains examples of:

- Person names
- Company names
- Email addresses
- Phone numbers
- Mailing addresses
- Dates of birth
- SSNs
- Credit card numbers
- IP addresses

Because the values are synthetically generated, the expected PII is known in advance. This allows detected entities to be compared against ground truth.

The dataset is designed as an additional evaluation artifact and is not a replacement for evaluation on the supplied document.

---

# Generate the Synthetic Dataset

The 100-record dataset can be regenerated programmatically.

Run:

```bash
python evaluation/generate_synthetic_docx.py
```

This creates the synthetic DOCX dataset used by the evaluation pipeline.

---

# Redact the Synthetic Dataset

Run:

```bash
python -m src.main "Synthetic_PII_Test_Dataset_100_Records.docx" "output/Synthetic_PII_Test_Dataset_100_Records_Redacted.docx" --report "output/synthetic_redaction_run.json" --no-spacy
```

Expected output:

```text
output/Synthetic_PII_Test_Dataset_100_Records_Redacted.docx
```

The input and output documents can then be compared visually to verify that sensitive values have been replaced.

---

# Running the Evaluation

The project contains two evaluation paths.

## 1. Controlled Detector Evaluation

Run:

```bash
python evaluation/evaluate.py
```

This checks the supported detectors against labeled test cases where the expected PII is known.

It is primarily useful as a regression test to ensure that required detector functionality continues to work.

---

## 2. 100-Record Synthetic Holdout Evaluation

Run:

```bash
python evaluation/evaluate_synthetic.py
```

This evaluates the detector against the larger synthetic dataset.

The evaluator compares:

```text
Expected PII
vs.
Detected PII
```

and calculates:

- True Positives (TP)
- False Positives (FP)
- False Negatives (FN)
- Precision
- Recall
- F1 Score
- Accuracy

---

# Evaluation Metrics

## Precision

Precision measures how many detected values were actually PII.

```text
Precision = TP / (TP + FP)
```

High precision means the system avoids unnecessarily redacting non-sensitive information.

---

## Recall

Recall measures how much of the actual PII was detected.

```text
Recall = TP / (TP + FN)
```

For a redaction system, recall is particularly important because missed PII may remain visible in the output.

---

## F1 Score

F1 balances precision and recall.

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

---

## Accuracy

Accuracy provides an additional overall evaluation measure based on the labeled evaluation cases used by the project.

Because PII detection is fundamentally an entity-detection problem, precision, recall, and F1 should be considered alongside accuracy rather than relying on accuracy alone.

---

# Evaluation Strategy

Two forms of testing are used intentionally.

### Controlled tests

Controlled test cases verify that each required detector works against known examples.

They are useful for:

- regression testing,
- validating required PII categories,
- detecting code changes that break existing functionality.

A perfect result on these controlled cases should **not** be interpreted as perfect performance on arbitrary real-world documents.

### Synthetic holdout evaluation

The 100-record synthetic dataset introduces more formatting and content variation.

Since the expected entities are known, it allows false positives and false negatives to be measured directly.

This provides a more realistic estimate of detector behavior than relying only on a small collection of ideal test cases.

Detailed results and observations are provided in:

```text
Evaluation_Report.docx
```

---

# Running Tests

From the project root directory, run:

```bash
pytest
```

If pytest is not already available:

```bash
pip install pytest
pytest
```

For more detailed output:

```bash
pytest -v
```

The tests help verify detector behavior and protect against regressions when the code is modified.

---

# Output Files

After running the project, the important artifacts include:

```text
Red_Herring_Prospectus_Redacted.docx
```

Redacted version of the supplied prospectus.

```text
Synthetic_PII_Test_Dataset_100_Records.docx
```

Synthetic 100-record evaluation dataset.

```text
Synthetic_PII_Test_Dataset_100_Records_Redacted.docx
```

Redacted output generated from the synthetic dataset.

```text
Evaluation_Report.docx
```

Evaluation methodology, metrics, observations, and limitations.

```text
redaction_run.json
```

Machine-readable statistics generated during a redaction run when `--report` is supplied.

---

# Design Decisions

## Hybrid Detection

No single PII detection technique works equally well for every entity type.

Structured values such as email addresses, IP addresses, SSNs, and phone numbers are suitable for regular-expression and validation-based detection.

Names, organizations, and addresses are more context-dependent. The project therefore combines pattern matching with contextual rules and optional NER.

---

## Deterministic Pseudonymization

Detected PII is replaced rather than simply removed.

A replacement store maintains consistency during processing.

For example, if:

```text
John Smith
```

appears multiple times, the same synthetic name is reused instead of generating a different identity on every occurrence.

This preserves relationships within the document while removing the original value.

---

## Validation

Patterns that look like PII are validated where practical.

This reduces false positives from ordinary numbers, financial figures, identifiers, and other structured values that may resemble sensitive information.

---

# Extending the Project

The project is designed so additional PII categories can be introduced without rewriting the entire pipeline.

A typical extension involves:

1. Create a detector for the new entity type.
2. Define its detection rules.
3. Add any necessary validation.
4. Register the detector with the main detection pipeline.
5. Add a synthetic replacement strategy.
6. Add unit/evaluation cases.
7. Run the test and evaluation suites.

For example:

```text
src/detectors/passport_detector.py
```

could be introduced for passport-number detection.

---

# Trade-offs and Limitations

PII detection is not perfect, particularly in unstructured and heavily formatted documents.

### Names

NER and rule-based systems may miss uncommon names, initials, abbreviated names, or names fragmented across DOCX runs or table cells.

### Companies

Organization names may overlap with ordinary phrases, product names, trusts, institutions, or legal terminology, which can cause false positives or missed organizations.

### Addresses

Addresses vary substantially by country and format. Multi-line addresses and addresses split across Word table cells can be difficult to identify as one continuous entity.

### Dates

Not every date represents a date of birth. Context is required to avoid redacting ordinary corporate, financial, filing, or transaction dates.

### Numeric identifiers

Long numeric values can resemble phone numbers, account identifiers, ticket numbers, financial references, or credit-card numbers. Validation is therefore important to prevent excessive redaction.

### DOCX structure

Word documents may split visually continuous text into multiple XML runs. Tables, hyperlinks, headers, footers, text boxes, and embedded objects can also make text extraction and replacement more difficult.

### Images

PII embedded directly inside images is outside the primary text-based detection pipeline unless OCR/image processing is added separately.

---

# False Positives and False Negatives

The evaluation intentionally records both types of error.

A **false positive** occurs when normal content is incorrectly classified as PII.

Example:

```text
A long financial identifier incorrectly detected as a phone number.
```

A **false negative** occurs when actual PII is not detected.

Example:

```text
A person name with an unusual format is missed by the name detector.
```

These cases are documented because understanding failure modes is important when assessing a redaction system.

---

# Quick Start

For a new environment, the complete workflow is:

### Windows PowerShell

```powershell
git clone https://github.com/Aayush-Crypt/PII_Redaction_Tool.git
cd YOUR_REPOSITORY_NAME

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

python -m src.main "Red Herring Prospectus.docx" "output/Red_Herring_Prospectus_Redacted.docx" --report "output/redaction_run.json"

pytest

python evaluation/evaluate.py
python evaluation/evaluate_synthetic.py
```

### macOS / Linux

```bash
git clone https://github.com/Aayush-Crypt/PII_Redaction_Tool.git
cd YOUR_REPOSITORY_NAME

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

python -m src.main "Red Herring Prospectus.docx" "output/Red_Herring_Prospectus_Redacted.docx" --report "output/redaction_run.json"

pytest

python evaluation/evaluate.py
python evaluation/evaluate_synthetic.py
```

---

# Reproducing the Complete Evaluation Workflow

To reproduce the synthetic evaluation from scratch:

```bash
python evaluation/generate_synthetic_docx.py
```

Run the redaction pipeline:

```bash
python -m src.main "Synthetic_PII_Test_Dataset_100_Records.docx" "output/Synthetic_PII_Test_Dataset_100_Records_Redacted.docx" --report "output/synthetic_redaction_run.json" --no-spacy
```

Run the evaluator:

```bash
python evaluation/evaluate_synthetic.py
```

The resulting metrics can then be compared with the values documented in:

```text
Evaluation_Report.docx
```

---

# Security Considerations

The tool is intended to reduce exposure of sensitive information, but automated PII detection should not be treated as an absolute privacy guarantee.

For high-risk production environments, recommended improvements include:

- human review of redacted documents,
- stronger domain-specific NER models,
- OCR support for image-based PII,
- encrypted processing/storage,
- audit logging,
- confidence thresholds,
- configurable detection policies,
- and organization-specific validation rules.

---

# Summary

This project demonstrates an end-to-end PII redaction workflow:

```text
DOCX Input
   ↓
PII Detection
   ↓
Validation
   ↓
Deterministic Pseudonymization
   ↓
Redacted DOCX
   ↓
Ground-Truth Evaluation
   ↓
Precision / Recall / F1 / Accuracy
```

The objective is not only to detect sensitive information but also to provide a modular, testable, reproducible, and extensible redaction pipeline suitable for evaluating real-world document anonymization challenges.