from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response, session
from .models import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import datetime
from datetime import datetime
from sqlalchemy import delete, desc, asc
# from io import TextIOWrapper
import csv
import numpy as np
import pandas as pd
import pickle
from tkinter import Y
from pandas import DataFrame
from flask import Flask, request, jsonify, render_template
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
from scipy.stats import spearmanr
from werkzeug.utils import secure_filename
import json
import random
import math
from os import path
import os
import requests
from .classes import UploadCSV

_route_cs = Blueprint('_route_cs', __name__)

@_route_cs.route('/index')
@login_required
def dashboard():
    return '1'

csv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/Institute-of-Computer-Studies-Graduate-Tracer-Study-2021-2022-Responses(ALTERED).csv")

model_IT_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/ProjectModel_IT.pkl")
model_CS_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/ProjectModel_CS.pkl")

# model_ITsuggest_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/IT_SUGGESTEDcourse.pkl")
# model_CSsuggest_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/CS_SUGGESTEDcourse.pkl")
model_ITsuggest_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/CourseRecommend.pkl")
model_CSsuggest_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"model/CourseRecommend.pkl")

dataset = pd.read_csv(csv_path)

ordinal_encoder = OrdinalEncoder()

IT_FEATURES = [
     'Sex',
     'Shiftee',
     'ComProg_1_1st',
     'ComProg_1_2nd',
     'ComProg_2_1st',
     'ComProg_2_2nd',
     'Intro_to_Computing_1st',
     'Intro_to_Computing_2nd',
     'Info_Management_1st',
     'Info_Management_2nd',
     'Operating_System_1st',
     'Operating_System_2nd',
     'Elective_1_1st',
     'Elective_1_2nd',
     'Elective_2_1st',
     'Elective_2_2nd',
     'Elective_3_1st',
     'Elective_3_2nd',
     'Data_Structures_1st',
     'Data_Structures_2nd',
     'Application_Dev_and_Emerging_Tech_1st',
     'Application_Dev_and_Emerging_Tech_2nd',
     'Human_and_Computer_Integration_1st',
     'Human_and_Computer_Integration_2nd',
     'Practicum_Industry_Immersion_1st',
     'Practicum_Industry_Immersion_2nd',
     'Integrative_Programming_and_Tech_1st',
     'Integrative_Programming_and_Tech_2nd',
     'System_Integration_and_Architecture_1st',
     'System_Integration_and_Architecture_2nd',
     'Information_Assurance_and_Security_1_1st',
     'Information_Assurance_and_Security_1_2nd',
     'Information_Assurance_and_Security_2_1st',
     'Information_Assurance_and_Security_2_2nd',
     'Software_Engineering_1st',
     'Software_Engineering_2nd',
     'Networking_1_1st',
     'Networking_1_2nd',
     'Networking_2_1st',
     'Networking_2_2nd',
     'WebProg_1st',
     'WebProg_2nd'
]
CS_FEATURES = [
     'Sex',
     'Shiftee',
     'ComProg_1_1st',
     'ComProg_1_2nd',
     'ComProg_2_1st',
     'ComProg_2_2nd',
     'Intro_to_Computing_1st',
     'Intro_to_Computing_2nd',
     'Info_Management_1st',
     'Info_Management_2nd',
     'Operating_System_1st',
     'Operating_System_2nd',
     'Elective_1_1st',
     'Elective_1_2nd',
     'Elective_2_1st',
     'Elective_2_2nd',
     'Elective_3_1st',
     'Elective_3_2nd',
     'Data_Structures_1st',
     'Data_Structures_2nd',
     'Application_Dev_and_Emerging_Tech_1st',
     'Application_Dev_and_Emerging_Tech_2nd',
     'Human_and_Computer_Integration_1st',
     'Human_and_Computer_Integration_2nd',
     'Practicum_Industry_Immersion_1st',
     'Practicum_Industry_Immersion_2nd',
     'Digital_Design_1st',
     'Digital_Design_2nd',
     'Architecture_and_Organization_1st',
     'Architecture_and_Organization_2nd',
     'Programming_Languages_1st',
     'Programming_Languages_2nd',
     'Modelling_and_Simulation_1st',
     'Modelling_and_Simulation_2nd',
     'Information_Assurance_and_Security_1st',
     'Information_Assurance_and_Security_1_2nd',
     'Software_Engineering_1_1st',
     'Software_Engineering_1_2nd',
     'Software_Engineering_2_1st',
     'Software_Engineering_2_2nd',
     'Network_Management_1st',
     'Network_Management_2nd',
     'Advance_Database_1st',
     'Advance_Database_2nd',
     'WebProg_1st',
     'WebProg_2nd'
]

TARGET = 'Suggested_job_role'

Cat_Y = dataset[TARGET]
X_IT = dataset[IT_FEATURES]
X_CS = dataset[CS_FEATURES]

X_IT = X_IT.replace(np.nan, 0)
X_CS = X_CS.replace(np.nan, 0)

X_IT['Sex'] = ordinal_encoder.fit_transform(X_IT[['Sex']])
X_CS['Sex'] = ordinal_encoder.fit_transform(X_CS[['Sex']])
percent = "%"
#   CREATE FLASK APP
flask_app = Flask(__name__)
#   MAIN JOB ROLE MODEL FOR BOTH IT CS
model_IT = pickle.load(open(model_IT_path, "rb"))
model_CS = pickle.load(open(model_CS_path, "rb"))
#   TOP 5 COURSES SUGGESTION FOR BOTH IT CS
model_ITsuggest = pickle.load(open(model_ITsuggest_path, "rb"))
model_CSsuggest = pickle.load(open(model_CSsuggest_path, "rb"))

@flask_app.route("/")

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def Home():
    return render_template("index.html")

# @flask_app.route("/faculty_end")
# def facultyEnd_view():
#     return render_template("Faculty/facultyEnd.html")

@_route_cs.route('/login_register_CS', methods=['GET'])
def login_registerCS_view():
    auth_user=current_user
    curriculum_input = db.session.query(CurriculumResult).all()
    if auth_user.is_authenticated:
        if auth_user.user_type == 1 and auth_user.department == "Computer Science":
            return redirect(url_for('.cs_dashboard'))
        else:
            return redirect(url_for('_auth.index'))
    return render_template("CS/login_CS.html", curriculum_input=curriculum_input)

@_route_cs.route('/register_CS', methods=['GET'])
def register_CS():
    auth_user=current_user
    curriculum_input = db.session.query(CurriculumResult).all()
    if auth_user.is_authenticated:
        if auth_user.user_type == 1 and auth_user.department == "Computer Science":
            return redirect(url_for('.cs_dashboard'))
        else:
            return redirect(url_for('_auth.index'))
    return render_template("CS/register_CS.html", curriculum_input=curriculum_input)

@_route_cs.route('/login_CS', methods=['GET', 'POST'])
def login_CS():
    auth_user=current_user
    if auth_user.is_authenticated:
        if auth_user.user_type == 1 and auth_user.department == "Computer Science":
            return redirect(url_for('.cs_profile'))
        else:
            return redirect(url_for('_auth.index'))
    else:
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email'], department='Computer Science').first()
            if user:
                if user.is_approve == True:
                    if check_password_hash(user.password, request.form['password']):
                        login_user(user, remember=True)
                        return redirect(url_for('.cs_profile'))
                    else:
                        flash('Invalid or wrong password', category='error')
                else:
                    flash('Account is not approve yet, wait for further notice.', category='info')
            else:
                flash('No record found', category='error')
    return redirect(url_for('.login_registerCS_view'))

@_route_cs.route('/signupCS', methods=['POST'])
def signupCS():
    first = request.form['first_name']
    middle = request.form['middle_name']
    last = request.form['last_name']
    
    if (request.form['email'].__contains__('@wmsu.edu.ph')):
        if(first.isspace() != True or middle.isspace() != True or last.isspace() != True):
            try:
                new_user = User(request.form['first_name'], request.form['middle_name'], request.form['last_name'], request.form['sex'], request.form['curriculum_year'], request.form['contact_number'], request.form['email'], request.form['desired_career'],  'Computer Science', request.form['program'], (generate_password_hash(request.form['password'], method="sha256")), False, 0, 1)
                db.session.add(new_user)
                db.session.commit()
                flash('Account successfully created. Registration feedback will be sent soon via email -support@wetechsupport.online', category='success_register_cs')
                return redirect(url_for('.login_CS'))
            except:  
                flash('Invalid credentials', category='error')
        else:
            flash('Please enter necessary data in fields', category='error')
    else:
        flash('Invalid Email. Outside WMSU email is not allowed', category='error')
    
    return redirect(url_for('.register_CS'))

@_route_cs.route('/cs_dashboard', methods=['GET', 'POST'])
@login_required
def cs_dashboard():
    auth_user=current_user
    form_upload = UploadCSV()
    
    if(request.method == 'GET'):
        try:
            if auth_user.user_type == 1 and auth_user.department == "Computer Science" and auth_user.sex == "Male":
                sex = 0
                student_predictions = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', PredictionResult.user_id == int(auth_user.id)).group_by(PredictionResult.result_id).all()
                predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
                remaining_attempt = int(predict_iter.predict_no)
            
                if auth_user.program == "Shiftee" or auth_user.program == "Transferee":
                    program = 1

                elif auth_user.program == "Regular":
                    program = 0
                    
            elif auth_user.user_type == 1 and auth_user.department == "Computer Science" and auth_user.sex == "Female":
                sex = 1
                student_predictions = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', PredictionResult.user_id == int(auth_user.id)).group_by(PredictionResult.result_id).all()
                predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
                remaining_attempt = int(predict_iter.predict_no)
                
                if auth_user.program == "Shiftee" or auth_user.program == "Transferee":
                    program = 1

                elif auth_user.program == "Regular":
                    program = 0

            else:
                return redirect(url_for('_auth.index'))
            
            return render_template("CS/CS_landing.html", auth_user=auth_user, sex=sex, program=program, remaining_attempt=remaining_attempt, student_predictions=student_predictions, form_upload=form_upload)
        
        except:
            return redirect(url_for('/logout'))
        
    else:
         # get uploaded file from thr form
        file = form_upload.file.data
        # create a file path and concatenate the file name
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/images',secure_filename(file.filename))
        # save the file based on the file path
        # file.filename
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        if file and allowed_file(file.filename):
            image = User.query.filter_by(id=int(auth_user.id)).first()
            image.img = file.filename
            db.session.commit()
            file.save(file_path)
            flash('Photo successfully added', category='upload_successfully')
        elif not file:
            flash('No photo uploaded!', category='upload_error')
        else:
            flash('Invalid format!', category='upload_error')
        
        return redirect(url_for('.cs_dashboard'))

@_route_cs.route("/cs_result", methods=['GET'])
def cs_result():
    auth_user=current_user
    if auth_user.user_type == 1:
        return render_template("CS/CS_result.html", auth_user=auth_user)
    else:
        return redirect(url_for('_auth.index'))
    
@_route_cs.route("/cs_profile", methods=['GET', 'POST'])
def cs_profile():
    form_upload = UploadCSV()
    auth_user=current_user
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    data1 = location_data.get("ip")
    data2 = location_data.get("city")
    data3 = location_data.get("region")
    data4 = location_data.get("country")
    
    # img = User.query.filter_by(id=int(auth_user.id)).order_by(desc(User.date_created)).first()
    # img_path = img.img
    # image = img_path
    if(request.method == 'GET'):  
        try:
            top_career = PredictionResult.query.filter_by(user_id=int(auth_user.id)).order_by(desc(PredictionResult.date_created)).first()
            top_path = top_career.top_rank
            job_desired = top_path

            if request.method == 'GET':
                
                if auth_user.user_type == 1 and auth_user.department == "Computer Science" and auth_user.sex == "Male":
                    sex = 0
                    student_predictions = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', PredictionResult.user_id == int(auth_user.id)).group_by(PredictionResult.result_id).all()
                    predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
                    remaining_attempt = int(predict_iter.predict_no)
                    
                    if auth_user.program == "Shiftee" or auth_user.program == "Transferee":
                        program = 1
                    elif auth_user.program == "Regular":
                        program = 0
                elif auth_user.user_type == 1 and auth_user.department == "Computer Science" and auth_user.sex == "Female":
                    sex = 1
                    student_predictions = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', PredictionResult.user_id == int(auth_user.id)).group_by(PredictionResult.result_id).all()
                    predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
                    remaining_attempt = int(predict_iter.predict_no)
                    
                    if auth_user.program == "Shiftee" or auth_user.program == "Transferee":
                        program = 1
                    elif auth_user.program == "Regular":
                        program = 0
                else:
                    return redirect(url_for('_auth.index'))
                
            return render_template("CS/CS_profile.html", auth_user=auth_user, sex=sex, program=program, remaining_attempt=remaining_attempt, student_predictions=student_predictions, job_desired=job_desired, data2=data2, 
                                data3=data3, data4=data4, form_upload=form_upload)
        except:
            return redirect(url_for('.cs_dashboard'))
    else:
        # get uploaded file from thr form
        file = form_upload.file.data
        # create a file path and concatenate the file name
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/images',secure_filename(file.filename))
        # save the file based on the file path
        # file.filename
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        if file and allowed_file(file.filename):
            image = User.query.filter_by(id=int(auth_user.id)).first()
            image.img = file.filename
            db.session.commit()
            file.save(file_path)
            flash('Photo successfully added', category='upload_successfully')
        elif not file:
            flash('No photo uploaded!', category='upload_error')
        else:
            flash('Invalid format!', category='upload_error')
        
        return redirect(url_for('.cs_profile'))

    
@_route_cs.route("/edit_profile_cs", methods=['POST'])
def edit_profile_cs():
    auth_user=current_user
    if auth_user.user_type == 1 and auth_user.department == "Computer Science":
        predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
        current_pred_no = predict_iter.predict_no
        if current_pred_no < 2:
            career = User.query.filter_by(id=int(auth_user.id)).first()
            career.desired_career = request.form['desiredCareer']
            
            job = db.session.query(PredictionResult).filter(PredictionResult.result_id == int(auth_user.id))
            job.desired_job = request.form['desiredCareer']
            db.session.commit()
            flash('Profile Successfully Modified', category='info')
        else:
            flash('Sorry there is no sense to change career, since you already met the prediction attempts', category='info')
    else:
        return redirect(url_for('_auth.index'))
    return redirect(url_for('.cs_profile'))

@_route_cs.route("/edit_profile_cs_dashboard", methods=['POST'])
def edit_profile_cs_dashboard():
    auth_user=current_user
    if auth_user.user_type == 1 and auth_user.department == "Computer Science":
        predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
        current_pred_no = predict_iter.predict_no
        if current_pred_no < 2:
            career = User.query.filter_by(id=int(auth_user.id)).first()
            career.desired_career = request.form['desiredCareer']
            
            job = db.session.query(PredictionResult).filter(PredictionResult.result_id == int(auth_user.id))
            job.desired_job = request.form['desiredCareer']
            db.session.commit()
            flash('Profile Successfully Modified', category='info')
        else:
            flash('Sorry there is no sense to change career, since you already met the prediction attempts', category='info')
    else:
        return redirect(url_for('_auth.index'))
    return redirect(url_for('.cs_dashboard'))

@_route_cs.route("/predict_CS", methods=["GET", "POST"])
def predict_CS():
    auth_user=current_user
    
    if auth_user.predict_no <= 1:
        if request.method== 'GET':
            return render_template("CS/CS_landing.html")
        else:
            float_features = [float(x) for x in request.form.values()]
            features = [np.array(float_features)]
            new_Xdata_CS = X_CS.sample(4)
            new_Ydata_CS = Cat_Y[new_Xdata_CS.index.values]
            pred_CS = model_CS.predict(features)
            suggestCS = model_CSsuggest.predict(pred_CS)

            def recall(new_Ydata_CS, pred_CS, K):
                    act_set = set(new_Ydata_CS)
                    pred_set = set(pred_CS[:K])
                    result = round(len(act_set & pred_set) / float(len(act_set)), 2)
                    return result
                
            for K in range(0, 3):
                
                predCS = pred_CS[0]
                actual = new_Ydata_CS
                prediction = ["Software Engineer / Programmer", "Technical Support Specialist", "Academician", "Administrative Assistant"]
                # random.shuffle(prediction)
                prediction = [prediction.replace(predCS, '0')for prediction in prediction]
                prediction.append(predCS)
                
                fetch1 = recall(actual, prediction, K)
                if fetch1 == 1.0:
                    fetch1 = 100
                elif fetch1 == 0.75:
                    fetch1 = 75
                elif fetch1 == 0.67:
                    fetch1 = 67 
                elif fetch1 == 0.5:
                    fetch1 = 50
                elif fetch1 == 0.33:
                    fetch1 = 33
                elif fetch1 == 0.25:
                    fetch1 = 25
                else:
                    fetch1 = 0
                    
                fetch2 = recall(actual, prediction, K-1)
                if fetch2 == 1.0:
                    fetch2 = 100
                elif fetch2 == 0.75:
                    fetch2 = 75
                elif fetch2 == 0.67:
                    fetch2 = 67
                elif fetch2 == 0.5:
                    fetch2 = 50
                elif fetch2 == 0.33:
                    fetch2 = 33
                elif fetch2 == 0.25:
                    fetch2 = 25
                else:
                    fetch2 = 0
                    
                fetch3 = recall(actual, prediction, K-2)
                if fetch3 == 1.0:
                    fetch3 = 100
                elif fetch3 == 0.75:
                    fetch3 = 75
                elif fetch3 == 0.67:
                    fetch3 = 67
                elif fetch3 == 0.5:
                    fetch3 = 50
                elif fetch3 == 0.33:
                    fetch3 = 33
                elif fetch3 == 0.25:
                    fetch3 = 25
                else:
                    fetch3 = 0
                    
                fetch4 = recall(actual, prediction, K-3)
                if fetch4 == 1.0:
                    fetch4 = 100
                elif fetch4 == 0.75:
                    fetch4 = 75
                elif fetch4 == 0.67:
                    fetch4 = 67
                elif fetch4 == 0.5:
                    fetch4 = 50
                elif fetch4 == 0.33:
                    fetch4 = 33
                elif fetch4 == 0.25:
                    fetch4 = 25
                else:
                    fetch4 = 0
                    
                fetchPred1 = prediction[0]
                fetchPred2 = prediction[-1]
                fetchPred3 = prediction[-2]
                fetchPred4 = prediction[-3]
                
                
                '''
                    ADD NEW RECORD TO DATABASE
                '''
                date_predicted = datetime.now()
                
                pred2 = "No Result" if fetch2 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred2 == '0' else "{}".format(f"{prediction[K-1]} : {fetch2}%")
                pred3 = "No Result" if fetch3 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred3 == '0' else "{}".format(f"{prediction[K-2]} : {fetch3}%"),
                pred4 = "No Result" if fetch4 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred4 == '0' else "{}".format(f"{prediction[K-3]} : {fetch4}%")
                pred1 = "No Result" if fetch1 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred1 == '0' else "{}".format(f"{prediction[K]} : {fetch1}%")
                
                job = User.query.filter_by(id=int(auth_user.id)).first()
                val = job.desired_career
                job_desired = val
                
                new_pred = PredictionResult(job_desired, fetchPred2, pred2, pred4, pred3, pred1, auth_user.id, date_created=date_predicted)
                db.session.add(new_pred)
                
                predict_iter = User.query.filter_by(id=int(auth_user.id)).first()
                predict_iter.predict_no += 1
                
                db.session.commit()
                
                return render_template("/CS/CS_result.html", 
                                    prediction_text1 = "" if fetch1 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred1 == '0' else "{}".format(f"{prediction[K]} : {fetch1}%"), 
                                    prediction_text2 = "" if fetch2 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred2 == '0' else "{}".format(f"{prediction[K-1]} : {fetch2}%"),
                                    prediction_text3 = "" if fetch3 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred3 == '0' else "{}".format(f"{prediction[K-2]} : {fetch3}%"),
                                    prediction_text4 = "" if fetch4 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 == 0 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" or fetchPred4 == '0' else "{}".format(f"{prediction[K-3]} : {fetch4}%"),
                                    prediction_label1 = "" if fetch2 == 0 or fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 == 1.0 and fetchPred2 == "Administrative Assistant" else "{}".format(f"{prediction[K-1]} "),
                                    prediction_label3 = "{}".format(f"We apologize for the poor results caused by the anomaly our system discovered when performing the prediction....") if fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 else "",
                                    prediction_label4 = "- In addition to the possibilities mentioned above, there is still a significant chance that you will be hired for your first job in one or more of the positions listed on the left side." if fetch1 > 0 and fetchPred1 !="0" or fetch3 > 0 and fetchPred3 !="0" or fetch4 > 0 and fetchPred4 !="0" or fetchPred2 == "Administrative Assistant" else "",
                                    job_label1 = "{}".format(f"{prediction[K-1]} = {fetch2}%") if fetch2 <= 100 and fetch1 >= 0 and fetch3 >= 0 and fetch4 >= 0 and fetchPred2 == "Administrative Assistant" else "",
                                    job_label2 = "Predicted IT/CS Related Job(s)" if fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch1 == 0 and fetch2 <= 100 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" else "Predicted IT/CS Related Job(s)",
                                    label_text2 = "- To increase the likelihood of landing IT/CS-related jobs, the below courses on the left side must be improved." if fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 >= 0 and fetch3 >= 0 and fetch4 >= 0 and fetchPred2 == "Administrative Assistant" or fetch2 <= 100 and fetch1 >= 0 and fetch3 >= 0 and fetch4 >= 0 and fetchPred2 == '0' or fetch1 == 0 and fetch2 <= 100 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" else "",
                                    course_suggestion2 = "{}".format(suggestCS.tolist()) if fetch1 == 0 and fetch2 == 0 and fetch3 == 0 and fetch4 == 0 or fetch2 <= 100 and fetch1 >= 0 and fetch3 >= 0 and fetch4 >= 0 and fetchPred2 == "Administrative Assistant" or fetch2 <= 100 and fetch1 >= 0 and fetch3 >= 0 and fetch4 >= 0 and fetchPred2 == '0' or fetch1 == 0 and fetch2 <= 100 and fetch3 == 0 and fetch4 == 0 and fetchPred2 == "Administrative Assistant" else "",
                                    auth_user=auth_user
                                    )
    else:
        flash('Sorry you cannot predict again, you have already met the prediction chances', category='error')
        return redirect(url_for('.cs_dashboard'))
