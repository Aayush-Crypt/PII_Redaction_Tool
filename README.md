# PII Redaction Tool

A production-style DOCX anonymization pipeline for the supplied Red Herring Prospectus. It detects required PII using deterministic regex/validation rules plus optional spaCy NER for PERSON/ORG entities, then replaces matches with stable synthetic alternatives so repeated source values receive the same pseudonym. The pipeline processes paragraphs, tables, headers and footers and writes a redacted DOCX while retaining the document structure.

## Supported PII
Full names, email addresses, phone numbers, company names, physical/mailing addresses, US SSNs, credit-card numbers (Luhn validated), dates of birth when DOB context is present, and IPv4 addresses.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm   # recommended, optional
python -m src.main input.docx output/Red_Herring_Prospectus_Redacted.docx --report output/redaction_run.json
```
For an offline regex/context-only run, add `--no-spacy`.

## Approach and trade-offs
Regex is used for structured identifiers because it is predictable and easy to test. Context rules and optional spaCy NER cover names and organizations, where regex alone is weaker. Credit-card candidates are validated with the Luhn checksum to reduce false positives. DOB detection intentionally requires explicit DOB/birth context so ordinary prospectus dates are not destroyed. The main trade-off is that NER/context heuristics can miss unusual names/addresses or occasionally classify capitalized business text as an entity; scanned text embedded only in images is outside the text-layer pipeline.

## Evaluation
Two evaluation views are included. `evaluation/evaluate.py` is the controlled baseline benchmark covering all required PII types plus negative Order/Ticket examples. `evaluation/evaluate_synthetic.py` evaluates a separate, deliberately challenging synthetic holdout dataset in `evaluation/synthetic_cases.py`; a readable DOCX copy is provided as `evaluation/Synthetic_PII_Test_Dataset_100_Records.docx`.

The controlled benchmark currently produces 100% exact-match precision/recall/F1 and is retained as a regression/coverage test. The harder synthetic holdout produces lower, more realistic exact-match metrics (92.54% precision, 89.56% recall, 91.02% F1, 91.45% case accuracy), exposing limitations in person names, address boundaries, company suffix variants, phone/long-number ambiguity, and date boundaries.

For the supplied prospectus, `output/redaction_run.json` reports the full-document detection counts. Because the 127-page document was not exhaustively human-annotated, those counts are operational run statistics rather than ground-truth precision/recall claims.

## Extend
Add a detector or validation rule in `src/pii_detector.py`, assign a replacement strategy in `src/anonymizer.py`, and add positive/negative cases to the evaluation and tests. This keeps detection, anonymization, DOCX I/O and evaluation concerns separated.
