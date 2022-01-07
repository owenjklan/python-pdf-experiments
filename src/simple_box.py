#!/usr/bin/env python3

from fpdf import FPDF

BOX_STR = u"┌───────────────────────────────────────────────────┐" \
          "│                                                   │" \
          "│                                                   │" \
          "│                 TEST STRING IN                    │" \
          "│                      A BOX.                       │" \
          "└───────────────────────────────────────────────────┘"

def main():
    pdf = FPDF(format='A5')
    pdf.add_page('P')

    # pdf_w = 210
    # pdf_h = 297
    # pdf.line(0, pdf_h/2, 210, pdf_h/2)

    pdf.set_xy(0.0, 0.0)
    pdf.set_font('Courier', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=50, h=50, align='L', txt=BOX_STR.encode("utf-8").decode('utf-8'))
    pdf.output('output.pdf', 'F')


if __name__ == "__main__":
    main()