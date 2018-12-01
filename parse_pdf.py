
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
import io
import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def pdf_to_text(filename):
    resource_manager = PDFResourceManager(caching=True)
    outfile = io.StringIO()
    # outfile = open(filename, 'w')
    la_params = LAParams()
    device = TextConverter(
        resource_manager, outfile, codec='utf-8', laparams=la_params, imagewriter=None
    )
    pagenos = set()
    with open(filename, 'rb') as fp:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                        maxpages=0, password='',
                                        caching=True, check_extractable=True):
            page.rotate = 0 # (page.rotate) % 360
            interpreter.process_page(page)
    device.close()
    return outfile.getvalue()

def get_word_tokens(text):
    tokens = nltk.word_tokenize(text)
    # Filter out tokens that aren't words, because we only care about keywords
    word_tokens = [token for token in tokens if re.match(r'^\w+$', token)]
    # Filter out stopwords
    return [token for token in word_tokens if not token in stopwords.words('swedish')]


def main():
    text = pdf_to_text("sample_pdf/not_a_result_file.pdf")
    stemmer = SnowballStemmer("swedish", ignore_stopwords=True)
    normalized_tokens = [
        stemmer.stem(token.lower())
        for token in get_word_tokens(text)
    ]
    print(FreqDist(normalized_tokens).most_common(10))


if __name__ == "__main__":
    main()
