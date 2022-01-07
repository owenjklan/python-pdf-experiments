#!/usr/bin/env python3

import click
from fpdf import FPDF


class SimplePDFBuilder(FPDF):
    A4_W_MM = 210
    A4_H_MM = 297
    A5_W_MM = 148
    A5_H_MM = 210

    DEFAULT_H_MARGIN = 20.0
    DEFAULT_V_MARGIN = 15.0

    DEFAULT_DOCUMENT_TITLE_SIZE_PT = 24
    DEFAULT_SECTION_TITLE_SIZE_PT = 18
    DEFAULT_TEXT_SIZE_PT = 10

    DEFAULT_LINE_WIDTH = 0.2

    PORTRAIT = "P"
    LANDSCAPE = "L"

    LEFT_ALIGN = "L"
    RIGHT_ALIGN = "R"
    CENTER_ALIGN = "C"
    JUSTIFIED_ALIGN = "J"

    def __init__(self, format="A4"):
        super().__init__(
            orientation=self.PORTRAIT,
            format=format,
            unit="mm",
        )
        self.set_margins(self.DEFAULT_H_MARGIN, self.DEFAULT_V_MARGIN)

        if format.upper() == "A4":
            self.page_width = self.A4_W_MM
            self.page_height = self.A4_H_MM
        elif format.upper() == "A5":
            self.page_width = self.A5_W_MM
            self.page_height = self.A5_H_MM
        else:
            raise ValueError(f"Unknown format: {format}")

        # Add fonts with Unicode support enabled
        self.add_font("arial", "", "Arial.ttf", uni=True)
        self.add_font("courier", "", "Courier_New.ttf", uni=True)

        # Calculate useful cell heights
        self.title_cell_height = 72 / self.DEFAULT_DOCUMENT_TITLE_SIZE_PT
        self.section_title_cell_height = 72 / self.DEFAULT_SECTION_TITLE_SIZE_PT
        self.normal_text_cell_height = 72 / self.DEFAULT_TEXT_SIZE_PT * (self.DEFAULT_TEXT_SIZE_PT / 16)

        # Initial page setup and cursor position
        self.add_page()
        self.set_text_color(0, 0, 0)
        self.set_xy(self.DEFAULT_H_MARGIN, self.DEFAULT_V_MARGIN)
        self.set_to_normal()

    def set_to_normal(self):
        self.set_font("arial", "", self.DEFAULT_TEXT_SIZE_PT)

    def write_title(self, title_text):
        self.set_font("arial", "B", self.DEFAULT_DOCUMENT_TITLE_SIZE_PT)
        self.cell(
            self.page_width - (self.DEFAULT_V_MARGIN * 2),
            self.title_cell_height,
            title_text,
            ln=1,
        )
        self.ln(self.normal_text_cell_height)

        # current_y = self.get_y()
        # self.set_xy(
        #     self.DEFAULT_H_MARGIN,
        #     current_y + (self.title_cell_height * 1.5)
        # )
        self.set_to_normal()

    def write_section_title(self, title_text):
        self.set_font("arial", "B", self.DEFAULT_SECTION_TITLE_SIZE_PT)
        self.cell(
            self.page_width - (self.DEFAULT_V_MARGIN * 2),
            self.section_title_cell_height,
            title_text,
            ln=1,
        )
        current_y = self.get_y()
        self.set_xy(
            self.DEFAULT_H_MARGIN,
            current_y + (self.section_title_cell_height * 0.5)
        )
        self.set_to_normal()

    def write_paragraph(self, text, border=0, font="arial"):
        self.set_font(font, "", self.DEFAULT_TEXT_SIZE_PT)
        self.multi_cell(
            self.page_width - (self.DEFAULT_H_MARGIN * 2),
            self.normal_text_cell_height,
            text,
            border=border,
        )
        self.cell(
            self.page_width - (self.DEFAULT_H_MARGIN * 2),
            self.normal_text_cell_height,
            "", border=0, ln=1,
        )

    def write_paragraphs(self, paragraphs, font="arial"):
        self.set_font(font, "", self.DEFAULT_TEXT_SIZE_PT)
        for p_num, paragraph in enumerate(paragraphs):
            line_count = len(paragraph.splitlines())
            current_y = self.get_y()

            if self.normal_text_cell_height * line_count > self.page_height - self.DEFAULT_H_MARGIN * 2 - current_y:
                if p_num != 0:
                    self.add_page()

            self.multi_cell(
                # self.A4_W_MM - (self.V_MARGIN * 2),
                self.page_width - (self.DEFAULT_H_MARGIN * 2),
                self.normal_text_cell_height,
                paragraph,
                align=self.JUSTIFIED_ALIGN,
            )
            self.cell(
                self.page_width - (self.DEFAULT_H_MARGIN * 2),
                self.normal_text_cell_height,
                border=0, ln=1,
            )

    def hr(self, thickness=DEFAULT_LINE_WIDTH):
        current_y = self.get_y()
        self.set_line_width(thickness)

        self.line(
            self.DEFAULT_H_MARGIN,
            current_y - (self.normal_text_cell_height / 8),
            self.page_width - (self.DEFAULT_H_MARGIN),
            current_y - (self.normal_text_cell_height / 8)
        )

        self.ln()

        self.set_line_width(self.DEFAULT_LINE_WIDTH)

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Print centered page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    # def header(self):
    #     # Select Arial bold 15
    #     self.set_font('Arial', 'B', 15)
    #     # Framed title
    #     self.cell(
    #         self.A4_W_MM - (self.DEFAULT_H_MARGIN * 2),
    #         self.normal_text_cell_height,
    #         "Document Builder Test Document",
    #         border=0,
    #         align="C",
    #         ln=1,
    #     )
    #     # Line break
    #     self.ln()


INTRO_PARAGRAPH = """This is a sample document, created with the 'SimplePDFBuilder()'
class.

This class is an extension of the PyFPDF base class, FPDF()."""

CODE_PARAGRAPH = """def wrap_text(self, text, orientation="P"):
    self.set_margins(self.V_MARGIN, self.H_MARGIN)
    self.add_page(orientation=orientation)
    self.add_font("courier", "", "Courier_New.ttf", uni=True)
    self.set_xy(self.V_MARGIN, self.H_MARGIN)
    self.set_font('courier', '', self.BASE_FONT_SIZE)
    self.set_text_color(0, 0, 0)"""

CONCLUSION_PARAGRAPH = """FPDF (and PyFPDF) is a library with low-level primitives to easily generate PDF documents. This is similar to ReportLab's graphics canvas, but with some methods to output "fluid" cells ("flowables" that can span multiple rows, pages, tables, columns, etc.). It has several methods ("hooks") that can be redefined, to fine-control headers, footers, etc.

Originally developed in PHP several years ago (as a free alternative to proprietary C libraries), it has been ported to many programming languages, including ASP, C++, Java, Pl/SQL, Ruby, Visual Basic, and of course, Python.

For more information see: http://www.fpdf.org/en/links.php"""

# @click.command()
# @click.argument("input_text_file", type=click.File("r"), metavar="INPUT.TXT")
def main():
    doc_pdf = SimplePDFBuilder(format="A4")

    doc_pdf.write_title("Test Title")
    doc_pdf.hr(thickness=1.0)

    doc_pdf.write_paragraph(INTRO_PARAGRAPH, border=1)
    doc_pdf.write_paragraph("The following paragraph includes some code, in "
                            "a monospaced font.")
    doc_pdf.write_paragraph(CODE_PARAGRAPH, font="courier")
    doc_pdf.write_paragraph("So, that appears to have worked out nicely. :D")

    doc_pdf.hr()
    doc_pdf.write_section_title("Conclusion")
    paragraphs = CONCLUSION_PARAGRAPH.split("\n\n")
    doc_pdf.write_paragraphs(paragraphs)

    # New page
    doc_pdf.add_page()
    doc_pdf.write_title("Appendices")
    doc_pdf.hr(thickness=1.0)
    doc_pdf.write_section_title("The Raven - Edgar Allen Poe")

    raven_text = open("raven.txt", "r").read()
    paragraphs = raven_text.split("\n\n")
    doc_pdf.write_paragraphs(paragraphs, font="courier")

    # New page
    doc_pdf.add_page()
    doc_pdf.write_section_title("LICENSE")
    license_text = open("../LICENSE", "r").read()
    paragraphs = license_text.split("\n\n")
    doc_pdf.write_paragraphs(paragraphs, font="courier")

    # New page
    doc_pdf.add_page()
    doc_pdf.write_section_title("Image Example")
    doc_pdf.write_paragraph("This appendix demonstrates inclusion of a "
                            "JPEG file from disk.")
    doc_pdf.image("line_graph.jpg", w=doc_pdf.page_width - (doc_pdf.DEFAULT_H_MARGIN * 2))
    doc_pdf.output("docbuilder.pdf")


if __name__ == "__main__":
    main()
