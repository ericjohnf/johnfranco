from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email
from wtforms.fields import TextField, TextAreaField, PasswordField, BooleanField, RadioField, HiddenField, SelectField

class ArtForm(Form):
    title = TextField("title")
    medium = TextField("medium")
    show = TextField("show")
    price = TextField("price")
    height = TextField("height")    
    width = TextField("width")    