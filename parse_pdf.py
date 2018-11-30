
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
import StringIO

def pdf_to_text(filename):
    resource_manager = PDFResourceManager(caching=True)
    outfile = StringIO.StringIO()
    # outfile = open(filename, 'w')
    la_params = LAParams()
    device = TextConverter(
        resource_manager, outfile, codec='utf-8', laparams=la_params, imagewriter=None
    )
    pagenos = set()
    with file(filename, 'rb') as fp:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                        maxpages=0, password='',
                                        caching=True, check_extractable=True):
            page.rotate = 0 # (page.rotate) % 360
            interpreter.process_page(page)
    device.close()
    return outfile.getvalue()

def main():
    print(pdf_to_text("sample_pdf/not_a_result_file.pdf"))

if __name__ == "__main__":
    main()
