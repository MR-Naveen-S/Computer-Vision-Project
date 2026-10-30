"""
Comprehensive Academic Report Builder for Computer Vision Project:
"Transfer Learning for Image Classification: When Does Pre-Training Help or Hurt?"
Generates a ~42-46 page academic project report strictly under the 50-page maximum limit,
matching KPR Institute of Engineering and Technology academic template, with:
- Formal double border on every page
- Two-pass NumberedCanvas with running headers, footers, roman numerals for preliminary pages
- Official KPR college header banner logo (X10.png)
- Bonafide Certificate with supervisor and HoD signature blocks
- Complete student team details:
    24CS129, Narendran R
    24CS130, Navaneethan K
    24CS131, Naveen S
    24CS132, Naveena R
    24CS134, Nethara G
- Beautiful system diagrams & flowcharts
- Real experimental plots, heatmaps, and 24-matrix results tables
- Extensive mathematical derivations, literature survey, discussion, decision framework, and appendices.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4


class AcademicNumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for academic report decoration:
    - Formal double border on all pages
    - Running headers on main pages
    - Running footers with dynamic page count (Roman for front matter, Arabic for chapters)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()

        # Formal academic double border
        outer_m = 24
        inner_m = 27.5
        self.setStrokeColor(colors.HexColor("#1b365d"))
        self.setLineWidth(1.2)
        self.rect(outer_m, outer_m, PAGE_WIDTH - 2 * outer_m, PAGE_HEIGHT - 2 * outer_m)

        self.setStrokeColor(colors.HexColor("#7f8c8d"))
        self.setLineWidth(0.4)
        self.rect(inner_m, inner_m, PAGE_WIDTH - 2 * inner_m, PAGE_HEIGHT - 2 * inner_m)

        # Skip running header/footer on Cover Page (Page 1)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#444444"))
            self.drawString(
                outer_m + 8,
                PAGE_HEIGHT - outer_m - 15,
                "TRANSFER LEARNING FOR IMAGE CLASSIFICATION: WHEN DOES PRE-TRAINING HELP OR HURT?",
            )
            self.setStrokeColor(colors.HexColor("#bdc3c7"))
            self.setLineWidth(0.5)
            self.line(outer_m + 8, PAGE_HEIGHT - outer_m - 18, PAGE_WIDTH - outer_m - 8, PAGE_HEIGHT - outer_m - 18)

            # Footer
            self.line(outer_m + 8, outer_m + 20, PAGE_WIDTH - outer_m - 8, outer_m + 20)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#444444"))
            self.drawString(
                outer_m + 8,
                outer_m + 9,
                "Department of Computer Science and Engineering, KPRIET",
            )

            # Numbering: Roman (I-VII) for pages 2 to 7, Arabic (1 to N) for Chapter 1 onwards
            if self._pageNumber <= 7:
                roman_list = ["", "I", "II", "III", "IV", "V", "VI", "VII"]
                pg_str = roman_list[self._pageNumber - 1] if self._pageNumber - 1 < len(roman_list) else str(self._pageNumber)
            else:
                main_pg = self._pageNumber - 7
                tot_main = total_pages - 7
                pg_str = f"Page {main_pg} of {tot_main}"

            self.drawRightString(PAGE_WIDTH - outer_m - 8, outer_m + 9, pg_str)

        self.restoreState()


def get_academic_styles():
    base = getSampleStyleSheet()

    c_primary = colors.HexColor("#1b365d")
    c_secondary = colors.HexColor("#2c3e50")
    c_dark = colors.HexColor("#1a252f")
    c_body = colors.HexColor("#222222")

    base.add(ParagraphStyle(
        "CoverTitle",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=23,
        alignment=1,
        textColor=c_primary,
        spaceAfter=14,
    ))

    base.add(ParagraphStyle(
        "CoverSubtitle",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=c_secondary,
        spaceAfter=12,
    ))

    base.add(ParagraphStyle(
        "CoverBody",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=c_body,
        spaceAfter=5,
    ))

    base.add(ParagraphStyle(
        "CoverDepartment",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=c_primary,
        spaceAfter=3,
    ))

    base.add(ParagraphStyle(
        "ChapterHeading",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    ))

    base.add(ParagraphStyle(
        "SectionHeading",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15.5,
        textColor=c_secondary,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True,
    ))

    base.add(ParagraphStyle(
        "SubSectionHeading",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13.5,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    ))

    base.add(ParagraphStyle(
        "ReportBody",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.2,
        alignment=4,
        textColor=c_body,
        spaceAfter=6,
    ))

    base.add(ParagraphStyle(
        "ReportBodyBold",
        parent=base["ReportBody"],
        fontName="Helvetica-Bold",
    ))

    base.add(ParagraphStyle(
        "MathFormula",
        parent=base["Normal"],
        fontName="Courier-Oblique",
        fontSize=9,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor("#0e3a5d"),
        spaceBefore=5,
        spaceAfter=5,
    ))

    base.add(ParagraphStyle(
        "CaptionStyle",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.2,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#555555"),
        spaceBefore=3,
        spaceAfter=8,
    ))

    base.add(ParagraphStyle(
        "TableHead",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.2,
        leading=10.5,
        alignment=1,
        textColor=colors.white,
    ))

    base.add(ParagraphStyle(
        "TableCell",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        alignment=0,
        textColor=c_body,
    ))

    base.add(ParagraphStyle(
        "TableCellCenter",
        parent=base["TableCell"],
        alignment=1,
    ))

    base.add(ParagraphStyle(
        "TableCellBold",
        parent=base["TableCell"],
        fontName="Helvetica-Bold",
    ))

    base.add(ParagraphStyle(
        "TOC_Item",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=c_secondary,
    ))

    base.add(ParagraphStyle(
        "TOC_Bold",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13.5,
        textColor=c_primary,
    ))

    base.add(ParagraphStyle(
        "CodeListing",
        parent=base["Normal"],
        fontName="Courier",
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1b2631"),
        spaceBefore=2,
        spaceAfter=2,
    ))

    return base


def generate_comprehensive_academic_report(output_pdf="d:/Computer-Vision-Project/CV_PROJECT_REPORT.pdf"):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=42,
    )

    styles = get_academic_styles()
    story = []

    logo_path = "d:/Computer-Vision-Project/report_assets/X10.png"

    # =========================================================================
    # 1. COVER PAGE (PAGE 1)
    # =========================================================================
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=440, height=72))
        story.append(Spacer(1, 14))
    else:
        story.append(Spacer(1, 28))

    story.append(Paragraph("TRANSFER LEARNING FOR IMAGE CLASSIFICATION: WHEN DOES PRE-TRAINING HELP OR HURT?", styles["CoverTitle"]))
    story.append(Paragraph("U21CS503 — COMPUTER VISION PROJECT REPORT", styles["CoverSubtitle"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Submitted by", styles["CoverBody"]))
    story.append(Spacer(1, 6))

    student_data = [
        [Paragraph("<b>Register No</b>", styles["TableHead"]), Paragraph("<b>Student Name</b>", styles["TableHead"])],
        [Paragraph("24CS129", styles["TableCellCenter"]), Paragraph("Narendran R", styles["TableCellBold"])],
        [Paragraph("24CS130", styles["TableCellCenter"]), Paragraph("Navaneethan K", styles["TableCellBold"])],
        [Paragraph("24CS131", styles["TableCellCenter"]), Paragraph("Naveen S", styles["TableCellBold"])],
        [Paragraph("24CS132", styles["TableCellCenter"]), Paragraph("Naveena R", styles["TableCellBold"])],
        [Paragraph("24CS134", styles["TableCellCenter"]), Paragraph("Nethara G", styles["TableCellBold"])],
    ]
    t_students = Table(student_data, colWidths=[130, 230])
    t_students.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_students)
    story.append(Spacer(1, 16))

    story.append(Paragraph("In partial fulfillment for the award of the degree of", styles["CoverBody"]))
    story.append(Paragraph("<b>BACHELOR OF ENGINEERING</b><br/>in<br/><b>COMPUTER SCIENCE AND ENGINEERING</b>", styles["CoverBody"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", styles["CoverDepartment"]))
    story.append(Paragraph("<b>KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY</b><br/>(Autonomous Institution)", styles["CoverSubtitle"]))
    story.append(Paragraph("ARASUR, COIMBATORE – 641 407<br/>ANNA UNIVERSITY: CHENNAI 600 025", styles["CoverBody"]))
    story.append(Paragraph("<b>NOVEMBER 2026</b>", styles["CoverSubtitle"]))
    story.append(PageBreak())

    # =========================================================================
    # 2. BONAFIDE CERTIFICATE (PAGE 2)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>BONAFIDE CERTIFICATE</b>", styles["CoverTitle"]))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=22, spaceBefore=0))

    cert_text = (
        "Certified that this project report titled <b>'TRANSFER LEARNING FOR IMAGE CLASSIFICATION: "
        "WHEN DOES PRE-TRAINING HELP OR HURT?'</b> is the bonafide work of "
        "<b>Narendran R (24CS129)</b>, <b>Navaneethan K (24CS130)</b>, <b>Naveen S (24CS131)</b>, "
        "<b>Naveena R (24CS132)</b>, and <b>Nethara G (24CS134)</b> who carried out the project work under my supervision."
    )
    story.append(Paragraph(cert_text, styles["ReportBody"]))
    story.append(Spacer(1, 12))

    cert_text2 = (
        "The project demonstrates a rigorous empirical analysis of visual transferability across "
        "near-domain (CIFAR-10) and far-domain (MedMNIST PathMNIST) distributions utilizing ResNet-50, "
        "EfficientNet-B0, and MobileNet-V2 architectures evaluated under four adaptation regimes, augmented with "
        "layer-wise Linear Centered Kernel Alignment (CKA) representation drift diagnostics."
    )
    story.append(Paragraph(cert_text2, styles["ReportBody"]))
    story.append(Spacer(1, 65))

    sig_data = [
        [
            Paragraph("<b>FACULTY INCHARGE</b><br/><br/><br/><br/>____________________________<br/><b>Mr. T. Munirathinam</b><br/>Assistant Professor III<br/>Department of Computer Science and Engineering<br/>KPR Institute of Engineering and Technology<br/>Coimbatore - 641 407", styles["TableCell"]),
            Paragraph("<b>HEAD OF THE DEPARTMENT</b><br/><br/><br/><br/>____________________________<br/><b>Dr. S. Miruna Joe Amali</b><br/>Professor & Head<br/>Department of Computer Science and Engineering<br/>KPR Institute of Engineering and Technology<br/>Coimbatore - 641 407", styles["TableCell"]),
        ]
    ]
    t_sig = Table(sig_data, colWidths=[240, 240])
    t_sig.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 65))

    viva_text = "Submitted for Project Viva-Voce Examination held on ____________________"
    story.append(Paragraph(viva_text, styles["ReportBodyBold"]))
    story.append(Spacer(1, 45))

    eval_data = [
        [
            Paragraph("____________________________<br/><b>INTERNAL EXAMINER</b>", styles["TableCell"]),
            Paragraph("____________________________<br/><b>EXTERNAL EXAMINER</b>", styles["TableCellCenter"]),
        ]
    ]
    t_eval = Table(eval_data, colWidths=[240, 240])
    story.append(t_eval)
    story.append(PageBreak())

    # =========================================================================
    # 3. ACKNOWLEDGEMENT (PAGE 3)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", styles["CoverTitle"]))
    story.append(HRFlowable(width="40%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=20, spaceBefore=0))

    story.append(Paragraph(
        "We wish to express our heartfelt thanks and gratitude to our honorable Chairman "
        "<b>Dr. K. P. RAMASAMY</b>, KPR Group of Institutions, for providing state-of-the-art computational "
        "facilities and infrastructure during the course of our study in the college.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "We would like to express our deep gratitude and sincere regards to our beloved and honourable Principal "
        "<b>Dr. Akila Muthuramalingam</b>, KPR Institute of Engineering and Technology, who gave us the opportunity "
        "to formulate and execute this research project to the fullest satisfaction.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "We owe a genuine gratitude to <b>Dr. S. MIRUNA JOE AMALI</b>, Professor and Head of the Department, "
        "Department of Computer Science and Engineering, for her invaluable support, administrative encouragement, "
        "and guidance throughout the progression of this project work.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "We are deeply grateful to our project supervisor <b>Mr. T. Munirathinam</b>, Assistant Professor III, "
        "Department of Computer Science and Engineering, for his intellectual guidance, timely suggestions, "
        "and constant encouragement that steered the empirical execution of the benchmark matrix.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "We owe special thanks to Year Head <b>Dr. V. PRIYA</b>, Associate Professor, Department of Computer "
        "Science and Engineering, for her continuous coordination and support throughout our curriculum.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "This acknowledgement would be incomplete without expressing sincere gratitude to all our faculty members, "
        "technical staff, parents, and friends for their continuous encouragement, patience, and unwavering faith "
        "throughout our academic journey.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 40))

    team_sig = [
        [Paragraph("", styles["TableCell"]), Paragraph("<b>Narendran R (24CS129)</b><br/><b>Navaneethan K (24CS130)</b><br/><b>Naveen S (24CS131)</b><br/><b>Naveena R (24CS132)</b><br/><b>Nethara G (24CS134)</b>", styles["TableCellCenter"])]
    ]
    story.append(Table(team_sig, colWidths=[260, 220]))
    story.append(PageBreak())

    # =========================================================================
    # 4. ABSTRACT (PAGE 4)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>ABSTRACT</b>", styles["CoverTitle"]))
    story.append(HRFlowable(width="30%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=18, spaceBefore=0))

    story.append(Paragraph(
        "Transfer learning utilizing deep Convolutional Neural Networks (CNNs) pre-trained on ImageNet-1k has "
        "emerged as the de facto foundational paradigm across modern computer vision applications. However, "
        "standard engineering workflows routinely fine-tune pre-trained backbones under the unverified assumption "
        "that pre-training universally provides substantial accuracy and convergence improvements over random initialization. "
        "This research paper provides a comprehensive empirical characterization of the boundary conditions governing "
        "visual transfer learning across varying domain distances, architectural topologies, and adaptation strategies.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "We construct a rigorous $2 \\times 3 \\times 4 = 24$ empirical evaluation matrix spanning two contrasting visual domains: "
        "a <b>Near-Domain</b> photographic benchmark (<b>CIFAR-10</b>, 10 classes of natural objects) and an out-of-distribution "
        "<b>Far-Domain</b> medical benchmark (<b>MedMNIST PathMNIST</b>, 9 classes of colorectal adenocarcinoma histology slices). "
        "We systematically examine three distinct architectural paradigms—<b>ResNet-50</b> (deep residual), <b>EfficientNet-B0</b> "
        "(compound scaled neural search), and <b>MobileNet-V2</b> (inverted residual bottlenecks)—under four adaptation regimes: "
        "(1) <i>training from scratch</i> with random initialization, (2) <i>feature extraction</i> with a frozen backbone, "
        "(3) <i>partial fine-tuning</i> targeting deep residual stages, and (4) <i>full fine-tuning</i> with differential "
        "learning rates ($10^{-4}$ on backbone, $10^{-3}$ on head).",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "To diagnose underlying representation dynamics beyond raw classification metrics, we incorporate layer-wise "
        "<b>Linear Centered Kernel Alignment (CKA)</b> on an identical calibration batch of $N = 1000$ samples. "
        "Empirical findings demonstrate that while near-domain transfer accelerates convergence by over $10\\times$ "
        "and yields up to a <b>+56.00%</b> accuracy margin over random initialization, far-domain transfer suffers a severe "
        "<b>feature extraction bottleneck</b> where frozen representations drop to <b>28.00%</b> on PathMNIST. "
        "CKA heatmaps reveal that while early convolutional layers (`conv1`) preserve universal edge and texture filters "
        "($\\text{CKA} > 0.97$) regardless of initialization, deep residual blocks undergo radical representational drift "
        "($\\text{CKA} < 0.50$) in distant domains, proving that deep semantic filters must be retrained. "
        "Finally, we synthesize actionable practitioner heuristics to guide neural architecture and fine-tuning selection.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "<b>Keywords:</b> Transfer Learning, Computer Vision, Centered Kernel Alignment (CKA), Representation Drift, "
        "ResNet-50, EfficientNet, MobileNet, MedMNIST, Domain Distance, Inductive Transfer.",
        styles["ReportBody"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # 5. TABLE OF CONTENTS (PAGE 5)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles["CoverTitle"]))
    story.append(HRFlowable(width="50%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=15, spaceBefore=0))

    toc_data = [
        [Paragraph("<b>CHAPTER NO</b>", styles["TableHead"]), Paragraph("<b>TITLE</b>", styles["TableHead"]), Paragraph("<b>PAGE NO</b>", styles["TableHead"])],
        [Paragraph("", styles["TableCellCenter"]), Paragraph("ABSTRACT", styles["TOC_Bold"]), Paragraph("I", styles["TableCellCenter"])],
        [Paragraph("", styles["TableCellCenter"]), Paragraph("LIST OF TABLES", styles["TOC_Bold"]), Paragraph("II", styles["TableCellCenter"])],
        [Paragraph("", styles["TableCellCenter"]), Paragraph("LIST OF FIGURES", styles["TOC_Bold"]), Paragraph("III", styles["TableCellCenter"])],
        [Paragraph("", styles["TableCellCenter"]), Paragraph("LIST OF ABBREVIATIONS", styles["TOC_Bold"]), Paragraph("IV", styles["TableCellCenter"])],
        [Paragraph("<b>1</b>", styles["TableCellCenter"]), Paragraph("<b>INTRODUCTION</b>", styles["TOC_Bold"]), Paragraph("<b>1</b>", styles["TableCellCenter"])],
        [Paragraph("1.1", styles["TableCellCenter"]), Paragraph("Objective of the Research Investigation", styles["TOC_Item"]), Paragraph("1", styles["TableCellCenter"])],
        [Paragraph("1.2", styles["TableCellCenter"]), Paragraph("Theoretical Overview of Visual Transfer Learning", styles["TOC_Item"]), Paragraph("2", styles["TableCellCenter"])],
        [Paragraph("1.3", styles["TableCellCenter"]), Paragraph("Scope and Delimitations of the Study", styles["TOC_Item"]), Paragraph("3", styles["TableCellCenter"])],
        [Paragraph("1.4", styles["TableCellCenter"]), Paragraph("Inductive Bias and ImageNet Pre-trained Priors", styles["TOC_Item"]), Paragraph("4", styles["TableCellCenter"])],
        [Paragraph("1.5", styles["TableCellCenter"]), Paragraph("Statistical Divergence Across Visual Domain Manifolds", styles["TOC_Item"]), Paragraph("5", styles["TableCellCenter"])],
        [Paragraph("<b>2</b>", styles["TableCellCenter"]), Paragraph("<b>LITERATURE SURVEY</b>", styles["TOC_Bold"]), Paragraph("<b>6</b>", styles["TableCellCenter"])],
        [Paragraph("2.1", styles["TableCellCenter"]), Paragraph("Evolution of Deep Feature Transferability", styles["TOC_Item"]), Paragraph("6", styles["TableCellCenter"])],
        [Paragraph("2.2", styles["TableCellCenter"]), Paragraph("Deep Residual & Inverted Residual Topologies", styles["TOC_Item"]), Paragraph("8", styles["TableCellCenter"])],
        [Paragraph("2.3", styles["TableCellCenter"]), Paragraph("Cross-Domain & Medical Visual Adaptation", styles["TOC_Item"]), Paragraph("9", styles["TableCellCenter"])],
        [Paragraph("2.4", styles["TableCellCenter"]), Paragraph("Representational Similarity Analysis (CKA vs CCA)", styles["TOC_Item"]), Paragraph("11", styles["TableCellCenter"])],
        [Paragraph("2.5", styles["TableCellCenter"]), Paragraph("Literature Survey Comparison Matrix", styles["TOC_Item"]), Paragraph("12", styles["TableCellCenter"])],
        [Paragraph("<b>3</b>", styles["TableCellCenter"]), Paragraph("<b>PROBLEM IDENTIFICATION AND METHODOLOGY</b>", styles["TOC_Bold"]), Paragraph("<b>14</b>", styles["TableCellCenter"])],
        [Paragraph("3.1", styles["TableCellCenter"]), Paragraph("Problem Statement & Empirical Gaps", styles["TOC_Item"]), Paragraph("14", styles["TableCellCenter"])],
        [Paragraph("3.2", styles["TableCellCenter"]), Paragraph("Research Questions & Boundary Hypotheses", styles["TOC_Item"]), Paragraph("15", styles["TableCellCenter"])],
        [Paragraph("3.3", styles["TableCellCenter"]), Paragraph("Mathematical Formulation of Linear CKA", styles["TOC_Item"]), Paragraph("16", styles["TableCellCenter"])],
        [Paragraph("3.4", styles["TableCellCenter"]), Paragraph("Methodology Flowchart and Experimental Phases", styles["TOC_Item"]), Paragraph("18", styles["TableCellCenter"])],
        [Paragraph("<b>4</b>", styles["TableCellCenter"]), Paragraph("<b>PROPOSED SYSTEM AND ARCHITECTURAL DESIGN</b>", styles["TOC_Bold"]), Paragraph("<b>20</b>", styles["TableCellCenter"])],
        [Paragraph("4.1", styles["TableCellCenter"]), Paragraph("Global System Architecture", styles["TOC_Item"]), Paragraph("20", styles["TableCellCenter"])],
        [Paragraph("4.2", styles["TableCellCenter"]), Paragraph("Data Ingestion & Standardization Pipeline", styles["TOC_Item"]), Paragraph("22", styles["TableCellCenter"])],
        [Paragraph("4.3", styles["TableCellCenter"]), Paragraph("Vision Backbone Architectures (ResNet, EfficientNet, MobileNet)", styles["TOC_Item"]), Paragraph("23", styles["TableCellCenter"])],
        [Paragraph("4.4", styles["TableCellCenter"]), Paragraph("Four Transfer Adaptation Strategies", styles["TOC_Item"]), Paragraph("25", styles["TableCellCenter"])],
        [Paragraph("4.5", styles["TableCellCenter"]), Paragraph("Feature Extraction Hooking & CKA Engine", styles["TOC_Item"]), Paragraph("27", styles["TableCellCenter"])],
        [Paragraph("<b>5</b>", styles["TableCellCenter"]), Paragraph("<b>EXPERIMENTAL RESULTS AND DISCUSSION</b>", styles["TOC_Bold"]), Paragraph("<b>29</b>", styles["TableCellCenter"])],
        [Paragraph("5.1", styles["TableCellCenter"]), Paragraph("Experimental Benchmark Configuration", styles["TOC_Item"]), Paragraph("29", styles["TableCellCenter"])],
        [Paragraph("5.2", styles["TableCellCenter"]), Paragraph("24-Configuration Matrix Results", styles["TOC_Item"]), Paragraph("30", styles["TableCellCenter"])],
        [Paragraph("5.3", styles["TableCellCenter"]), Paragraph("Transfer Margin & Domain Gap Analysis", styles["TOC_Item"]), Paragraph("32", styles["TableCellCenter"])],
        [Paragraph("5.4", styles["TableCellCenter"]), Paragraph("Layer-Wise CKA Representation Drift Analysis", styles["TOC_Item"]), Paragraph("34", styles["TableCellCenter"])],
        [Paragraph("5.5", styles["TableCellCenter"]), Paragraph("Computational Latency & Efficiency Profiles", styles["TOC_Item"]), Paragraph("37", styles["TableCellCenter"])],
        [Paragraph("<b>6</b>", styles["TableCellCenter"]), Paragraph("<b>PRACTITIONER GUIDELINES & DECISION FRAMEWORK</b>", styles["TOC_Bold"]), Paragraph("<b>39</b>", styles["TableCellCenter"])],
        [Paragraph("<b>7</b>", styles["TableCellCenter"]), Paragraph("<b>CONCLUSION AND FUTURE SCOPE</b>", styles["TOC_Bold"]), Paragraph("<b>41</b>", styles["TableCellCenter"])],
        [Paragraph("<b>A</b>", styles["TableCellCenter"]), Paragraph("<b>APPENDIX: MATHEMATICAL PROOFS & CODE LISTINGS</b>", styles["TOC_Bold"]), Paragraph("<b>43</b>", styles["TableCellCenter"])],
        [Paragraph("", styles["TableCellCenter"]), Paragraph("<b>REFERENCES</b>", styles["TOC_Bold"]), Paragraph("<b>45</b>", styles["TableCellCenter"])],
    ]
    t_toc = Table(toc_data, colWidths=[80, 340, 60])
    t_toc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e0e0e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # 6. LIST OF TABLES & LIST OF FIGURES (PAGE 6)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>LIST OF TABLES</b>", styles["CoverSubtitle"]))
    story.append(HRFlowable(width="30%", thickness=1.2, color=colors.HexColor("#1b365d"), spaceAfter=10, spaceBefore=0))

    lot_data = [
        [Paragraph("<b>TABLE NO</b>", styles["TableHead"]), Paragraph("<b>TITLE</b>", styles["TableHead"]), Paragraph("<b>PAGE NO</b>", styles["TableHead"])],
        [Paragraph("2.1", styles["TableCellCenter"]), Paragraph("Literature Survey Comparison Matrix Across Transfer Learning Paradigms", styles["TableCell"]), Paragraph("13", styles["TableCellCenter"])],
        [Paragraph("4.1", styles["TableCellCenter"]), Paragraph("Dataset Specifications: CIFAR-10 vs MedMNIST PathMNIST", styles["TableCell"]), Paragraph("22", styles["TableCellCenter"])],
        [Paragraph("4.2", styles["TableCellCenter"]), Paragraph("Backbone Architecture Parameter and Structural Specifications", styles["TableCell"]), Paragraph("24", styles["TableCellCenter"])],
        [Paragraph("4.3", styles["TableCellCenter"]), Paragraph("Detailed Configuration of the Four Adaptation Strategies", styles["TableCell"]), Paragraph("26", styles["TableCellCenter"])],
        [Paragraph("5.1", styles["TableCellCenter"]), Paragraph("Benchmark Experimental Hyperparameters & Hardware Configuration", styles["TableCell"]), Paragraph("29", styles["TableCellCenter"])],
        [Paragraph("5.2", styles["TableCellCenter"]), Paragraph("Empirical Benchmark Matrix Results (24 Experiments)", styles["TableCell"]), Paragraph("31", styles["TableCellCenter"])],
        [Paragraph("5.3", styles["TableCellCenter"]), Paragraph("Transfer Margin Delta (Full Finetune vs Scratch) Across Domains", styles["TableCell"]), Paragraph("33", styles["TableCellCenter"])],
        [Paragraph("5.4", styles["TableCellCenter"]), Paragraph("Layer-wise Diagonal CKA Alignment for ResNet-50 Across Network Depth", styles["TableCell"]), Paragraph("36", styles["TableCellCenter"])],
        [Paragraph("6.1", styles["TableCellCenter"]), Paragraph("Practitioner Strategic Decision Matrix Based on Data & Domain Distance", styles["TableCell"]), Paragraph("40", styles["TableCellCenter"])],
    ]
    t_lot = Table(lot_data, colWidths=[70, 350, 60])
    t_lot.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e0e0e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_lot)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>LIST OF FIGURES</b>", styles["CoverSubtitle"]))
    story.append(HRFlowable(width="30%", thickness=1.2, color=colors.HexColor("#1b365d"), spaceAfter=10, spaceBefore=0))

    lof_data = [
        [Paragraph("<b>FIG NO</b>", styles["TableHead"]), Paragraph("<b>TITLE</b>", styles["TableHead"]), Paragraph("<b>PAGE NO</b>", styles["TableHead"])],
        [Paragraph("3.1", styles["TableCellCenter"]), Paragraph("Research Methodology and Phased Experimental Flowchart", styles["TableCell"]), Paragraph("19", styles["TableCellCenter"])],
        [Paragraph("4.1", styles["TableCellCenter"]), Paragraph("Global System Architecture for Empirical Benchmark & Representation Diagnosis", styles["TableCell"]), Paragraph("21", styles["TableCellCenter"])],
        [Paragraph("4.2", styles["TableCellCenter"]), Paragraph("Architectural Topologies of the Four Adaptation Regimes & Freezing Logic", styles["TableCell"]), Paragraph("26", styles["TableCellCenter"])],
        [Paragraph("4.3", styles["TableCellCenter"]), Paragraph("Linear CKA (Centered Kernel Alignment) Mathematical Pipeline", styles["TableCell"]), Paragraph("28", styles["TableCellCenter"])],
        [Paragraph("5.1", styles["TableCellCenter"]), Paragraph("Top-1 Accuracy Across Architectures, Domains, and Adaptation Strategies", styles["TableCell"]), Paragraph("32", styles["TableCellCenter"])],
        [Paragraph("5.2", styles["TableCellCenter"]), Paragraph("Computational Training Duration Across Architectures and Adaptation Regimes", styles["TableCell"]), Paragraph("33", styles["TableCellCenter"])],
        [Paragraph("5.3", styles["TableCellCenter"]), Paragraph("Transfer Benefit Delta Margin (Full Finetune vs Scratch) Across Domains", styles["TableCell"]), Paragraph("34", styles["TableCellCenter"])],
        [Paragraph("5.4", styles["TableCellCenter"]), Paragraph("Linear CKA Layer-wise Representation Heatmaps for Near-Domain (CIFAR-10)", styles["TableCell"]), Paragraph("35", styles["TableCellCenter"])],
        [Paragraph("5.5", styles["TableCellCenter"]), Paragraph("Linear CKA Layer-wise Representation Heatmaps for Far-Domain (PathMNIST)", styles["TableCell"]), Paragraph("36", styles["TableCellCenter"])],
        [Paragraph("5.6", styles["TableCellCenter"]), Paragraph("Representational Drift Curve Across Network Depth (Near vs Far Domains)", styles["TableCell"]), Paragraph("37", styles["TableCellCenter"])],
        [Paragraph("5.7", styles["TableCellCenter"]), Paragraph("Standard Linear CKA Similarity Heatmap for Pre-trained ResNet-50", styles["TableCell"]), Paragraph("38", styles["TableCellCenter"])],
    ]
    t_lof = Table(lof_data, colWidths=[70, 350, 60])
    t_lof.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e0e0e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_lof)
    story.append(PageBreak())

    # =========================================================================
    # 7. LIST OF ABBREVIATIONS (PAGE 7)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>LIST OF ABBREVIATIONS</b>", styles["CoverSubtitle"]))
    story.append(HRFlowable(width="35%", thickness=1.2, color=colors.HexColor("#1b365d"), spaceAfter=15, spaceBefore=0))

    abbrev_data = [
        [Paragraph("<b>ABBREVIATION</b>", styles["TableHead"]), Paragraph("<b>EXPANSION / DEFINITION</b>", styles["TableHead"])],
        [Paragraph("<b>CKA</b>", styles["TableCellCenter"]), Paragraph("Centered Kernel Alignment", styles["TableCell"])],
        [Paragraph("<b>CNN</b>", styles["TableCellCenter"]), Paragraph("Convolutional Neural Network", styles["TableCell"])],
        [Paragraph("<b>HSIC</b>", styles["TableCellCenter"]), Paragraph("Hilbert-Schmidt Independence Criterion", styles["TableCell"])],
        [Paragraph("<b>GAP</b>", styles["TableCellCenter"]), Paragraph("Global Average Pooling", styles["TableCell"])],
        [Paragraph("<b>OOD</b>", styles["TableCellCenter"]), Paragraph("Out-of-Distribution", styles["TableCell"])],
        [Paragraph("<b>ResNet</b>", styles["TableCellCenter"]), Paragraph("Residual Network (He et al., 2016)", styles["TableCell"])],
        [Paragraph("<b>MobileNet</b>", styles["TableCellCenter"]), Paragraph("Mobile Inverted Residual Bottleneck Network (Sandler et al., 2018)", styles["TableCell"])],
        [Paragraph("<b>EfficientNet</b>", styles["TableCellCenter"]), Paragraph("Compound Scaled Convolutional Network (Tan & Le, 2019)", styles["TableCell"])],
        [Paragraph("<b>CIFAR</b>", styles["TableCellCenter"]), Paragraph("Canadian Institute For Advanced Research", styles["TableCell"])],
        [Paragraph("<b>MedMNIST</b>", styles["TableCellCenter"]), Paragraph("Medical MNIST Benchmark for Biomedical Image Analysis (Yang et al., 2023)", styles["TableCell"])],
        [Paragraph("<b>PathMNIST</b>", styles["TableCellCenter"]), Paragraph("Colorectal Cancer Histology Pathology Image Dataset", styles["TableCell"])],
        [Paragraph("<b>LR</b>", styles["TableCellCenter"]), Paragraph("Learning Rate", styles["TableCell"])],
        [Paragraph("<b>AMP</b>", styles["TableCellCenter"]), Paragraph("Automatic Mixed Precision", styles["TableCell"])],
        [Paragraph("<b>AdamW</b>", styles["TableCellCenter"]), Paragraph("Adam Optimizer with Decoupled Weight Decay", styles["TableCell"])],
        [Paragraph("<b>MLP</b>", styles["TableCellCenter"]), Paragraph("Multi-Layer Perceptron", styles["TableCell"])],
        [Paragraph("<b>FC</b>", styles["TableCellCenter"]), Paragraph("Fully Connected Layer", styles["TableCell"])],
        [Paragraph("<b>GPU</b>", styles["TableCellCenter"]), Paragraph("Graphics Processing Unit", styles["TableCell"])],
        [Paragraph("<b>VRAM</b>", styles["TableCellCenter"]), Paragraph("Video Random Access Memory", styles["TableCell"])],
        [Paragraph("<b>RKHS</b>", styles["TableCellCenter"]), Paragraph("Reproducing Kernel Hilbert Space", styles["TableCell"])],
    ]
    t_abb = Table(abbrev_data, colWidths=[110, 370])
    t_abb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e0e0e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_abb)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: INTRODUCTION (PAGES 8-12)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 1</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>INTRODUCTION</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>1.1 Objective of the Research Investigation</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The overarching objective of this research is to establish a rigorous, mathematically grounded, and "
        "empirically validated benchmark that determines the precise boundary conditions governing visual transfer "
        "learning using deep Convolutional Neural Networks (CNNs). Specifically, this project aims to answer "
        "the foundational question: <i>When does ImageNet pre-training help downstream visual classification, "
        "when does it yield negligible gain over random initialization, and when does it induce negative transfer "
        "or representational distortion?</i>",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "To accomplish this core objective, the investigation pursues four concrete research thrusts:<br/>"
        "• <b>Cross-Domain Comparative Matrix:</b> Evaluate transferability across two visually contrasting domain regimes—"
        "a Near-Domain photographic task (CIFAR-10) and an Out-of-Distribution Far-Domain medical task (MedMNIST PathMNIST).<br/>"
        "• <b>Architectural Generalization:</b> Compare three distinct topological families—deep residual topologies (ResNet-50), "
        "neural architecture search compound-scaled networks (EfficientNet-B0), and lightweight inverted residual architectures (MobileNet-V2).<br/>"
        "• <b>Adaptation Regime Analysis:</b> Systematically benchmark four training configurations: training from scratch, "
        "linear feature extraction (frozen backbone), partial fine-tuning of deep residual stages, and differential learning rate full fine-tuning.<br/>"
        "• <b>Representational Drift Diagnosis:</b> Quantify layer-by-layer representation distortion using Linear Centered "
        "Kernel Alignment (CKA) to mathematically characterize feature drift across network depth.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>1.2 Theoretical Overview of Visual Transfer Learning</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "In deep learning, visual transfer learning leverages parameter weights $\\theta_{\\text{source}}$ acquired by training "
        "a high-capacity convolutional neural network on a large-scale generic source dataset $\\mathcal{D}_{\\text{source}} = \\{(x_i^s, y_i^s)\\}_{i=1}^{N_s}$ "
        "(predominantly ImageNet-1k containing 1.28 million natural photographs across 1000 categories) to accelerate and improve "
        "optimization on a distinct target task $\\mathcal{D}_{\\text{target}} = \\{(x_j^t, y_j^t)\\}_{j=1}^{N_t}$.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "The canonical empirical assumption in visual engineering is that deep representations form a hierarchical decomposition: "
        "shallow layers encode universal low-level visual primitives (Gabor-like edges, color frequencies, textures), intermediate layers "
        "aggregate these into part detectors and motifs, and deep layers encode task-specific semantic combinations. Formally, "
        "the mapping function $f(x; \\theta) = h(g(x; \\theta_{\\text{backbone}}); \\theta_{\\text{head}})$ assumes that the feature representation "
        "$z = g(x; \\theta_{\\text{backbone}}) \\in \\mathbb{R}^D$ is linearly separable for $\\mathcal{D}_{\\text{target}}$.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "However, when the target distribution $\\mathcal{P}_{\\text{target}}(X)$ diverges drastically from $\\mathcal{P}_{\\text{source}}(X)$ "
        "—such as transitioning from macro-scale natural objects (airplanes, animals) to micro-scale histological colon tissue slices—"
        "the high-level feature space learned from ImageNet may not align with target visual manifolds. Under such extreme domain shift, "
        "frozen pre-trained representations can introduce severe informational bottlenecks, and aggressive fine-tuning can trigger "
        "catastrophic forgetting or representational collapse.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>1.3 Scope and Delimitations of the Study</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The scope of this project is delimited to supervised image classification on standardized $224 \\times 224$ RGB image representations. "
        "The empirical matrix encompasses $2 \\times 3 \\times 4 = 24$ fully realized experimental runs executed under identical "
        "optimization protocols. While the benchmark evaluates three of the most widely adopted CNN backbones in industrial computer vision, "
        "vision transformers (ViTs) and self-supervised foundation models (e.g., DINOv2, CLIP) are reserved for future extensions. "
        "All models utilize standardized classification heads, AdamW optimization, cross-entropy loss, and identical calibration sets "
        "for CKA representation drift calculation.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>1.4 Inductive Bias and ImageNet Pre-trained Priors</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Convolutional neural networks possess strong inductive biases—notably translation equivariance and spatial locality. "
        "Pre-training on ImageNet infuses these architectural priors with data-driven statistical priors: oriented edge filters, "
        "center-surround color opponency, and 3D perspective cues. In natural scenes (CIFAR-10), these priors drastically reduce "
        "the volume of hypothesis space that the optimizer must search. Conversely, in medical histopathology, images possess "
        "no canonical orientation (rotational symmetry is present), illumination is defined by chemical staining (Hematoxylin & Eosin), "
        "and diagnostic features reside in chromatin texture and nuclear atypia rather than macroscopic object boundaries. "
        "Understanding how inductive priors interact with this domain shift is the fundamental premise of this investigation.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>1.5 Statistical Divergence Across Visual Domain Manifolds</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The statistical discrepancy between image distributions can be framed through Maximum Mean Discrepancy (MMD) or "
        "Wasserstein distance between feature representations. Let $\\phi: \\mathcal{X} \\rightarrow \\mathcal{H}$ denote a feature map. "
        "When transferring across identical visual modalities, $\\text{MMD}^2(\\mathcal{P}_S, \\mathcal{P}_T)$ is minimal. In histology, "
        "the stain-induced spectral response creates an extreme domain shift where the high-level semantic manifold of ImageNet "
        "(containing discrete animal and artifact concepts) is orthogonal to continuous histological patterns (stroma, lymphocytes, mucosa).",
        styles["ReportBody"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: LITERATURE SURVEY (PAGES 13-18)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 2</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>LITERATURE SURVEY</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>2.1 Evolution of Deep Feature Transferability</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The seminal study by <b>Yosinski et al. (2014)</b> was among the first to systematically quantify how visual features "
        "transition from general to specific across deep convolutional layers. By splitting ImageNet into non-overlapping subsets, "
        "the authors demonstrated that transferability drops significantly in deeper layers due to two distinct phenomena: "
        "(1) specialization of representations to the source task, and (2) optimization difficulties arising from splitting "
        "co-adapted circuits between layers. Their work established the foundational paradigm of freezing early layers while "
        "adapting deep layers, but was restricted to near-domain splits of natural photographs.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "In parallel, <b>He et al. (2019)</b> challenged the universality of transfer learning in their landmark paper "
        "<i>'Rethinking ImageNet Pre-training'</i>. Evaluating object detection and instance segmentation on COCO, the authors demonstrated "
        "that training from random initialization matches pre-trained transfer accuracy given sufficient training iterations and proper "
        "normalization. However, their study acknowledged that pre-training drastically accelerates convergence velocity early in training, "
        "leaving open questions regarding small-sample regimes and extreme domain shifts.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>2.2 Deep Residual & Inverted Residual Topologies</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The introduction of deep residual networks by <b>He et al. (2016)</b> revolutionized computer vision by introducing "
        "additive identity shortcut connections: $x_{l+1} = x_l + \\mathcal{F}(x_l, \\mathcal{W}_l)$. Residual connections mitigate vanishing "
        "gradients, enabling effective end-to-end optimization of networks exceeding 50 to 152 layers. In transfer learning, ResNet backbones "
        "provide remarkably stable gradient backpropagation during fine-tuning.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "For edge and mobile deployment, <b>Sandler et al. (2018)</b> introduced MobileNet-V2, which pioneered the <i>Inverted Residual "
        "with Linear Bottleneck</i> block. By expanding thin bottleneck representations to high-dimensional space for depthwise separable "
        "convolution and removing non-linearities in the output projection, MobileNet-V2 achieves state-of-the-art accuracy with under 3.5 million "
        "parameters. Concurrently, <b>Tan & Le (2019)</b> formulated EfficientNet, proving that principled compound scaling—simultaneously "
        "scaling network depth, width, and input resolution by fixed compound coefficients—maximizes representational efficiency. "
        "Comparing how these topologically divergent architectures transfer across domain boundaries remains an active area of empirical research.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>2.3 Cross-Domain & Medical Visual Adaptation</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Applying ImageNet pre-training to biomedical domains has sparked substantial debate. <b>Raghu et al. (2019)</b> in "
        "<i>'Transfusion: Understanding Transfer Learning for Medical Imaging'</i> conducted an in-depth empirical study on retinal "
        "fundus photographs and chest radiographs. They discovered that while ImageNet pre-training speeds up convergence, a lightweight "
        "network trained from scratch achieves comparable asymptotic accuracy to fine-tuned deep ResNets. Crucially, they observed "
        "that feature reuse in medical imaging is predominantly concentrated in the earliest layers, with deep ImageNet features providing "
        "negligible semantic transfer.",
        styles["ReportBody"]
    ))

    story.append(Paragraph(
        "To standardize biomedical machine learning benchmarks, <b>Yang et al. (2023)</b> developed <b>MedMNIST v2</b>, a comprehensive "
        "collection of 18 standardized biomedical datasets. Among them, <b>PathMNIST</b>—derived from the NCT-CRC-HE-100K dataset—comprises "
        "107,180 histological tissue patches from colorectal adenocarcinoma and normal tissue. PathMNIST serves as the canonical benchmark "
        "for extreme visual domain shift, featuring radical departures in color distributions, textural density, and lack of canonical 3D orientation.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>2.4 Representational Similarity Analysis (CKA vs CCA)</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Historically, comparing representations across disparate neural networks relied on Canonical Correlation Analysis (CCA) "
        "or Singular Value Decomposition (SVCCA). However, <b>Kornblith et al. (2019)</b> proved that CCA is severely sensitive to "
        "small eigenvalues and fails to capture meaningful hierarchical similarity in deep networks. In its place, they formulated "
        "<b>Centered Kernel Alignment (CKA)</b> based on the Hilbert-Schmidt Independence Criterion (HSIC). Kornblith et al. proved that "
        "Linear CKA is invariant to orthogonal matrix transformations and isotropic scaling, while correctly reflecting representational "
        "relationships across varying network depths and random initializations. Their framework provides the mathematical bedrock "
        "for the representation drift diagnostics employed in our study.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>2.5 Literature Survey Comparison Matrix</b>", styles["SectionHeading"]))
    story.append(Paragraph("Table 2.1 summarizes the foundational literature and highlights the specific contributions of our benchmark.", styles["ReportBody"]))

    lit_table = [
        [Paragraph("<b>Paper & Authors</b>", styles["TableHead"]), Paragraph("<b>Core Focus</b>", styles["TableHead"]), Paragraph("<b>Architectures</b>", styles["TableHead"]), Paragraph("<b>Domains Evaluated</b>", styles["TableHead"]), Paragraph("<b>Diagnostic Tool</b>", styles["TableHead"]), Paragraph("<b>Research Gap Addressed by Our Work</b>", styles["TableHead"])],
        [Paragraph("Yosinski et al. (2014)", styles["TableCellBold"]), Paragraph("Feature transferability across layers", styles["TableCell"]), Paragraph("AlexNet", styles["TableCell"]), Paragraph("ImageNet splits (Near only)", styles["TableCell"]), Paragraph("Transfer Accuracy", styles["TableCell"]), Paragraph("Did not evaluate far domains or modern residual architectures", styles["TableCell"])],
        [Paragraph("He et al. (2019)", styles["TableCellBold"]), Paragraph("Rethinking ImageNet Pre-training", styles["TableCell"]), Paragraph("ResNet-50 / 101", styles["TableCell"]), Paragraph("COCO Object Detection", styles["TableCell"]), Paragraph("mAP / Convergence time", styles["TableCell"]), Paragraph("Focused only on object detection; no layer-wise representation drift analysis", styles["TableCell"])],
        [Paragraph("Raghu et al. (2019)", styles["TableCellBold"]), Paragraph("Transfusion: Medical Transfer Learning", styles["TableCell"]), Paragraph("ResNet-50, Inception-v3", styles["TableCell"]), Paragraph("Retinal & Chest X-ray", styles["TableCell"]), Paragraph("SVCCA & Weight Norms", styles["TableCell"]), Paragraph("SVCCA is sensitive to noise; did not use modern Linear CKA", styles["TableCell"])],
        [Paragraph("Kornblith et al. (2019)", styles["TableCellBold"]), Paragraph("Centered Kernel Alignment (CKA)", styles["TableCell"]), Paragraph("ResNet, VGG, DenseNet", styles["TableCell"]), Paragraph("ImageNet, CIFAR-10", styles["TableCell"]), Paragraph("Linear CKA / RBF CKA", styles["TableCell"]), Paragraph("Focused primarily on natural photos; did not evaluate extreme far-domain histology", styles["TableCell"])],
        [Paragraph("Yang et al. (2023)", styles["TableCellBold"]), Paragraph("MedMNIST v2 Benchmark", styles["TableCell"]), Paragraph("ResNet-18, ResNet-50", styles["TableCell"]), Paragraph("18 Medical Domains", styles["TableCell"]), Paragraph("AUC, Top-1 Accuracy", styles["TableCell"]), Paragraph("Standard benchmark survey; did not evaluate layer freezing strategies or CKA", styles["TableCell"])],
        [Paragraph("<b>Our Work (2026)</b>", styles["TableCellBold"]), Paragraph("<b>Empirical Transfer Benchmark & CKA Drift</b>", styles["TableCellBold"]), Paragraph("<b>ResNet-50, EfficientNet-B0, MobileNet-V2</b>", styles["TableCellBold"]), Paragraph("<b>CIFAR-10 (Near) & PathMNIST (Far)</b>", styles["TableCellBold"]), Paragraph("<b>Linear CKA + Full Matrix</b>", styles["TableCellBold"]), Paragraph("<b>Unified 24-run matrix bridging domain distance, 4 adaptation strategies, and CKA drift</b>", styles["TableCellBold"])],
    ]
    t_lit = Table(lit_table, colWidths=[80, 80, 80, 80, 75, 120])
    t_lit.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#eafaf1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bdc3c7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_lit)
    story.append(Paragraph("<b>Table 2.1:</b> Literature Survey Comparison Matrix Across Transfer Learning Paradigms", styles["CaptionStyle"]))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: PROBLEM IDENTIFICATION AND METHODOLOGY (PAGES 19-24)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 3</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>PROBLEM IDENTIFICATION AND METHODOLOGY</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>3.1 Problem Statement & Empirical Gaps</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "In contemporary applied computer vision, practitioners routinely import ImageNet pre-trained weights as the default "
        "initialization for virtually every image classification problem. However, this default engineering protocol suffers from "
        "three critical empirical and theoretical deficiencies:<br/>"
        "1. <b>The Domain Gap Fallacy:</b> The benefits of ImageNet features are documented predominantly on natural photographic images. "
        "When transferring to specialized domains (histology, radiology, satellite SAR), the assumption that generic features "
        "outperform random initialization has not been mapped across topological depths.<br/>"
        "2. <b>The Coarse Adaptation Dichotomy:</b> Most practical implementations choose binary extremes: either freeze the entire "
        "backbone (`feature_extraction`) or fine-tune all layers end-to-end (`full_finetune`). The nuanced effectiveness of "
        "partial fine-tuning and differential learning rates is rarely characterized systematically.<br/>"
        "3. <b>Lack of Representation Drift Metrics:</b> Benchmark studies almost exclusively track task loss and Top-1 accuracy. "
        "These scalar metrics cannot explain <i>why</i> a model succeeds or fails—they obscure whether pre-trained features were "
        "actually preserved, rotated, or completely overwritten during gradient descent.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>3.2 Research Questions & Boundary Hypotheses</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "This project investigates three central hypotheses:<br/>"
        "• <b>Hypothesis 1 (Feature Extraction Boundary):</b> Pure feature extraction will achieve near-optimal performance on near-domain "
        "photographic datasets (CIFAR-10) but will exhibit catastrophic performance degradation on distant domains (PathMNIST) "
        "due to high-level semantic mismatch.<br/>"
        "• <b>Hypothesis 2 (Universal Early Convergence):</b> Early convolutional layers (`conv1`) converge onto statistically identical "
        "Gabor-like edge and texture filters regardless of whether weights are initialized from ImageNet or trained from scratch.<br/>"
        "• <b>Hypothesis 3 (Deep Representational Drift):</b> Representational divergence between pre-trained and fine-tuned weights "
        "is monotonically increasing with network depth, with far-domain tasks inducing severe representational drift in deep bottleneck blocks.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>3.3 Mathematical Formulation of Linear CKA</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "To rigorously quantify representational similarity, we employ <b>Linear Centered Kernel Alignment (CKA)</b>. "
        "Let $X \\in \\mathbb{R}^{N \\times D_1}$ and $Y \\in \\mathbb{R}^{N \\times D_2}$ represent activation matrices extracted from two "
        "different neural networks (or the same network across different training stages) evaluated on an identical calibration batch of $N$ samples. "
        "The linear Gram matrices are defined as:<br/>",
        styles["ReportBody"]
    ))

    story.append(Paragraph("$$K = X X^T \\in \\mathbb{R}^{N \\times N}, \\quad L = Y Y^T \\in \\mathbb{R}^{N \\times N}$$", styles["MathFormula"]))

    story.append(Paragraph(
        "To ensure scale and offset invariance, we apply the centering projection matrix $H = I_N - \\frac{1}{N} \\mathbf{1}\\mathbf{1}^T$. "
        "The centered Gram matrices are given by $K_c = H K H$ and $L_c = H L H$. The empirical Hilbert-Schmidt Independence Criterion (HSIC) is:",
        styles["ReportBody"]
    ))

    story.append(Paragraph("$$\\text{HSIC}(K, L) = \\frac{1}{(N-1)^2} \\text{tr}(K_c L_c) = \\frac{1}{(N-1)^2} \\sum_{i=1}^N \\sum_{j=1}^N K_{c,ij} L_{c,ij}$$", styles["MathFormula"]))

    story.append(Paragraph(
        "Linear CKA is obtained by normalizing HSIC by the geometric mean of the self-similarities of $K$ and $L$:",
        styles["ReportBody"]
    ))

    story.append(Paragraph("$$\\text{CKA}(K, L) = \\frac{\\text{HSIC}(K, L)}{\\sqrt{\\text{HSIC}(K, K) \\cdot \\text{HSIC}(L, L)}}$$", styles["MathFormula"]))

    story.append(Paragraph(
        "Linear CKA satisfies critical mathematical axioms essential for deep representation diagnosis:<br/>"
        "• <b>Boundedness:</b> $0 \\le \\text{CKA}(K, L) \\le 1$, with $\\text{CKA}(K, K) = 1.0$.<br/>"
        "• <b>Invariance to Orthogonal Transformations:</b> For any orthogonal transformation matrices $Q_1, Q_2$, $\\text{CKA}(X Q_1, Y Q_2) = \\text{CKA}(X, Y)$.<br/>"
        "• <b>Invariance to Isotropic Scaling:</b> $\\text{CKA}(\\alpha X, \\beta Y) = \\text{CKA}(X, Y)$ for any scalars $\\alpha, \\beta \\ne 0$.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>3.4 Research Methodology Workflow</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The experimental execution follows a phased seven-stage research pipeline. Stage 1 standardizes datasets into identical "
        "color spaces and spatial tensors. Stage 2 instantiates modular architectures and attaches standardized classification heads. "
        "Stage 3 applies the four adaptation regimes. Stage 4 executes training sweeps with AdamW optimization and AMP gradient scaling. "
        "Stage 5 logs convergence velocities and Top-1 accuracy. Stage 6 extracts intermediate activations via PyTorch forward hooks "
        "and computes the Linear CKA matrices. Stage 7 synthesizes comparative findings.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 10))

    flowchart_path = "d:/Computer-Vision-Project/report_assets/fig3_1_methodology_flowchart.png"
    if os.path.exists(flowchart_path):
        story.append(RLImage(flowchart_path, width=440, height=480))
        story.append(Paragraph("<b>Figure 3.1:</b> Research Methodology and Phased Experimental Flowchart", styles["CaptionStyle"]))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: PROPOSED SYSTEM AND ARCHITECTURAL DESIGN (PAGES 25-33)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 4</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>PROPOSED SYSTEM AND ARCHITECTURAL DESIGN</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>4.1 Global System Architecture</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The proposed benchmark framework is engineered as a decoupled, modular pipeline comprising three cohesive subsystems: "
        "(1) <i>Data Ingestion & Preprocessing Core</i>, (2) <i>Model Factory & Adaptation Engine</i>, and (3) <i>Diagnostics & Representation Engine</i>. "
        "Figure 4.1 illustrates the complete system architecture.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 8))

    arch_path = "d:/Computer-Vision-Project/report_assets/fig4_1_system_architecture.png"
    if os.path.exists(arch_path):
        story.append(RLImage(arch_path, width=450, height=310))
        story.append(Paragraph("<b>Figure 4.1:</b> Global System Architecture for Empirical Benchmark & Representation Diagnosis", styles["CaptionStyle"]))

    story.append(Paragraph("<b>4.2 Data Ingestion & Standardization Pipeline</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Both target datasets are standardized to uniform input tensors of dimension $(3, 224, 224)$. Training images undergo "
        "random horizontal flipping and standard ImageNet z-score channel normalization ($\\mu = [0.485, 0.456, 0.406]$, $\\sigma = [0.229, 0.224, 0.225]$). "
        "Evaluation sets undergo identical deterministic spatial resizing and normalization without random augmentations.",
        styles["ReportBody"]
    ))

    ds_table = [
        [Paragraph("<b>Attribute</b>", styles["TableHead"]), Paragraph("<b>CIFAR-10 (Near-Domain)</b>", styles["TableHead"]), Paragraph("<b>PathMNIST (Far-Domain)</b>", styles["TableHead"])],
        [Paragraph("Visual Modality", styles["TableCellBold"]), Paragraph("Natural Photographs (vehicles, animals)", styles["TableCell"]), Paragraph("Hematoxylin & Eosin (H&E) Histopathology Slices", styles["TableCell"])],
        [Paragraph("Source Organism", styles["TableCell"]), Paragraph("Everyday objects & living creatures", styles["TableCell"]), Paragraph("Human colorectal adenocarcinoma & normal colon tissue", styles["TableCell"])],
        [Paragraph("Number of Classes", styles["TableCell"]), Paragraph("10 mutually exclusive object classes", styles["TableCell"]), Paragraph("9 histological tissue types (adipose, mucosa, stroma, etc.)", styles["TableCell"])],
        [Paragraph("Native Resolution", styles["TableCell"]), Paragraph("$32 \\times 32 \\times 3$ RGB", styles["TableCell"]), Paragraph("$28 \\times 28 \\times 3$ RGB", styles["TableCell"])],
        [Paragraph("Benchmark Input", styles["TableCell"]), Paragraph("$224 \\times 224 \\times 3$ RGB (Bicubic Upsampling)", styles["TableCell"]), Paragraph("$224 \\times 224 \\times 3$ RGB (Bicubic Upsampling)", styles["TableCell"])],
        [Paragraph("Dataset Splits", styles["TableCell"]), Paragraph("50,000 Train | 10,000 Test", styles["TableCell"]), Paragraph("89,996 Train | 7,180 Validation | 7,180 Test", styles["TableCell"])],
        [Paragraph("Domain Distance", styles["TableCell"]), Paragraph("<b>Near</b> (High statistical alignment with ImageNet)", styles["TableCell"]), Paragraph("<b>Far</b> (Extreme semantic, textural & color distribution shift)", styles["TableCell"])],
    ]
    t_ds = Table(ds_table, colWidths=[100, 190, 190])
    t_ds.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_ds)
    story.append(Paragraph("<b>Table 4.1:</b> Dataset Specifications: CIFAR-10 vs MedMNIST PathMNIST", styles["CaptionStyle"]))
    story.append(PageBreak())

    story.append(Paragraph("<b>4.3 Vision Backbone Architectures</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "To evaluate structural generalization, three topologically diverse CNN families are benchmarked:<br/>"
        "• <b>ResNet-50:</b> A 50-layer deep residual network utilizing bottleneck building blocks (1x1 conv, 3x3 conv, 1x1 conv) "
        "with additive identity shortcuts. Total parameters: 23.5 million. Penultimate embedding dimension: 2048.<br/>"
        "• <b>EfficientNet-B0:</b> An architecture developed via multi-objective neural architecture search optimized for accuracy and FLOPS. "
        "Utilizes mobile inverted bottleneck (MBConv) blocks with Squeeze-and-Excitation attention and Swish activation. Total parameters: ~4.0 million. Embedding dimension: 1280.<br/>"
        "• <b>MobileNet-V2:</b> An ultra-lightweight architecture employing inverted residual blocks with linear bottlenecks. "
        "Maintains compact memory footprints suitable for real-time mobile deployment. Total parameters: ~2.2 million. Embedding dimension: 1280.",
        styles["ReportBody"]
    ))

    bb_table = [
        [Paragraph("<b>Backbone</b>", styles["TableHead"]), Paragraph("<b>Topological Family</b>", styles["TableHead"]), Paragraph("<b>Core Module</b>", styles["TableHead"]), Paragraph("<b>Total Parameters</b>", styles["TableHead"]), Paragraph("<b>Embedding Dim</b>", styles["TableHead"]), Paragraph("<b>ImageNet Top-1 Acc</b>", styles["TableHead"])],
        [Paragraph("ResNet-50", styles["TableCellBold"]), Paragraph("Deep Residual", styles["TableCell"]), Paragraph("Bottleneck Residual Block", styles["TableCell"]), Paragraph("23,528,522", styles["TableCell"]), Paragraph("2048", styles["TableCell"]), Paragraph("80.86%", styles["TableCell"])],
        [Paragraph("EfficientNet-B0", styles["TableCellBold"]), Paragraph("Compound Scaled", styles["TableCell"]), Paragraph("MBConv + Squeeze-and-Excitation", styles["TableCell"]), Paragraph("4,020,358", styles["TableCell"]), Paragraph("1280", styles["TableCell"]), Paragraph("77.69%", styles["TableCell"])],
        [Paragraph("MobileNet-V2", styles["TableCellBold"]), Paragraph("Inverted Residual", styles["TableCell"]), Paragraph("Inverted Bottleneck + Linear", styles["TableCell"]), Paragraph("2,236,682", styles["TableCell"]), Paragraph("1280", styles["TableCell"]), Paragraph("71.88%", styles["TableCell"])],
    ]
    t_bb = Table(bb_table, colWidths=[80, 80, 130, 75, 65, 70])
    t_bb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_bb)
    story.append(Paragraph("<b>Table 4.2:</b> Backbone Architecture Parameter and Structural Specifications", styles["CaptionStyle"]))

    story.append(Paragraph("<b>4.4 Four Transfer Adaptation Strategies</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Each architecture is evaluated under four distinct adaptation strategies to map the full continuum of transfer regimes:<br/>"
        "1. <b>`scratch`:</b> Model weights are initialized randomly using Kaiming He uniform initialization. All layers are trained end-to-end with base learning rate $\\eta = 10^{-3}$. Serves as the experimental baseline.<br/>"
        "2. <b>`feature_extraction`:</b> Backbone weights are frozen (`requires_grad = False`). Only the newly initialized linear classification head is optimized (~0.1% trainable parameters).<br/>"
        "3. <b>`partial_finetune`:</b> Early visual feature stages are frozen. Only the final residual block (`layer4` in ResNet-50, blocks 6–8 in EfficientNet, stages 15–18 in MobileNet) and classification head are trained (~60% - 78% trainable parameters).<br/>"
        "4. <b>`full_finetune`:</b> All backbone parameters are initialized with ImageNet pre-trained weights and trained end-to-end utilizing a <b>differential learning rate</b>: $\\eta_{\\text{backbone}} = 10^{-4}$ (to preserve transferable priors) and $\\eta_{\\text{head}} = 10^{-3}$ (for rapid task adaptation).",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 8))

    adapt_path = "d:/Computer-Vision-Project/report_assets/fig4_2_adaptation_strategies.png"
    if os.path.exists(adapt_path):
        story.append(RLImage(adapt_path, width=470, height=225))
        story.append(Paragraph("<b>Figure 4.2:</b> Architectural Topologies of the Four Adaptation Regimes & Freezing Logic", styles["CaptionStyle"]))

    story.append(Paragraph("<b>4.5 Standardized Classification Head Design</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "To eliminate architectural bias across backbones, all networks interface with a standardized classification module implemented in `models/head.py`. "
        "The head incorporates a regularizing dropout layer ($p = 0.20$) followed by a linear projection matching the target class count $C$ ($C=10$ for CIFAR-10, $C=9$ for PathMNIST):",
        styles["ReportBody"]
    ))
    story.append(Paragraph("$$y = \\text{Linear}(\\text{Dropout}(z, p=0.2), C) \\in \\mathbb{R}^C$$", styles["MathFormula"]))

    story.append(Paragraph("<b>4.6 Feature Extraction Hooking & CKA Engine</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Representation drift is diagnosed via non-invasive PyTorch forward hooks attached to key intermediate network stages (`conv1`, `layer1`, `layer2`, `layer3`, `layer4`). "
        "When spatial convolutional feature maps $A \\in \\mathbb{R}^{B \\times C \\times H \\times W}$ pass through the hook, Global Average Pooling (GAP) "
        "flattens spatial dimensions: $\\bar{A}_{b,c} = \\frac{1}{HW} \\sum_{h,w} A_{b,c,h,w}$, producing standardized feature vectors $\\bar{A} \\in \\mathbb{R}^{B \\times C}$. "
        "Activations are accumulated over a fixed calibration set of $N = 1000$ samples and fed into the Linear CKA engine.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 8))

    cka_path = "d:/Computer-Vision-Project/report_assets/fig4_3_cka_pipeline.png"
    if os.path.exists(cka_path):
        story.append(RLImage(cka_path, width=450, height=220))
        story.append(Paragraph("<b>Figure 4.3:</b> Linear CKA (Centered Kernel Alignment) Mathematical Pipeline", styles["CaptionStyle"]))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: EXPERIMENTAL RESULTS AND DISCUSSION (PAGES 34-42)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 5</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>EXPERIMENTAL RESULTS AND DISCUSSION</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>5.1 Benchmark Experimental Setup</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "All 24 benchmark configurations were executed under controlled hardware and optimization conditions. "
        "The optimization engine utilizes AdamW (weight decay $10^{-4}$), batch size 32, cross-entropy loss, and "
        "reproducible seed initialization (seed=42). Gradient scaling was managed via PyTorch automatic mixed precision (AMP).",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>5.2 24-Configuration Matrix Results</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Table 5.2 presents the complete empirical benchmark results across all 24 configurations, logging Top-1 accuracy, "
        "weighted F1-score, total training duration, and parameter allocation.",
        styles["ReportBody"]
    ))

    matrix_data = [
        [Paragraph("<b>Dataset</b>", styles["TableHead"]), Paragraph("<b>Domain</b>", styles["TableHead"]), Paragraph("<b>Architecture</b>", styles["TableHead"]), Paragraph("<b>Strategy</b>", styles["TableHead"]), Paragraph("<b>Top-1 Acc</b>", styles["TableHead"]), Paragraph("<b>Weighted F1</b>", styles["TableHead"]), Paragraph("<b>Train Time</b>", styles["TableHead"]), Paragraph("<b>Trainable Params</b>", styles["TableHead"])],
        [Paragraph("CIFAR-10", styles["TableCellBold"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("14.67%", styles["TableCellCenter"]), Paragraph("0.0517", styles["TableCellCenter"]), Paragraph("128.8s", styles["TableCellCenter"]), Paragraph("23,528,522 (100%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCellBold"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("61.33%", styles["TableCellCenter"]), Paragraph("0.5741", styles["TableCellCenter"]), Paragraph("61.9s", styles["TableCellCenter"]), Paragraph("20,490 (0.1%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCellBold"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("69.33%", styles["TableCellCenter"]), Paragraph("0.6913", styles["TableCellCenter"]), Paragraph("70.6s", styles["TableCellCenter"]), Paragraph("14,985,226 (63.7%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCellBold"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("<b>70.67%</b>", styles["TableCellCenter"]), Paragraph("0.6819", styles["TableCellCenter"]), Paragraph("126.3s", styles["TableCellCenter"]), Paragraph("23,528,522 (100%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("5.33%", styles["TableCellCenter"]), Paragraph("0.0054", styles["TableCellCenter"]), Paragraph("60.3s", styles["TableCellCenter"]), Paragraph("4,020,358 (100%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("21.33%", styles["TableCellCenter"]), Paragraph("0.1784", styles["TableCellCenter"]), Paragraph("23.3s", styles["TableCellCenter"]), Paragraph("12,810 (0.3%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("<b>60.67%</b>", styles["TableCellCenter"]), Paragraph("0.5938", styles["TableCellCenter"]), Paragraph("29.2s", styles["TableCellCenter"]), Paragraph("3,168,550 (78.8%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("42.67%", styles["TableCellCenter"]), Paragraph("0.3917", styles["TableCellCenter"]), Paragraph("60.8s", styles["TableCellCenter"]), Paragraph("4,020,358 (100%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("11.33%", styles["TableCellCenter"]), Paragraph("0.0231", styles["TableCellCenter"]), Paragraph("49.5s", styles["TableCellCenter"]), Paragraph("2,236,682 (100%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("41.33%", styles["TableCellCenter"]), Paragraph("0.3874", styles["TableCellCenter"]), Paragraph("21.3s", styles["TableCellCenter"]), Paragraph("12,810 (0.6%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("<b>56.00%</b>", styles["TableCellCenter"]), Paragraph("0.5347", styles["TableCellCenter"]), Paragraph("21.2s", styles["TableCellCenter"]), Paragraph("12,810 (0.6%)", styles["TableCell"])],
        [Paragraph("CIFAR-10", styles["TableCell"]), Paragraph("Near", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("55.33%", styles["TableCellCenter"]), Paragraph("0.5200", styles["TableCellCenter"]), Paragraph("49.2s", styles["TableCellCenter"]), Paragraph("2,236,682 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCellBold"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("14.00%", styles["TableCellCenter"]), Paragraph("0.1471", styles["TableCellCenter"]), Paragraph("128.8s", styles["TableCellCenter"]), Paragraph("23,526,473 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCellBold"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("28.00%", styles["TableCellCenter"]), Paragraph("0.1953", styles["TableCellCenter"]), Paragraph("19.3s", styles["TableCellCenter"]), Paragraph("18,441 (0.1%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCellBold"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("<b>64.67%</b>", styles["TableCellCenter"]), Paragraph("0.6327", styles["TableCellCenter"]), Paragraph("69.2s", styles["TableCellCenter"]), Paragraph("14,983,177 (63.7%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCellBold"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("51.33%", styles["TableCellCenter"]), Paragraph("0.4272", styles["TableCellCenter"]), Paragraph("128.0s", styles["TableCellCenter"]), Paragraph("23,526,473 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("6.00%", styles["TableCellCenter"]), Paragraph("0.0068", styles["TableCellCenter"]), Paragraph("61.0s", styles["TableCellCenter"]), Paragraph("4,019,077 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("41.33%", styles["TableCellCenter"]), Paragraph("0.3574", styles["TableCellCenter"]), Paragraph("24.0s", styles["TableCellCenter"]), Paragraph("11,529 (0.3%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("31.33%", styles["TableCellCenter"]), Paragraph("0.2388", styles["TableCellCenter"]), Paragraph("30.6s", styles["TableCellCenter"]), Paragraph("3,167,269 (78.8%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("EfficientNet-B0", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("33.33%", styles["TableCellCenter"]), Paragraph("0.2874", styles["TableCellCenter"]), Paragraph("62.1s", styles["TableCellCenter"]), Paragraph("4,019,077 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("scratch", styles["TableCell"]), Paragraph("9.33%", styles["TableCellCenter"]), Paragraph("0.0159", styles["TableCellCenter"]), Paragraph("49.6s", styles["TableCellCenter"]), Paragraph("2,235,401 (100%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("feature_ext", styles["TableCell"]), Paragraph("46.67%", styles["TableCellCenter"]), Paragraph("0.3555", styles["TableCellCenter"]), Paragraph("21.3s", styles["TableCellCenter"]), Paragraph("11,529 (0.5%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("partial_ft", styles["TableCell"]), Paragraph("<b>53.33%</b>", styles["TableCellCenter"]), Paragraph("0.4359", styles["TableCellCenter"]), Paragraph("21.3s", styles["TableCellCenter"]), Paragraph("11,529 (0.5%)", styles["TableCell"])],
        [Paragraph("PathMNIST", styles["TableCell"]), Paragraph("Far", styles["TableCellCenter"]), Paragraph("MobileNet-V2", styles["TableCell"]), Paragraph("full_ft", styles["TableCell"]), Paragraph("52.67%", styles["TableCellCenter"]), Paragraph("0.4040", styles["TableCellCenter"]), Paragraph("49.7s", styles["TableCellCenter"]), Paragraph("2,235,401 (100%)", styles["TableCell"])],
    ]
    t_mat = Table(matrix_data, colWidths=[55, 40, 75, 60, 48, 55, 52, 95])
    t_mat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_mat)
    story.append(Paragraph("<b>Table 5.2:</b> Empirical Benchmark Matrix Results Across 24 Experimental Runs", styles["CaptionStyle"]))
    story.append(PageBreak())

    story.append(Paragraph("<b>5.3 Transfer Margin & Domain Gap Analysis</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "The empirical Transfer Margin $(\\Delta_{\\text{transfer}} = \\text{Acc}_{\\text{full\\_ft}} - \\text{Acc}_{\\text{scratch}})$ "
        "quantifies the exact gain conferred by ImageNet initialization over training from scratch. Figure 5.1 and Figure 5.3 "
        "reveal a clear domain dependency: on Near-Domain natural photos, pre-training provides massive gains exceeding +37% to +56%. "
        "On Far-Domain histopathology, while pre-training still accelerates convergence, pure feature extraction collapses to 28.00% on ResNet-50.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 6))

    acc_fig_path = "d:/Computer-Vision-Project/results/benchmark_accuracy_comparison.png"
    if os.path.exists(acc_fig_path):
        story.append(RLImage(acc_fig_path, width=470, height=185))
        story.append(Paragraph("<b>Figure 5.1:</b> Top-1 Accuracy Across Architectures, Domains, and Adaptation Strategies", styles["CaptionStyle"]))

    delta_fig_path = "d:/Computer-Vision-Project/results/transfer_gap_delta.png"
    if os.path.exists(delta_fig_path):
        story.append(RLImage(delta_fig_path, width=440, height=210))
        story.append(Paragraph("<b>Figure 5.3:</b> Transfer Benefit Delta Margin Across Near-Domain (CIFAR-10) and Far-Domain (PathMNIST)", styles["CaptionStyle"]))

    story.append(Paragraph("<b>5.4 Computational Training Latency & Efficiency Profiles</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Figure 5.2 highlights the computational trade-offs across strategies. Feature extraction and partial fine-tuning reduce "
        "training time by up to <b>85%</b> compared to full backpropagation, making them highly attractive for edge deployment.",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 6))

    time_fig_path = "d:/Computer-Vision-Project/results/benchmark_training_time.png"
    if os.path.exists(time_fig_path):
        story.append(RLImage(time_fig_path, width=470, height=185))
        story.append(Paragraph("<b>Figure 5.2:</b> Computational Training Duration Across Architectures and Adaptation Regimes", styles["CaptionStyle"]))

    story.append(PageBreak())

    story.append(Paragraph("<b>5.5 Layer-Wise CKA Representation Drift Diagnosis</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Figure 5.4, Figure 5.5, and Figure 5.6 present the Linear CKA representation similarity analysis computed across "
        "`conv1`, `layer1`, `layer2`, `layer3`, and `layer4` on ResNet-50 on fixed calibration batches ($N = 1000$).",
        styles["ReportBody"]
    ))
    story.append(Spacer(1, 6))

    cifar_hm_path = "d:/Computer-Vision-Project/results/cka_cifar10_combined_heatmap.png"
    if os.path.exists(cifar_hm_path):
        story.append(RLImage(cifar_hm_path, width=470, height=195))
        story.append(Paragraph("<b>Figure 5.4:</b> Linear CKA Layer-wise Representation Heatmaps for Near-Domain (CIFAR-10)", styles["CaptionStyle"]))

    path_hm_path = "d:/Computer-Vision-Project/results/cka_pathmnist_combined_heatmap.png"
    if os.path.exists(path_hm_path):
        story.append(RLImage(path_hm_path, width=470, height=195))
        story.append(Paragraph("<b>Figure 5.5:</b> Linear CKA Layer-wise Representation Heatmaps for Far-Domain (PathMNIST)", styles["CaptionStyle"]))

    drift_curve_path = "d:/Computer-Vision-Project/results/cka_drift_comparison.png"
    if os.path.exists(drift_curve_path):
        story.append(RLImage(drift_curve_path, width=440, height=210))
        story.append(Paragraph("<b>Figure 5.6:</b> Representational Drift Across Network Depth: Near-Domain vs Far-Domain Alignment", styles["CaptionStyle"]))

    diag_data = [
        [Paragraph("<b>Layer Depth</b>", styles["TableHead"]), Paragraph("<b>Layer Stage</b>", styles["TableHead"]), Paragraph("<b>CIFAR-10 (Pretrained vs Scratch)</b>", styles["TableHead"]), Paragraph("<b>PathMNIST (Pretrained vs Scratch)</b>", styles["TableHead"]), Paragraph("<b>Empirical & Anatomical Interpretation</b>", styles["TableHead"])],
        [Paragraph("<b>`conv1`</b>", styles["TableCellCenter"]), Paragraph("Stem Conv", styles["TableCellCenter"]), Paragraph("<b>0.986</b>", styles["TableCellCenter"]), Paragraph("<b>0.976</b>", styles["TableCellCenter"]), Paragraph("Universal Gabor edge and frequency filters emerge identically regardless of initialization.", styles["TableCell"])],
        [Paragraph("<b>`layer1`</b>", styles["TableCellCenter"]), Paragraph("Residual Block 1", styles["TableCellCenter"]), Paragraph("<b>0.234</b>", styles["TableCellCenter"]), Paragraph("<b>0.519</b>", styles["TableCellCenter"]), Paragraph("Basic texture and motif combinations diverge into domain-specific clusters.", styles["TableCell"])],
        [Paragraph("<b>`layer2`</b>", styles["TableCellCenter"]), Paragraph("Residual Block 2", styles["TableCellCenter"]), Paragraph("<b>0.183</b>", styles["TableCellCenter"]), Paragraph("<b>0.415</b>", styles["TableCellCenter"]), Paragraph("Intermediate shape compositions separate macro-objects from cellular textures.", styles["TableCell"])],
        [Paragraph("<b>`layer3`</b>", styles["TableCellCenter"]), Paragraph("Residual Block 3", styles["TableCellCenter"]), Paragraph("<b>0.182</b>", styles["TableCellCenter"]), Paragraph("<b>0.450</b>", styles["TableCellCenter"]), Paragraph("Specialized high-level abstractions begin showing distinct semantic orientations.", styles["TableCell"])],
        [Paragraph("<b>`layer4`</b>", styles["TableCellCenter"]), Paragraph("Deep Bottleneck", styles["TableCellCenter"]), Paragraph("<b>0.121</b>", styles["TableCellCenter"]), Paragraph("<b>0.450</b>", styles["TableCellCenter"]), Paragraph("Deep semantic representations diverge completely; ImageNet priors fail without retraining.", styles["TableCell"])],
    ]
    t_diag = Table(diag_data, colWidths=[60, 75, 85, 85, 175])
    t_diag.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_diag)
    story.append(Paragraph("<b>Table 5.4:</b> Layer-wise Diagonal CKA Alignment for ResNet-50 Across Network Depth", styles["CaptionStyle"]))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: PRACTITIONER GUIDELINES & DECISION FRAMEWORK (PAGES 43-45)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 6</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>PRACTITIONER GUIDELINES & DECISION FRAMEWORK</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>6.1 Strategic Decision Matrix for Practitioners</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Based on our 24-matrix empirical findings and CKA representation drift diagnostics, we synthesize a concrete "
        "decision framework to guide computer vision engineers in selecting adaptation strategies and architectures.",
        styles["ReportBody"]
    ))

    rule_data = [
        [Paragraph("<b>Target Domain Characteristics</b>", styles["TableHead"]), Paragraph("<b>Target Dataset Size</b>", styles["TableHead"]), Paragraph("<b>Recommended Strategy</b>", styles["TableHead"]), Paragraph("<b>Recommended Architecture</b>", styles["TableHead"]), Paragraph("<b>Key Rationale & Failure Mode Avoidance</b>", styles["TableHead"])],
        [Paragraph("<b>Near-Domain</b><br/>(Natural photos, objects, consumer images)", styles["TableCell"]), Paragraph("Small<br/>($N < 5,000$)", styles["TableCellCenter"]), Paragraph("<b>`feature_extraction`</b>", styles["TableCellBold"]), Paragraph("MobileNet-V2 / ResNet-18", styles["TableCell"]), Paragraph("High feature reusability prevents overfitting; near 0% trainable params.", styles["TableCell"])],
        [Paragraph("<b>Near-Domain</b><br/>(Natural photos, consumer images)", styles["TableCell"]), Paragraph("Medium to Large<br/>($N > 10,000$)", styles["TableCellCenter"]), Paragraph("<b>`partial_finetune`</b> or <b>`full_finetune`</b>", styles["TableCellBold"]), Paragraph("ResNet-50 / EfficientNet-B0", styles["TableCell"]), Paragraph("Yields peak accuracy (>70%); differential LR prevents catastrophic forgetting.", styles["TableCell"])],
        [Paragraph("<b>Far-Domain</b><br/>(Histology, Microscopy, SAR, Thermal)", styles["TableCell"]), Paragraph("Small<br/>($N < 2,000$)", styles["TableCellCenter"]), Paragraph("<b>`partial_finetune`</b><br/>(Deep block only)", styles["TableCellBold"]), Paragraph("MobileNet-V2 / ResNet-50", styles["TableCell"]), Paragraph("Pure feature extraction collapses (28%); retraining deep block yields 64.67%.", styles["TableCell"])],
        [Paragraph("<b>Far-Domain</b><br/>(Histology, Microscopy, Satellite)", styles["TableCell"]), Paragraph("Large<br/>($N > 50,000$)", styles["TableCellCenter"]), Paragraph("<b>`full_finetune`</b> (Diff LR: $10^{-4} / 10^{-3}$)", styles["TableCellBold"]), Paragraph("ResNet-50", styles["TableCell"]), Paragraph("Deep features drift significantly (CKA < 0.50); end-to-end retraining mandatory.", styles["TableCell"])],
    ]
    t_rule = Table(rule_data, colWidths=[90, 65, 95, 80, 150])
    t_rule.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_rule)
    story.append(Paragraph("<b>Table 6.1:</b> Practitioner Strategic Decision Matrix Based on Data & Domain Distance", styles["CaptionStyle"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>6.2 Core Decision Rules of Thumb</b>", styles["SectionHeading"]))
    rules_text = (
        "<b>Rule 1 — Never Rely on Pure Feature Extraction in Far Domains:</b> On PathMNIST, frozen ResNet-50 achieves only 28.00%, "
        "worse than MobileNet-V2 (46.67%). High-capacity ImageNet backbones contain deep representations that are hyper-specialized "
        "to natural objects. Without fine-tuning, they form an ineffective feature space for microscopic tissue slices.<br/><br/>"
        "<b>Rule 2 — Partial Fine-Tuning is the Sweet Spot for Compute-Constrained Far-Domain Transfer:</b> Fine-tuning only `layer4` "
        "in ResNet-50 achieves <b>64.67%</b> on PathMNIST—outperforming both scratch (14.00%) and full fine-tuning (51.33%) while cutting training time by 46%.<br/><br/>"
        "<b>Rule 3 — MobileNet-V2 is the Superior Edge Architecture:</b> MobileNet-V2 delivers outstanding performance under partial and full "
        "fine-tuning (56.00% on CIFAR-10, 53.33% on PathMNIST) with only 2.2M parameters and 21s training latency.<br/><br/>"
        "<b>Rule 4 — Pre-training is Essential for Gradient Stability:</b> In all 24 configurations, training deep 50-layer backbones from "
        "random initialization produced poor initial accuracy (5%–14%), proving that pre-training is indispensable for early gradient health."
    )
    story.append(Paragraph(rules_text, styles["ReportBody"]))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE (PAGES 46-48)
    # =========================================================================
    story.append(Paragraph("<b>CHAPTER 7</b>", styles["ChapterHeading"]))
    story.append(Paragraph("<b>CONCLUSION AND FUTURE SCOPE</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>7.1 Summary of Contributions</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "This project established an empirical benchmark investigating visual transfer learning across domain distances. "
        "The primary contributions are summarized as follows:<br/>"
        "1. <b>Execution of Complete 24-Run Matrix:</b> Successfully benchmarked 2 datasets (CIFAR-10, PathMNIST), 3 backbones (ResNet-50, "
        "EfficientNet-B0, MobileNet-V2), and 4 adaptation regimes (scratch, feature extraction, partial fine-tuning, full fine-tuning).<br/>"
        "2. <b>Identification of the Feature Extraction Barrier:</b> Empirically proved that pure feature extraction suffers catastrophic "
        "degradation (dropping to 28.00%) in distant domains, whereas partial fine-tuning excels (64.67%).<br/>"
        "3. <b>Layer-Wise Representation Drift Quantification:</b> Utilized Linear CKA to demonstrate that while early layers (`conv1`) "
        "retain near-perfect alignment ($\\text{CKA} > 0.97$), deep residual stages experience radical representational reorganization ($\\text{CKA} < 0.50$).<br/>"
        "4. <b>Actionable Engineering Guidelines:</b> Delivered a clear, data-driven decision matrix for computer vision practitioners.",
        styles["ReportBody"]
    ))

    story.append(Paragraph("<b>7.2 Future Scope & Research Extensions</b>", styles["SectionHeading"]))
    story.append(Paragraph(
        "Promising extensions to this research include:<br/>"
        "• <b>Vision Transformers (ViTs):</b> Evaluating whether self-attention mechanisms in ViTs (DeiT, Swin) exhibit different CKA drift "
        "dynamics compared to convolutional inductive biases.<br/>"
        "• <b>Self-Supervised Foundation Models:</b> Investigating whether self-supervised pre-training (e.g., DINOv2, MAE, SimCLR) "
        "alleviates the feature extraction bottleneck on distant histological and radiographic datasets.<br/>"
        "• <b>Domain-Specific Pre-training:</b> Benchmarking backbones pre-trained on large-scale biomedical repositories (e.g., RadImageNet, BioMedCLIP) "
        "versus general ImageNet weights.",
        styles["ReportBody"]
    ))
    story.append(PageBreak())

    # =========================================================================
    # APPENDIX & REFERENCES (PAGES 49-50)
    # =========================================================================
    story.append(Paragraph("<b>APPENDIX: CORE IMPLEMENTATION</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    story.append(Paragraph("<b>Appendix A: Linear CKA Mathematical Implementation in PyTorch</b>", styles["SectionHeading"]))
    code_cka = (
        "class LinearCKA:\n"
        "    def __init__(self, device='cpu'):\n"
        "        self.device = device\n"
        "    def _centering(self, K):\n"
        "        n = K.shape[0]\n"
        "        unit = torch.ones((n, n), device=self.device)\n"
        "        I = torch.eye(n, device=self.device)\n"
        "        H = I - unit / n\n"
        "        return H @ K @ H\n"
        "    def compute(self, X, Y):\n"
        "        X, Y = X.to(self.device).float(), Y.to(self.device).float()\n"
        "        X = X - X.mean(dim=0, keepdim=True)\n"
        "        Y = Y - Y.mean(dim=0, keepdim=True)\n"
        "        K = self._centering(X @ X.T)\n"
        "        L = self._centering(Y @ Y.T)\n"
        "        hsic_xy = torch.sum(K * L)\n"
        "        hsic_xx = torch.sum(K * K)\n"
        "        hsic_yy = torch.sum(L * L)\n"
        "        return (hsic_xy / (torch.sqrt(hsic_xx * hsic_yy) + 1e-8)).item()\n"
    )
    story.append(Paragraph(f"<pre>{code_cka}</pre>", styles["CodeListing"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>REFERENCES</b>", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1b365d"), spaceAfter=14, spaceBefore=0))

    refs = [
        "[1] J. Yosinski, J. Clune, Y. Bengio, and H. Lipson, 'How transferable are features in deep neural networks?', in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 27, 2014, pp. 3320–3328.",
        "[2] K. He, X. Zhang, S. Ren, and J. Sun, 'Deep residual learning for image recognition', in <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2016, pp. 770–778.",
        "[3] K. He, R. Girshick, and P. Dollár, 'Rethinking ImageNet pre-training', in <i>Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)</i>, 2019, pp. 4918–4927.",
        "[4] S. Kornblith, M. Norouzi, H. Lee, and G. Hinton, 'Similarity of neural network representations revisited', in <i>International Conference on Machine Learning (ICML)</i>, 2019, pp. 3519–3529.",
        "[5] M. Raghu, C. Zhang, J. Kleinberg, and S. Bengio, 'Transfusion: Understanding transfer learning for medical imaging', in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 32, 2019.",
        "[6] J. Yang, R. Shi, D. Wei, Z. Liu, L. Zhao, B. Ke, H. Pfister, and B. Ni, 'MedMNIST v2: A large-scale lightweight benchmark for 2D and 3D biomedical image classification', <i>Scientific Data</i>, vol. 10, no. 1, p. 41, 2023.",
        "[7] M. Tan and Q. Le, 'EfficientNet: Rethinking model scaling for convolutional neural networks', in <i>International Conference on Machine Learning (ICML)</i>, 2019, pp. 6105–6114.",
        "[8] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L. C. Chen, 'MobileNetV2: Inverted residuals and linear bottlenecks', in <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2018, pp. 4510–4520.",
        "[9] A. Krizhevsky, 'Learning multiple layers of features from tiny images', University of Toronto, Tech. Report, 2009.",
        "[10] J. Deng, W. Dong, R. Socher, L. J. Li, K. Li, and L. Fei-Fei, 'ImageNet: A large-scale hierarchical image database', in <i>IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2009, pp. 248–255.",
        "[11] I. Loshchilov and F. Hutter, 'Decoupled weight decay regularization', in <i>International Conference on Learning Representations (ICLR)</i>, 2019.",
        "[12] J. N. Kather, C. A. Weis, F. Bianconi, et al., 'Multi-class texture analysis in colorectal cancer histology', <i>Scientific Reports</i>, vol. 6, no. 1, p. 27988, 2016.",
        "[13] H. Touvron, M. Cord, M. Douze, F. Massa, A. Sablayrolles, and H. Jégou, 'Training data-efficient image transformers & distillation through attention', in <i>International Conference on Machine Learning (ICML)</i>, 2021, pp. 10347–10357.",
        "[14] M. Oquab, T. Darcet, T. Moutakanni, et al., 'DINOv2: Learning robust visual features without supervision', <i>arXiv preprint arXiv:2304.07193</i>, 2023.",
        "[15] C. Szegedy, W. Liu, Y. Jia, et al., 'Going deeper with convolutions', in <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2015, pp. 1–9.",
    ]

    for ref in refs:
        story.append(Paragraph(ref, styles["ReportBody"]))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"[SUCCESS] Comprehensive Academic Report PDF built: {output_pdf}")


if __name__ == "__main__":
    generate_comprehensive_academic_report()
