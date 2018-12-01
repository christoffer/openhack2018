
import os
import sys
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PSEOF, PDFSyntaxError
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
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords

FOSSIL_FUEL_DOCUMENT = 'FOSSIL_FUEL'

def get_document_classification(classification_tokens):
    if 'fuel' in classification_tokens and 'fossil' in classification_tokens:
        return FOSSIL_FUEL_DOCUMENT
    return None

def get_text_lang(word_tokens):
    """Returns the language based on the given tokens. 100% accurate and complete solution."""
    swe_char_re = re.compile('[åäö]')
    is_probably_swedish = any(swe_char_re.search(token) for token in word_tokens)
    return 'swedish' if is_probably_swedish else 'english'

def is_supported_lang(lang):
    return lang == 'english'

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
    try:
        text = pdf_to_text(filepath).strip()
    except (PSEOF, PDFSyntaxError):
        print("Failed to parse document %s" % filepath)
        return
    except PDFTextExtractionNotAllowed:
        print("Text parsing not allowed for document %s" % filepath)
        return

    if text == '':
        print("Document does not contain text data %s" % filepath)
        return

    word_tokens = tokenize(text)
    lang = get_text_lang(word_tokens)
    if not is_supported_lang(lang):
        print("Not a supported language %s, skipping..." % lang)
        return

    lemmatizer = WordNetLemmatizer()
    stopword_set = stopwords.words(lang)
    normalized_tokens = [lemmatizer.lemmatize(token, "n") for token in word_tokens if not token in stopword_set]

    classification_tokens = [word for word, _ in FreqDist(normalized_tokens).most_common(100)]
    print(classification_tokens)
    doc_class = get_document_classification(classification_tokens)
    print("Document classification: %s" % doc_class)

def main():
    pdf_dir = "pdf_cache"
    pdf_filenames = [filename for filename in os.listdir(pdf_dir) if filename.lower().endswith('.pdf')]
    for pdf_filename in pdf_filenames:
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        parse_doc(pdf_path)
    
if __name__ == "__main__":
    main()
