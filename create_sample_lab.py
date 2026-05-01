"""
Generates a synthetic Labcorp-style lab PDF for demo/testing purposes.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle

PANELS = [
    {
        "name": "CBC With Differential/Platelet",
        "biomarkers": [
            ("WBC",                    "5.0",  "",     "x10E3/uL", "3.4-10.8"),
            ("RBC",                    "4.95", "",     "x10E6/uL", "4.14-5.80"),
            ("Hemoglobin",             "14.4", "",     "g/dL",     "13.0-17.7"),
            ("Hematocrit",             "44.3", "",     "%",        "37.5-51.0"),
            ("MCV",                    "90",   "",     "fL",       "79-97"),
            ("MCH",                    "29.1", "",     "pg",       "26.6-33.0"),
            ("MCHC",                   "32.5", "",     "g/dL",     "31.5-35.7"),
            ("RDW",                    "12.7", "",     "%",        "11.6-15.4"),
            ("Platelets",              "262",  "",     "x10E3/uL", "150-450"),
            ("Neutrophils",            "51",   "",     "%",        "Not Estab."),
            ("Lymphs",                 "32",   "",     "%",        "Not Estab."),
            ("Monocytes",              "8",    "",     "%",        "Not Estab."),
            ("Eos",                    "7",    "",     "%",        "Not Estab."),
            ("Basos",                  "1",    "",     "%",        "Not Estab."),
            ("Neutrophils (Absolute)", "2.6",  "",     "x10E3/uL", "1.4-7.0"),
            ("Lymphs (Absolute)",      "1.6",  "",     "x10E3/uL", "0.7-3.1"),
            ("Monocytes(Absolute)",    "0.4",  "",     "x10E3/uL", "0.1-0.9"),
            ("Eos (Absolute)",         "0.4",  "",     "x10E3/uL", "0.0-0.4"),
            ("Baso (Absolute)",        "0.0",  "",     "x10E3/uL", "0.0-0.2"),
            ("Immature Granulocytes",  "1",    "",     "%",        "Not Estab."),
            ("Immature Grans (Abs)",   "0.0",  "",     "x10E3/uL", "0.0-0.1"),
        ],
    },
    {
        "name": "Comp. Metabolic Panel (14)",
        "biomarkers": [
            ("Glucose",                 "84",   "",    "mg/dL",     "70-99"),
            ("BUN",                     "12",   "",    "mg/dL",     "6-20"),
            ("Creatinine",              "0.74", "Low", "mg/dL",     "0.76-1.27"),
            ("eGFR",                    "123",  "",    "mL/min/1.73","59-999"),
            ("BUN/Creatinine Ratio",    "16",   "",    "",          "9-20"),
            ("Sodium",                  "139",  "",    "mmol/L",    "134-144"),
            ("Potassium",               "4.3",  "",    "mmol/L",    "3.5-5.2"),
            ("Chloride",                "100",  "",    "mmol/L",    "96-106"),
            ("Carbon Dioxide, Total",   "24",   "",    "mmol/L",    "20-29"),
            ("Calcium",                 "9.4",  "",    "mg/dL",     "8.7-10.2"),
            ("Protein, Total",          "7.6",  "",    "g/dL",      "6.0-8.5"),
            ("Albumin",                 "4.6",  "",    "g/dL",      "4.1-5.1"),
            ("Globulin, Total",         "3.0",  "",    "g/dL",      "1.5-4.5"),
            ("Bilirubin, Total",        "0.4",  "",    "mg/dL",     "0.0-1.2"),
            ("Alkaline Phosphatase",    "70",   "",    "IU/L",      "47-123"),
            ("AST (SGOT)",              "22",   "",    "IU/L",      "0-40"),
            ("ALT (SGPT)",              "32",   "",    "IU/L",      "0-44"),
        ],
    },
    {
        "name": "Lipid Panel",
        "biomarkers": [
            ("Cholesterol, Total",      "172",  "",    "mg/dL",     "100-199"),
            ("Triglycerides",           "134",  "",    "mg/dL",     "0-149"),
            ("HDL Cholesterol",         "39",   "Low", "mg/dL",     "39-999"),
            ("VLDL Cholesterol Cal",    "22",   "",    "mg/dL",     "5-40"),
            ("LDL Chol Calc (NIH)",     "111",  "High","mg/dL",     "0-99"),
        ],
    },
    {
        "name": "Hemoglobin A1c",
        "biomarkers": [
            ("Hemoglobin A1c",          "5.5",  "",    "%",         "4.8-5.6"),
        ],
    },
    {
        "name": "Thyroxine (T4) Free, Direct",
        "biomarkers": [
            ("T4,Free(Direct)",         "1.65", "",    "ng/dL",     "0.82-1.77"),
        ],
    },
    {
        "name": "DHEA-Sulfate",
        "biomarkers": [
            ("DHEA-Sulfate",            "99.1", "Low", "ug/dL",     "138.5-475.2"),
        ],
    },
    {
        "name": "TSH",
        "biomarkers": [
            ("TSH",                     "0.815","",    "uIU/mL",    "0.450-4.500"),
        ],
    },
    {
        "name": "Estradiol",
        "biomarkers": [
            ("Estradiol",               "30.4", "",    "pg/mL",     "7.6-42.6"),
        ],
    },
    {
        "name": "GGT",
        "biomarkers": [
            ("GGT",                     "58",   "",    "IU/L",      "0-65"),
        ],
    },
    {
        "name": "Insulin",
        "biomarkers": [
            ("Insulin",                 "24.1", "",    "uIU/mL",    "2.6-24.9"),
        ],
    },
    {
        "name": "C-Reactive Protein, Quant",
        "biomarkers": [
            ("C-Reactive Protein, Quant","3",   "",    "mg/L",      "0-10"),
        ],
    },
    {
        "name": "Triiodothyronine (T3), Free",
        "biomarkers": [
            ("Triiodothyronine (T3), Free","3.4","",  "pg/mL",     "2.0-4.4"),
        ],
    },
    {
        "name": "Apolipoprotein B",
        "biomarkers": [
            ("Apolipoprotein B",        "98",   "High","mg/dL",     "0-90"),
        ],
    },
]


def create_sample_lab_pdf(output_path: str) -> None:
    styles_map = {
        "title":  ParagraphStyle("title",  fontSize=13, fontName="Helvetica-Bold", spaceAfter=4),
        "meta":   ParagraphStyle("meta",   fontSize=8,  fontName="Helvetica", spaceAfter=8),
        "panel":  ParagraphStyle("panel",  fontSize=10, fontName="Helvetica-Bold", textColor=colors.white),
        "cell":   ParagraphStyle("cell",   fontSize=7,  fontName="Helvetica", leading=9),
        "hcell":  ParagraphStyle("hcell",  fontSize=7,  fontName="Helvetica-Bold", leading=9),
    }

    HEADER_BG = colors.HexColor("#343a40")
    SUBHEAD_BG = colors.HexColor("#f8f9fa")
    BORDER = colors.HexColor("#dee2e6")
    FLAG_RED = colors.HexColor("#f8d7da")

    col_widths = [2.2*inch, 1.0*inch, 0.7*inch, 0.9*inch, 1.5*inch]
    page_width = sum(col_widths)

    story = []
    story.append(Paragraph("Labcorp — Lab Report (Sample / Demo)", styles_map["title"]))
    story.append(Paragraph(
        "Date Collected: 04/23/2026 &nbsp;&nbsp; Date Reported: 04/25/2026 &nbsp;&nbsp; Fasting: Yes",
        styles_map["meta"]
    ))
    story.append(Spacer(1, 8))

    for panel in PANELS:
        # Panel header bar
        hdr = Table([[Paragraph(panel["name"], styles_map["panel"])]], colWidths=[page_width])
        hdr.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), HEADER_BG),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("TOPPADDING",    (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(hdr)

        col_header = [[
            Paragraph("Test",                     styles_map["hcell"]),
            Paragraph("Current Result and Flag",  styles_map["hcell"]),
            Paragraph("Flag",                     styles_map["hcell"]),
            Paragraph("Units",                    styles_map["hcell"]),
            Paragraph("Reference Interval",       styles_map["hcell"]),
        ]]

        rows = []
        flag_rows = []
        for i, (name, value, flag, units, ref) in enumerate(panel["biomarkers"]):
            row = [
                Paragraph(name,  styles_map["cell"]),
                Paragraph(value, styles_map["cell"]),
                Paragraph(flag,  styles_map["cell"]),
                Paragraph(units, styles_map["cell"]),
                Paragraph(ref,   styles_map["cell"]),
            ]
            rows.append(row)
            if flag in ("Low", "High"):
                flag_rows.append(i + 1)  # +1 for header offset

        data = col_header + rows
        t = Table(data, colWidths=col_widths, repeatRows=1)

        style_cmds = [
            ("BACKGROUND",    (0,0), (-1,0), SUBHEAD_BG),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 7),
            ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ]
        for r in flag_rows:
            style_cmds.append(("BACKGROUND", (1,r), (2,r), FLAG_RED))

        t.setStyle(TableStyle(style_cmds))
        story.append(t)
        story.append(Spacer(1, 10))

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    doc.build(story)
    print(f"Sample lab PDF created: {output_path}")


if __name__ == "__main__":
    create_sample_lab_pdf("sample_lab.pdf")
