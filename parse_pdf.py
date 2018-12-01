
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

KEYWORDS_WE_WANT = ['church', 'school']

def get_text_lang(word_tokens):
    """Returns the language based on the given tokens. 100% accurate and complete solution."""
    swe_char_re = re.compile('[åäö]')
    is_probably_swedish = any(swe_char_re.search(token) for token in word_tokens)
    return 'swedish' if is_probably_swedish else 'english'

def pdf_to_text(filename):
    resource_manager = PDFResourceManager(caching=True)
    outfile = io.StringIO()
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

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    # Filter out tokens that aren't words, because we only care about keywords
    word_tokens = [token.lower() for token in tokens if re.match(r'^\w+$', token.lower())]
    return word_tokens

def parse_doc(filepath):
    print("Reading %s and converting it to text..." % filepath)
    text = pdf_to_text(filepath).strip()
    if text == '':
        print("Not parseable %s" % filepath)
        return
    
    word_tokens = tokenize(text)
    lang = get_text_lang(word_tokens)
    print(" - document language %s" % lang)
        
    stemmer = SnowballStemmer(lang)
    stopword_set = stopwords.words(lang)
    normalized_tokens = [stemmer.stem(token) for token in word_tokens if not token in stopword_set]

    most_common_words = [word for word, _ in FreqDist(normalized_tokens).most_common(100)]
    print(most_common_words)

def main():
    parse_doc("sample_pdf/not_a_result_file_sv.pdf")
    parse_doc("sample_pdf/not_a_result_file_en.pdf")
    parse_doc("sample_pdf/result_en.pdf")

if __name__ == "__main__":
    main()
