from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger

pdf_file = PdfFileReader(open("GEOGRAPHY_QUIZ.pdf","rb"))
def making_pdf(page_no):
    page = pdf_file.getPage(page_no)
    page.cropBox.setLowerRight((595.22,0))
    page.cropBox.setLowerLeft((0,0))
    page.cropBox.setUpperRight((595.22,842))
    page.cropBox.setUpperLeft((0,842))
    output = PdfFileWriter()
    output.addPage(page)

    with open("New.pdf", "wb") as out_f:
        output.write(out_f)
