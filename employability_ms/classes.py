from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, FileField, HiddenField
from wtforms.validators import ValidationError, DataRequired, InputRequired, Email

class UploadCSV(FlaskForm):
    # csrf_ = HiddenField(id="csrf_token", name="csrf_token", default="{{ csrf_token() }}")
    file = FileField(label=('File'), id="pic_input", name="pic_input", render_kw={'@input':'onSelectedFile'})
    # submit = SubmitField(label=('Submit'))