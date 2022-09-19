from app import app
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from .ProjectUtils.pdfextract import pdftoexcel
from .ProjectUtils.compareExcel import comparefile
from .ProjectUtils.pivot import  Pivot  
from .ProjectUtils.webscraping import Scrap
from .models import W2Form, User
from flask_login import login_required, login_user,logout_user, current_user
from app import db
from sqlalchemy import desc

@app.route("/", methods=['get'])
def index():
    return render_template("base.html", home=True)

@app.route('/login',methods=['post', 'get'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email_id = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("index"))
            else:
                flash("Password is Incorrect", category="danger")
        else:
            flash("Eamil ID is incorrect",category="danger")
        
    return render_template("login.html", login=True)

@app.route('/signup', methods = ['post', 'get'])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        if User.query.filter_by(email_id = email).first() != None:
            flash("Email ID already exists.", category='danger')
            return redirect(url_for("signup"))
        pwd = request.form.get("pwd2")
        user = User(fullname = fullname, email_id = email, password = generate_password_hash(pwd, method= "sha256"))
        db.session.add(user)
        db.session.commit()
        flash("Registration is Success! You Can Login Now Using your Email ID.", category='success')
        return redirect(url_for('login'))
    return render_template("signup.html", signup=True)

@app.route("/logout", methods=['get'])
@login_required
def logout():
    session['user_id'], session["user_name"] = None, None
    logout_user()
    return redirect(url_for("index"))

@app.route("/pdfextract",methods=['get', 'post'])
@login_required
def pdf_extract():

    if request.method == "POST":
        files = request.files.getlist('files')
        user_id = int(current_user.id)
        
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            
            obj = pdftoexcel(app.config['UPLOAD_FOLDER']+'/'+str(file.filename))
            data = list(obj.get_data_from_pdf().values())
            user_id = int(current_user.id)
            form = W2Form(
                emp_social_num=str(data[0]), 
                ein=str(data[1]), 
                emp_address=" ".join(data[2]), 
                control_num=str(data[-1]), 
                user_id = user_id
            )
            db.session.add(form)
            db.session.commit()
            
        flash("Files are Successfuly extracted.")
        return render_template("pdfextractPage.html", pdf_extract = True, id = user_id, count = len(files))

    return render_template("pdfextractPage.html", pdf_extract = True)

@app.route('/details/<int:id>,<int:count>', methods=['get'])
@login_required
def details(id, count):
    user_details = W2Form.query.filter_by(user_id = id).order_by(desc(W2Form.id)).limit(count)
    return render_template("details.html", user_datas = user_details)

@app.route("/compareexcel", methods=['post', 'get'])
@login_required
def compare_excel():
    if request.method == "POST":
        file1 = request.files['file1']
        file2 = request.files['file2']

        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))


        compareFile = comparefile(app.config['UPLOAD_FOLDER']+'/'+str(file1.filename), app.config['UPLOAD_FOLDER']+'/'+str(file2.filename))

        filename = compareFile.compare()
        if filename:
            flash("File Comparison Successful.")
            f = r"Other/{}".format(filename)
            return render_template("compareexcel.html", compare_excel=True, filename = f)
        else:
            flash("Some Error")
            return render_template("compareexcel.html", compare_excel=True)
    return render_template("compareexcel.html", compare_excel=True)


@app.route('/pivottabel', methods=["post", "get"])
@login_required
def pivot_table():
    if request.method == "POST":
        file = request.files['file']
        
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
        p = Pivot(app.config['UPLOAD_FOLDER']+'/'+str(file.filename))
        filename = p.get_pivot()
        if filename:
            flash("Pivot Tabel Created.")
            f = "Other/{}".format(filename)
            return render_template("pivotTable.html", pivot_table = True, filename = f)
        else:
            flash("Some Error")
            return render_template("pivot_table.html", pivot_tabel = True)
    return render_template("pivotTable.html", pivot_table = True)

@app.route("/webscraping", methods=['post', 'get'])
@login_required
def web_scraping():

    if request.method == "POST":
        productname = request.form.get("productname")
        
        ps = Scrap(productname)
        filename = ps.open_browser_with_amazon()
        ps.close_diver()
        if filename:
            flash("Data Successfuly Scraped.")
            f = "Other/{}".format(filename)
            return render_template("webscraping.html", web_scraping=True, filename = f)
        else:
            flash("Some Error")
            return render_template("webscraping.html", web_scraping=True)

    return render_template("webscraping.html", web_scraping = True)