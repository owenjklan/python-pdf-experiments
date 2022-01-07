#!/usr/bin/env python3
# coding: utf8

import click
from fpdf import FPDF

TEST_TEXT = """I am trying to make flowing text using PyFPDF and a sub-class.
New-lines are supposed to just work.

So should paragraphs, etc.
Blah, blah, purple monkey dishwasher.
"""


class TextWrappingPDF(FPDF):
    A4_W_MM = 210
    A4_H_MM = 297

    H_MARGIN = 10.0
    V_MARGIN = 10.0

    def wrap_text(self, text, orientation="P"):
        self.set_margins(self.V_MARGIN, self.H_MARGIN)
        self.add_page(orientation=orientation)
        self.add_font("courier", "", "Courier_New.ttf", uni=True)
        self.set_xy(self.V_MARGIN, self.H_MARGIN)
        self.set_font('courier', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(
            self.A4_W_MM - (self.V_MARGIN * 2),
            self.A4_H_MM - (self.H_MARGIN * 4),
            text,
            align="R",
        )


@click.command()
@click.argument("input_text_file", type=click.File("r"), metavar="INPUT.TXT")
def main(input_text_file):
    wrap_pdf = TextWrappingPDF()
    # wrap_pdf.wrap_text(input_text_file.read())
    wrap_pdf.wrap_text(TEST_TEXT)
    wrap_pdf.output("wrapped.pdf")


if __name__ == "__main__":
    main()
