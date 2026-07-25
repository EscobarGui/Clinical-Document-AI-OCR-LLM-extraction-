# Clinical Document AI — OCR + LLM extraction

Reads clinical prescriptions and exam requests, extracts the relevant fields,
and maps each item to standardized medical codes (TUSS), with a human-in-the-loop
review step. Built to replace manual reading/typing of documents one at a time.

## Results
- Processing time cut from ~20 min to ~4 min per document (−80%)
- YOLOv8 field/checkbox detector at ~86% mAP@50
- Human-in-the-loop validation for accuracy

## Stack
Python · YOLOv8 (computer vision) · OCR · LLM prompt engineering · rule-based normalization

## How it works
1. Upload a document (PDF/image)
2. OCR + detection extract fields and checkboxes
3. Items are classified and normalized to TUSS codes
4. A reviewer confirms/edits before export (Excel/CSV/JSON)

## Run locally
```(bash)
pip install -r requirements.txt
python main.py --input ./samples
pip install --no-cache-dir Pillow
pip install -r requirements.txt
```
> Note: sample data only — no real patient data is included in this repository.
