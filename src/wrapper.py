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

    BASE_FONT_SIZE = 10

    def wrap_text(self, text, orientation="P"):
        self.set_margins(self.V_MARGIN, self.H_MARGIN)
        self.add_page(orientation=orientation)
        self.add_font("courier", "", "Courier_New.ttf", uni=True)
        self.set_xy(self.V_MARGIN, self.H_MARGIN)
        self.set_font('courier', '', self.BASE_FONT_SIZE)
        self.set_text_color(0, 0, 0)

        cell_height = (72 / self.BASE_FONT_SIZE) * (self.BASE_FONT_SIZE / 16)
        print(f"Font Size: {self.BASE_FONT_SIZE} pt ({72 / self.BASE_FONT_SIZE} mm) Cell Height: {cell_height} mm")
        paragraphs = text.split("\n\n")

        for p_num, paragraph in enumerate(paragraphs):
            line_count = len(paragraph.splitlines())
            current_y = self.get_y()
            print(f"{p_num}: {line_count} lines  y={current_y} mm")
            print(f"Paragraph is {cell_height * line_count} mm high.")
            print(f"There are {self.A4_H_MM - current_y} mm left in the page.")

            if cell_height * line_count > self.A4_H_MM - self.H_MARGIN * 2 - current_y:
                if p_num != 0:
                    self.add_page(orientation=orientation)

            self.multi_cell(
                # self.A4_W_MM - (self.V_MARGIN * 2),
                self.A4_W_MM - (self.V_MARGIN * 2),
                cell_height,
                paragraph,
            )
            self.cell(
                self.A4_W_MM - (self.V_MARGIN * 2),
                cell_height,
                border=0, ln=1,
            )
            print()


@click.command()
@click.argument("input_text_file", type=click.File("r"), metavar="INPUT.TXT")
def main(input_text_file):
    wrap_pdf = TextWrappingPDF()
    wrap_pdf.wrap_text(input_text_file.read())
    # wrap_pdf.wrap_text(TEST_TEXT)
    wrap_pdf.output("wrapped.pdf")


if __name__ == "__main__":
    main()
