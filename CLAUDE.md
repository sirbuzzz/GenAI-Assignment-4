# Lab Report Analyzer — Agent Instructions

## Available Skills

This project includes the `lab-report-analyzer` skill located at:
`.agents/skills/lab-report-analyzer/`

Always read `SKILL.md` before executing the skill.

## How to invoke the skill

When the user says anything like:
- "analyze my labs"
- "run the report"
- "compare my labs to the reference"

Follow these steps:

1. Read `.agents/skills/lab-report-analyzer/SKILL.md`
2. Use `sample_lab.pdf` as the lab input (already in this folder)
3. Use `mapping.json` as the biomarker name mapping (already in this folder)
4. Run the script:

```bash
python3 .agents/skills/lab-report-analyzer/scripts/analyze_labs.py sample_lab.pdf mapping.json output_report.pdf
```

5. Confirm the report was saved to `output_report.pdf`

## Important boundaries
- Do not make medical recommendations or diagnoses
- Do not interpret results clinically
- Report only — clinical judgment stays with the health coach
