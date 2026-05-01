---
name: lab-report-analyzer
description: Extracts biomarker values from a patient lab results PDF (e.g. Labcorp), compares them against a health coach's optimal reference ranges stored in the references folder, and produces a color-coded PDF report showing each biomarker's result, optimal range, status (In Range / Slightly Off / Out of Range), and relevant findings. Use when a patient lab PDF is uploaded and a comparison report needs to be generated.
---

## When to use this skill
- A patient lab PDF has been uploaded and a comparison report is needed
- The user asks to "analyze my labs", "run the report", or "compare my labs to the reference"

## When NOT to use this skill
- No lab PDF has been provided
- The user is asking for medical advice, diagnoses, or treatment recommendations
- The file provided is not a lab results PDF

## Inputs
- **User prompt** — e.g. "analyze my labs", "run the report", "compare my labs to the reference"
- **Lab results PDF** — uploaded by the user at runtime (e.g. Labcorp, Quest)
- **Reference Excel** — `references/Optimal Lab Ranges.xlsx` (static, already in the skill folder)

## Steps
1. Extract all biomarker names and their current result values from the lab PDF
   - The PDF is organized into panels (e.g. CBC With Differential, Comp. Metabolic Panel, Lipid Panel) — extract biomarkers across all panels
   - Strip footnote markers (e.g. ⁰¹, ⁰²) from biomarker names
   - Skip any result that says "Will Follow" or is non-numeric
   - Note the Labcorp reference interval for each biomarker
2. Load the reference Excel and extract: biomarker name, optimal range, HIGH findings, LOW findings
3. Use fuzzy matching to connect lab PDF biomarker names to reference Excel biomarker names
   - The model handles this step — names may be worded differently between sources
   - Flag any biomarker that cannot be confidently matched
4. For each matched biomarker, run the comparison script:
   - Green: result is within the coach's optimal range
   - Orange: result is outside the coach's optimal range but within Labcorp's reference interval
   - Red: result is outside both ranges (flagged High or Low by Labcorp)
5. Generate the output PDF report

## Output Format
A single PDF report organized by lab panel (e.g. CBC With Differential, Comp. Metabolic Panel, Lipid Panel), matching the structure of the original lab report. Each panel has its own labeled section with the following table structure:

| Biomarker | Result | Optimal Range | Status | Findings |
|-----------|--------|---------------|--------|----------|

- Panels are labeled as section headers matching the original lab PDF
- Status cell is color-coded: Green / Orange / Red
- Findings column pulls HIGH or LOW text from the reference Excel based on the result direction
- Biomarkers with no match in the reference sheet are listed at the bottom with status "Not Found"

## Limitations
- Biomarker name matching is fuzzy — always review unmatched markers manually
- Does not interpret results medically or make recommendations
- Optimal ranges in the reference sheet are the coach's ranges, not standard medical ranges
- Non-numeric results (e.g. "Will Follow") are excluded from the report
- Units are not converted — assumes units match between the PDF and reference sheet
