#! /usr/bin/python3
import sys
import os
import os.path as path

from pathlib import Path
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTImage, LTFigure

filename = os.path.basename(sys.argv[1])

print("File",  filename)

def pdf2txt(pdfname, txtname):
    btxt=False
    try:
        fp = open(pdfname, 'rb')    
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
    
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)    
        ncount=0
        print("pdf2txt %s..." % pdfname) # informa por consola del nombre de archivo
    
        # abre archivo de texto para la salida
        fptxt = open(txtname, 'w')
        # recorre el documento procesando cada página
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            # recorre la página procesando cada objeto
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    spagetxt = lt_obj.get_text().strip() + " "
                    if(spagetxt!=""):
                        btxt=True
                        fptxt.write(spagetxt)
                        print("Palabra", spagetxt)
                elif isinstance(lt_obj, LTFigure):
                    print("LTFigure, pte implementar!")
                    spagetxt=""
            ncount+=1
    
        print("end")
        fptxt.closed
        fp.closed
    except Exception as e:
        print("Error: %s" % (e))        
    return btxt


pdf2txt(filename, "/home/ulises/1.txt")

