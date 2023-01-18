from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response, session
from flask_login import login_required, current_user
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import delete, desc, asc
from sqlalchemy import select
import datetime
from datetime import datetime
import json

from .auth import send_link, send_link_disapproved # for email message

_faculty = Blueprint('_faculty', __name__)

@_faculty.route('/login_register_faculty', methods=['GET'])
def login_registerFaculty_view():
    auth_user=current_user
    if auth_user.is_authenticated:
        if auth_user.user_type == -1 or auth_user.user_type == 0:
            return redirect(url_for('.faculty_dashboard'))
        else:
            return redirect(url_for('_auth.index'))
            
    return render_template("Faculty/login_admin.html")

@_faculty.route('/register_faculty', methods=['GET'])
def register_faculty():    
    auth_user=current_user
    if auth_user.is_authenticated and auth_user.user_type == -1:
        return render_template("Faculty/register_admin.html")
    else:
        flash('Sorry only the admin is permitted to register a faculty account', category='error')
        return redirect(url_for('.faculty_dashboard'))

    
@_faculty.route('/login_faculty', methods=['GET', 'POST'])
def login_faculty():
    auth_user=current_user
    if auth_user.is_authenticated:
        if auth_user.user_type == -1 or auth_user.user_type == 0:
            return redirect(url_for('.faculty_dashboard'))
        else:
            return redirect(url_for('_auth.index'))
    else:
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email'], department='faculty').first()
            print(user)
            if user:
                if check_password_hash(user.password, request.form['password']):
                    login_user(user, remember=True)
                    return redirect(url_for('.faculty_dashboard'))
                else:
                    flash('Invalid or wrong password', category='error')
            else:
                flash('No record found', category='error')
    return redirect(url_for('.login_registerFaculty_view'))


@_faculty.route('/faculty_dash', methods=['GET'])
@login_required
def faculty_dash():
    if request.method == 'GET':
        # Current Logged User
        auth_user=current_user
        page = request.args.get('page', 1, type=int)

        # Data for search
        search = request.args.getlist('search')
        search = (','.join(search))
        
        sex = request.args.getlist('sex')
        sex = (','.join(sex))
        
        print(search, sex)
        # Data for filter department
        # Return Data for template
        if auth_user.user_type == -1 or auth_user.user_type == 0:
            if search:
                students_record = db.session.query(User).filter(User.is_approve == 1, User.department == 'Faculty')\
                    .filter((User.first_name.like('%' + search + '%'))      |
                    (User.middle_name.like('%' + search + '%'))     |
                    (User.last_name.like('%' + search + '%'))       |
                    (User.desired_career.like('%' + search + '%'))         |
                    (User.contact_number.like('%' + search + '%'))  |
                    (User.department.like('%' + search + '%'))    |
                    (User.email.like('%' + search + '%')))\
                    .paginate(page=page, per_page=5)# fetch user students only
            elif sex:
                students_record = db.session.query(User).filter(User.is_approve == 1, User.department == 'Faculty')\
                    .filter((User.sex==sex))\
                    .paginate(page=page, per_page=5)# fetch sex only
            else:
                students_record = db.session.query(User).filter(User.is_approve == 1, User.department == 'Faculty').paginate(page=page, per_page=5)# fetch user students only

            auth_user=current_user
        else:
            return redirect(url_for('_auth.index'))
        
        return render_template("Faculty/faculty_dashboard.html", auth_user=auth_user, students_record=students_record, search=search, sex=sex)

@_faculty.route('/faculty_dashboard', methods=['GET'])
@login_required
def faculty_dashboard():
    
    # no_studs_desired_job_1 = db.session.query(User).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.desired_career == 'Software Engineer / Programmer').group_by(User.id).count()
    # no_studs_desired_job_2 = db.session.query(User).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.desired_career == 'Technical Support Specialist').group_by(User.id).count()
    # no_studs_desired_job_3 = db.session.query(User).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.desired_career == 'Academician').group_by(User.id).count()
    # no_studs_desired_job_4 = db.session.query(User).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.desired_career == 'Administrative Assistant').group_by(User.id).count()
    # overall_studs_desired_job = int(no_studs_desired_job_1 + no_studs_desired_job_2 + no_studs_desired_job_3 + no_studs_desired_job_4)
    
    no_studs_top_1_prediction_1 = db.session.query(User, PredictionResult).filter(PredictionResult.top_rank == 'Software Engineer / Programmer').group_by(PredictionResult.result_id).count()
    no_studs_top_1_prediction_2 = db.session.query(User, PredictionResult).filter(PredictionResult.top_rank == 'Technical Support Specialist').group_by(PredictionResult.result_id).count()
    no_studs_top_1_prediction_3 = db.session.query(User, PredictionResult).filter(PredictionResult.top_rank == 'Academician').group_by(PredictionResult.result_id).count()
    no_studs_top_1_prediction_4 = db.session.query(User, PredictionResult).filter(PredictionResult.top_rank == 'Administrative Assistant').group_by(PredictionResult.result_id).count()
    overall_studs_top_1_prediction = int(no_studs_top_1_prediction_1 + no_studs_top_1_prediction_2 + no_studs_top_1_prediction_3 + no_studs_top_1_prediction_4)
    
    # no_studs_met_their_desired_career = db.session.query(User).filter(User.desired_career == PredictionResult.top_rank).count()
    no_studs_met_their_desired_career = PredictionResult.query.filter(PredictionResult.desired_job.like('%' + PredictionResult.top_rank + '%')).group_by(PredictionResult.result_id).count()
    # print(no_studs_met_their_desired_career)
    
    cs_students = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.department == 'Computer Science', PredictionResult.user_id == User.id).group_by(User.id).count()
    it_students = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, User.department == 'Information Technology', PredictionResult.user_id == User.id).group_by(User.id).count()
    
    first_SE = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.top_rank == 'Software Engineer / Programmer', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    first_TSS = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.top_rank == 'Technical Support Specialist', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    first_A = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.top_rank == 'Academician', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    first_AA = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.top_rank == 'Administrative Assistant', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    
    software_engineer_programmer = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.desired_job == 'Software Engineer / Programmer', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    technical_support_specialist = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.predict_no >=1, User.user_type == 1, PredictionResult.desired_job == 'Technical Support Specialist', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    academician = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, PredictionResult.desired_job == 'Academician', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    administrative_assistant = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, PredictionResult.desired_job == 'Administrative Assistant', PredictionResult.user_id == User.id).group_by(PredictionResult.result_id).count()
    
    male = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.sex == 'Male', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    female = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.sex == 'Female', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    
    shiftee = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.program == 'Shiftee', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    transferee = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.program == 'Transferee', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    regular = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.program == 'Regular', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    
    registered_students = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).count()
    unregistered_students = db.session.query(User).filter(User.is_approve == 0, User.user_type == 1).count()
    
    if request.method == 'GET':
        # Current Logged User
        auth_user=current_user
        page = request.args.get('page', 1, type=int)

        # Data for search
        search = request.args.getlist('search')
        search = (','.join(search))
        
        department = request.args.getlist('department')
        department = (','.join(department))
        
        program = request.args.getlist('program')
        program = (','.join(program))
        
        sex = request.args.getlist('sex')
        sex = (','.join(sex))
        
        curriculum_year = request.args.getlist('curriculum_year')
        curriculum_year = (','.join(curriculum_year))
        print(search, department, sex, curriculum_year)
        # Data for filter department
        # Return Data for template
        
        if auth_user.user_type == -1 or auth_user.user_type == 0:
            
            if search:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).order_by(asc(PredictionResult.date_created))\
                    .filter((User.first_name.like('%' + search + '%'))      |
                    (User.middle_name.like('%' + search + '%'))     |
                    (User.last_name.like('%' + search + '%'))       |
                    (PredictionResult.desired_job.like('%' + search + '%'))|
                    (User.contact_number.like('%' + search + '%'))  |
                    (User.department.like('%' + search + '%'))    |
                    (User.curriculum_year.like('%' + search + '%'))    |
                    (User.email.like('%' + search + '%')))\
                    .paginate(page=page, per_page=5)# fetch user students only
            elif department:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).order_by(asc(PredictionResult.date_created))\
                    .filter((User.department.like('%' + department + '%')))\
                    .paginate(page=page, per_page=5)# fetch department only
            elif program:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).order_by(asc(PredictionResult.date_created))\
                    .filter((User.program.like('%' + program + '%')))\
                    .paginate(page=page, per_page=5)# fetch program only
            elif sex:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).order_by(asc(PredictionResult.date_created))\
                    .filter((User.sex==sex))\
                    .paginate(page=page, per_page=5)# fetch sex only
            elif curriculum_year:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(User.id).order_by(asc(PredictionResult.date_created))\
                    .filter((User.curriculum_year.like('%' + curriculum_year + '%')))\
                    .paginate(page=page, per_page=5)# fetch curriculum year only
            else:
                students_record = db.session.query(User, PredictionResult).filter(User.is_approve == 1, User.department != 'Faculty', User.predict_no >=1, PredictionResult.user_id == User.id).group_by(PredictionResult.user_id).order_by(asc(PredictionResult.date_created)).paginate(page=page, per_page=5)# fetch user students only
            
            auth_user=current_user
            curriculum_input = db.session.query(CurriculumResult).all()
            curriculum_record = db.session.query(CurriculumResult).all()
            unapprove_account = User.query.filter_by(is_approve = False, user_type = 1).all()
            count_unapprove = User.query.filter_by(is_approve = False, user_type = 1).count()
        else:
            return redirect(url_for('_auth.index'))
        
    else:  
        return redirect(url_for('_auth.index'))
    
    return render_template("Faculty/facultyEnd.html", auth_user=auth_user, 
                            students_record=students_record, overall_studs_top_1_prediction=overall_studs_top_1_prediction,
                            unapprove_account=unapprove_account, no_studs_met_their_desired_career=no_studs_met_their_desired_career,
                            count_unapprove=count_unapprove, search=search, curriculum_input=curriculum_input,
                            department=department, sex=sex, curriculum_year=curriculum_year, curriculum_record=curriculum_record,
                            software_engineer_programmer=json.dumps(software_engineer_programmer), technical_support_specialist=json.dumps(technical_support_specialist),
                            academician=json.dumps(academician), administrative_assistant=json.dumps(administrative_assistant),
                            male=json.dumps(male), female=json.dumps(female), registered_students=registered_students,
                            unregistered_students=unregistered_students, first_SE=json.dumps(first_SE), first_TSS=json.dumps(first_TSS),
                            first_A=json.dumps(first_A), first_AA=json.dumps(first_AA), cs_students = json.dumps(cs_students),
                            it_students = json.dumps(it_students), shiftee = json.dumps(shiftee), transferee = json.dumps(transferee),
                            regular = json.dumps(regular)
                            )

@_faculty.route('/view_results', methods=['POST'])
@login_required
def view_results():
    try:
        auth_user=current_user
        page = request.args.get('page', 1, type=int)
        
        view_pred_result = db.session.query(User, PredictionResult).filter(User.id == int(request.form['user_id'])).filter(PredictionResult.user_id == int(request.form['user_id'])).group_by(PredictionResult.result_id).order_by(asc(PredictionResult.date_created)).paginate(page=page, per_page=5)
        
        return render_template("Faculty/faculty_view.html", view_pred_result=view_pred_result, auth_user=auth_user)
    
    except:
        flash('System error cannot delete data', category='error')
        return redirect(url_for('.faculty_dashboard'))
    
    

@_faculty.route('/delete_results', methods=['POST'])
@login_required
def delete_results():
    try:
        delete_pred_result = delete(PredictionResult).where(PredictionResult.result_id == request.form['result_id'])
        db.session.execute(delete_pred_result)
        
        predict_iter = User.query.filter_by(id=int(request.form['user_id'])).first()
        val = predict_iter.predict_no
        predict_iter.predict_no = (val - 1)
        db.session.commit()

        flash('History successfully deleted', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))
    except:
        flash('System error cannot delete data', category='error')
        return redirect(url_for('.faculty_dashboard'))

@_faculty.route('/delete_student', methods=['POST'])
@login_required
def delete_student():
    try:
        delete_result = delete(User).where(User.id == request.form['user_id'])
        db.session.execute(delete_result)
        db.session.commit()
        flash('Student account successfully deleted', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))
    except:
        flash('Delete the prediction history first to delete account', category='error')
        return redirect(url_for('.faculty_dashboard'))
    
@_faculty.route('/delete_faculty', methods=['POST'])
@login_required
def delete_faculty():
    auth_user=current_user
    
    if auth_user.is_authenticated and auth_user.user_type == -1:
        try:
            delete_result = delete(User).where(User.id == request.form['user_id'])
            db.session.execute(delete_result)
            db.session.commit()
            flash('Faculty account successfully deleted', category='success_deletion')
            return redirect(url_for('.faculty_dashboard'))
        except:
            flash('System error cannot delete data please try again', category='error')
            return redirect(url_for('.faculty_dashboard'))
        
    flash('Sorry only the admin is permitted to delete some data', category='error')
    return redirect(url_for('.faculty_dashboard'))

@_faculty.route('/approve_account', methods=['POST'])
@login_required
def approve_account():
    if int(request.form['approve_flag']) == 1:
        approve_account = User.query.filter_by(id=int(request.form['user_id'])).first()
        approve_account.is_approve = True
        db.session.commit()
        # send_link(request.form['user_email'], request.form['user_department'])
        flash('Account successfully approved', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))
        
    elif int(request.form['approve_flag']) == 0:
        approve_account = delete(User).where(User.id == request.form['user_id'])
        approve_account.is_approve = False
        db.session.execute(approve_account)
        db.session.commit()
        # send_link_disapproved(request.form['user_email'])
        flash('Account successfully disapproved/deleted', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))

    return redirect(url_for('_faculty.faculty_dashboard'))

@_faculty.route('/delete_curriculum_year', methods=['POST'])
@login_required
def delete_curriculum_year():
    try:
        delete_result = delete(CurriculumResult).where(CurriculumResult.curriculum_id == request.form['curriculum_identity'])
        db.session.execute(delete_result)
        db.session.commit()
        flash('Curriculum Year successfully deleted', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))
    except:
        flash('Failed to deleted Curriculum Year', category='error')
        return redirect(url_for('.faculty_dashboard'))

@_faculty.route('/add_curriculum_year', methods=['POST'])
@login_required
def add_curriculum_year():
    auth_user=current_user
    date_added = datetime.now()
    get_created_by = User.query.filter_by(id=int(auth_user.id)).first()
    admin_created_by = get_created_by.first_name
    try:
        new_year = CurriculumResult(request.form['add_curriculum'], admin_created_by, date_created=date_added)
        db.session.add(new_year)
        db.session.commit()
        flash('Curriculum Year successfully created', category='success_deletion')
        return redirect(url_for('.faculty_dashboard'))
    except:
        flash('Failed to add Curriculum Year, Identical Input detected! Please try again', category='error')
        return redirect(url_for('.faculty_dashboard'))

@_faculty.route('/signup_Superadmin', methods=['POST'])
@login_required
def signup_Superadmin():
    first = request.form['first_name']
    middle = request.form['middle_name']
    last = request.form['last_name']
    
    if (first.isspace() != True or middle.isspace() != True or last.isspace() != True):
        try:
            new_user = User(request.form['first_name'], request.form['middle_name'], request.form['last_name'], request.form['sex'], '-------', request.form['contact_number'], request.form['email'], 'Faculty',  'Faculty', 'Not Applicable', (generate_password_hash(request.form['password'], method="sha256")), True, 0, 0)
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created', category='success_register')
        except:
            flash('Invalid credentials', category='error')  
    else:
        flash('Please enter necessary data in fields', category='error')
        
    return redirect(url_for('.register_faculty'))

# ROUTE FOR PIE CHART
@_faculty.route('/change_data_status', methods=['POST'])
@login_required
def change_data_status():
    status = db.session.query(User).filter(User.program != 'Not Applicable', User.predict_no >=1).group_by(User.program).all()
    data_dict_stat = {}
    for s in status:
        fetch_data = db.session.query(User)\
                    .filter(User.program == s.program)\
                    .filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1)\
                    .filter(User.department == request.form['department']).all()
        data_dict_stat.update({s.program: len(fetch_data)})
    return data_dict_stat

@_faculty.route('/change_data_sex', methods=['POST'])
@login_required
def change_data_sex():
    sex = db.session.query(User).filter(User.predict_no >=1).group_by(User.sex).all()
    data_dict_sex = {}
    for s in sex:
        fetch_data = db.session.query(User)\
                    .filter(User.program == request.form['status'])\
                    .filter(User.sex == s.sex)\
                    .filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1)\
                    .filter(User.department == request.form['department']).all()
        data_dict_sex.update({s.sex: len(fetch_data)})
    return data_dict_sex

@_faculty.route('/generate_names', methods=['POST'])
@login_required
def generate_names():
    data_dict_names = {}
    fetch_data = db.session.query(User)\
                .filter(User.program == request.form['status'])\
                .filter(User.sex == request.form['sex'])\
                .filter(User.is_approve == 1, User.user_type == 1, User.predict_no >=1)\
                .filter(User.department == request.form['department']).all()
    
    for name in fetch_data:
        fetch_result = db.session.query(PredictionResult)\
                .filter(PredictionResult.user_id == name.id).first()
        data_dict_names.update({name.id: {'fullname': str(name.first_name +' '+name.middle_name+' '+ name.last_name), 'desired_career': fetch_result.desired_job, 'main_rank': fetch_result.main_rank}})
    return data_dict_names