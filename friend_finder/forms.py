from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import User


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    key = StringField('SignUp Key', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    school = StringField("Your Kid's School", validators=[DataRequired()])
   
    # myChoices = school_list
    # school = SelectField(u'Field name', choices = myChoices, validators = [DataRequired()])
    grade = StringField("Your Kid's Grade", validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    #signup_keys = ['12345', '23456', '34567', 'abcde', 'bcdef']

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError(f'Name {name} is already taken. Please use a different name.')
        
    # def validate_key(self, key):
    #     signup_keys = [12345, 23456, 34567, 'abcde', 'bcdef']
    #     key = User.query.filter_by(key=key.data).first()
    #     if key not in signup_keys:
    #         raise ValidationError("forms.py: Not a valid signup key. Please contact your child's school to obtain a valid key.")



    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('A user with that email address already exists. Please use a different email address.')
        


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class PostForm(FlaskForm):
    title = StringField('Title')
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=400)])
    submit = SubmitField('Submit')

    

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# class UpdateForm(FlaskForm):
#     submit = SubmitField('Update Post')


# class DeleteForm(FlaskForm):
#     submit = SubmitField('Delete Post')


class SchoolForm(FlaskForm):
    city = StringField('City')
    state = StringField('State-Code  Ex:NY')
    submit = SubmitField('Submit')