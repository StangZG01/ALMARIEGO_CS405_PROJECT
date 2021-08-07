import os
import nltk
import PyPDF2
import pandas as pd

from flask import Flask, render_template, request, send_from_directory
from flask_dropzone import Dropzone
import glob
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH= os.path.join(basedir,'uploads'),
    DROPZONE_MAX_FILE_SIZE = 100000,
    DROPZONE_TIMEOUT = 5*60*1000)

dropzone = Dropzone(app)



@app.route('/',methods=['POST','GET'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    Path = "./uploads/"
    filelist = os.listdir(Path)
    pdfs = []

    for i in filelist:
        if i.endswith(".pdf"): 
            with open(Path + i, 'rb') as f:
                pdfReader = PyPDF2.PdfFileReader(f)
                pdf = {}
                text = ''
                for p in range(pdfReader.numPages):
                    pageObject = pdfReader.getPage(p)
                    text +=pageObject.extractText()
                words = nltk.word_tokenize(text)
                pdf['Filename'] = i
                pdf['Ner'] = words
                pdf_copy = pdf.copy()
                pdfs.append(pdf_copy)
    return render_template('search.html', pdfs = pdfs)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):    
    return send_from_directory(directory='uploads', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
