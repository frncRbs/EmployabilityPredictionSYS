from sqlalchemy.sql import func
from sqlalchemy import column, func
from . import db, marsh, app
from flask_login import UserMixin

from marshmallow import Schema, fields

class UserSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'sex', 'curriculum_year', 'contact_number', 'email', 'desired_career', 'department', 'program', 'top_rank', 'password', 'is_approve', 'predict_no', 'user_type')
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(150), nullable=False)
    curriculum_year = db.Column(db.String(150), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    desired_career = db.Column(db.String(150), nullable=False) 
    department = db.Column(db.String(150), nullable=False)
    program = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_approve = db.Column(db.Boolean, nullable=False, default=0)
    predict_no = db.Column(db.SmallInteger, nullable=False, default=1)
    user_type = db.Column(db.SmallInteger, nullable=False, default=1) # -1 Superadmin(Built-in), 0 - Admin, 1 - Personnel
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    pred_results = db.relationship('PredictionResult', backref='user', uselist=False)

    def __init__(self, first_name, middle_name, last_name, sex, curriculum_year, contact_number, email, desired_career, department, program, password, is_approve, predict_no, user_type):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.curriculum_year = curriculum_year
        self.contact_number = contact_number
        self.email = email
        self.desired_career = desired_career 
        self.department = department 
        self.program = program
        self.password = password
        self.is_approve = is_approve
        self.predict_no = predict_no
        self.user_type = user_type

class PredictionResultSchema(marsh.Schema):
    class Meta:
        fields = ('result_id', 'desired_job', 'top_rank', 'main_rank', 'sub_rank1', 'sub_rank2', 'sub_rank3', 'user_id', 'date_created')

class PredictionResult(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    desired_job = db.Column(db.String(150), nullable=True)
    top_rank = db.Column(db.String(150), nullable=False)    
    main_rank = db.Column(db.String(255), nullable=False)
    sub_rank1 = db.Column(db.String(255), nullable=False)
    sub_rank2 = db.Column(db.String(255), nullable=False)
    sub_rank3 = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, desired_job, top_rank, main_rank, sub_rank1, sub_rank2, sub_rank3, user_id, date_created):
        self.desired_job = desired_job
        self.top_rank = top_rank
        self.main_rank = main_rank
        self.sub_rank1 = sub_rank1
        self.sub_rank2 = sub_rank2
        self.sub_rank3 = sub_rank3
        self.user_id = user_id
        self.date_created = date_created
        
class CurriculumSchema(marsh.Schema):
    class Meta:
        fields = ('curriculum_id', 'curriculum_year', 'created_by')
        
class CurriculumResult(db.Model):
    curriculum_id = db.Column(db.Integer, primary_key=True)
    curriculum_year = db.Column(db.String(150), unique=True, nullable=True)
    created_by = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, curriculum_year, created_by, date_created):
        self.curriculum_year = curriculum_year
        self.created_by = created_by
        self.date_created = date_created