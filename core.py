from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import urllib, json

def convert_pdf_to_txt(path):
    #http://stackoverflow.com/questions/26748788/extraction-of-text-from-pdf-with-pdfminer-gives-multiple-copies
    #adapted from DuckPuncher on stackoverflow 
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    result = text.split("\n")
    result = [x for x in result if x != ""]
    return result

def cat_sentences(stringlist): #need to add criteria of how to determine a valid search term
    for index, thing in enumerate(stringlist):
        if "1. " in thing:
            print thing
            print index
    print stringlist

def search(query):
    querystring = ''
    base_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
    base_cache_url = 'http://webcache.googleusercontent.com/search?q=cache:'

    for index, single in enumerate(query):
        if (index == len(query) - 1):
            querystring += single
        else:
            querystring = querystring + single + "+"
    
    url = base_url + "q=%22" + querystring + "%22"
    raw_data = urllib.urlopen(url).read()
    results = json.loads(raw_data)
    num_results = results['responseData']['cursor']['resultCount']

    return [num_results, results['responseData']['results']]
