# hw5-Manny_Sotero — lab-report-analyzer

## Video Walkthrough
[Insert video link here]

---

## What the skill does

`lab-report-analyzer` is a reusable skill for health coaches that:

1. Accepts a patient lab results PDF (e.g. Labcorp)
2. Compares each biomarker against the health coach's own optimal reference ranges stored in an Excel file
3. Produces a color-coded PDF report organized by lab panel, showing each biomarker's result, optimal range, status, and relevant findings

**Status color coding:**
- 🟢 **In Range** — within the coach's optimal range
- 🟡 **Slightly Off** — outside optimal range but within the lab's standard reference interval
- 🔴 **Out of Range** — outside both ranges

---

## Why I chose this skill

A health coach currently does this manually: she receives a patient PDF, opens a blank Excel sheet, transcribes each biomarker, looks up her reference sheet, and writes whether each value is in or out of range. It is tedious, error-prone, and takes significant time per patient.

This is exactly the kind of task where **a script is genuinely load-bearing**:

- A model cannot reliably parse structured tables from a PDF
- A model cannot be trusted to do precise numeric comparisons at scale without errors
- A model cannot generate a consistently formatted, color-coded PDF report

Prose alone cannot do this job. The script handles all the deterministic work. The model contributes where ambiguity exists — fuzzy matching biomarker names between the PDF and the reference sheet (e.g. "ALT (SGPT)" → "ALT", "C-Reactive Protein, Quant" → "CRP").

---

## How to use it

### Install dependencies
```bash
pip install pdfplumber openpyxl reportlab
```

### Prepare inputs
1. Place your lab results PDF in the project folder
2. Ensure `references/Optimal Lab Ranges.xlsx` is in the skill's references folder (already included)
3. Create a `mapping.json` file — the model generates this by fuzzy-matching biomarker names between the PDF and the reference Excel

### mapping.json format
```json
{
  "Glucose": "GLUCOSE",
  "AST (SGOT)": "AST",
  "DHEA-Sulfate": "DHEA- S",
  "C-Reactive Protein, Quant": "CRP"
}
```

### Run the script
```bash
python scripts/analyze_labs.py <lab_pdf> <mapping_json> <output_pdf>
```

**Example:**
```bash
python scripts/analyze_labs.py patient_labs.pdf mapping.json report.pdf
```

### Invoke via agent
In Claude Code or another coding assistant, simply say:

> "Analyze my labs" — with a lab PDF uploaded

The agent will activate the skill, perform fuzzy name matching, generate the mapping, and call the script to produce the final report.

---

## What the script does

`scripts/analyze_labs.py` handles all deterministic work:

| Step | What the script does | Why code and not prose |
|------|----------------------|------------------------|
| 1 | Parses the lab PDF page by page, detects panel headers, extracts biomarker names and values | Reliable structured extraction — a model would hallucinate or miss values |
| 2 | Loads the reference Excel and parses optimal ranges, HIGH findings, and LOW findings | Deterministic file parsing — Excel has verbose, inconsistent names that need cleaning |
| 3 | Receives the model's fuzzy name mapping as a JSON file | The model handles ambiguity; the script handles precision |
| 4 | Compares each value against optimal range and lab reference interval | Numeric comparison must be exact — prose cannot be trusted here |
| 5 | Generates a color-coded PDF report organized by lab panel | Consistent formatting requires code, not a language model |

---

## What worked well

- **Panel organization** — the output PDF mirrors the structure of the original lab report, making it easy for the health coach to cross-reference
- **Color coding** — Green / Orange / Red gives an immediate visual summary without reading every row
- **Findings column** — the script automatically selects the HIGH or LOW findings text from the reference sheet based on which direction the value deviates
- **Unmatched biomarkers** — any biomarker the model couldn't confidently match is listed in a dedicated section rather than silently dropped
- **Progressive disclosure** — the SKILL.md is concise at the top level; the script carries all the deterministic complexity separately

---

## Limitations

- **OCR not implemented** — Labcorp PDFs generated from their web app store content as vector paths, not text. The current script requires a PDF with extractable text. A production version would add Tesseract OCR as a fallback.
- **Fuzzy matching is model-dependent** — the model generates the biomarker name mapping. If the model makes a wrong match, the report will compare against the wrong reference range. The unmatched section helps catch this but does not prevent it.
- **Units are not converted** — the script assumes units match between the PDF and the reference sheet. Discrepancies (e.g. mg/dL vs mmol/L) are not detected.
- **Non-numeric results excluded** — values like "Will Follow" or "Pending" are skipped entirely and do not appear in the report.
- **Gender-specific ranges not resolved** — some reference ranges differ by sex (e.g. Hemoglobin, DHEA). The script uses the first numeric range it finds; the model does not currently resolve which range applies.

---

## Folder structure

```
hw5-Manny_Sotero/
├── .agents/
│   └── skills/
│       └── lab-report-analyzer/
│           ├── SKILL.md
│           ├── scripts/
│           │   └── analyze_labs.py
│           └── references/
│               └── Optimal Lab Ranges.xlsx
├── README.md
├── sample_lab.pdf
├── mapping.json
└── create_sample_lab.py
```
