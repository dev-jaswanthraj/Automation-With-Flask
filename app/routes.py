from app import app
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .ProjectUtils.pdfextract import pdftoexcel
from .models import W2Form
from app import db


@app.route("/", methods=['get'])
def index():
    return render_template("base.html")

@app.route("/pdfextract",methods=['get', 'post'])
def pdf_extract():

    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        
        obj = pdftoexcel(app.config['UPLOAD_FOLDER']+'/'+str(file.filename))
        data = list(obj.get_data_from_pdf().values())

        form = W2Form(emp_social_num=str(data[0]), ein=str(data[1]), emp_address=' '.join(data[2]), control_num=str(data[-1]))
        db.session.add(form)
        db.session.commit()

        return render_template("pdfextractPage.html", pdf_extract = True, success = True)

    return render_template("pdfextractPage.html", pdf_extract = True)