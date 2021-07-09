from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User,Admin,Item


    
class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    Admin_key = PasswordField(label='Admin key:')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log in')



class AddSensorForm(FlaskForm):

	"""def validate_username(self, username_to_check):
		item = Item.query.filter_by(name=username_to_check.data).first()
		if Item:
			raise ValidationError('Name already exists! Please try a different name')"""

	soil_moisture = StringField(label='Soil moisture:', validators=[DataRequired()])
	status = StringField(label='status:', validators=[DataRequired()])
	time = StringField(label='time:', validators=[DataRequired()])
	sensor_location = StringField(label='sensor location:', validators=[DataRequired()])
	submit = SubmitField(label='Add Sensor')

class UpdateSensorForm(FlaskForm):

	id_ = IntegerField(label='Sensor id:', validators=[DataRequired()])
	soil_moisture = StringField(label='Soil moisture:', validators=[DataRequired()])
	status = StringField(label='status:', validators=[DataRequired()])
	time = StringField(label='time:', validators=[DataRequired()])
	sensor_location = StringField(label='sensor location:', validators=[DataRequired()])
	submit = SubmitField(label='Update Sensor')

class DeleteSensorForm(FlaskForm):

	id_ = IntegerField(label='Sensor Id:', validators=[DataRequired()])
	submit = SubmitField(label='delete Sensor')

		

class DeleteAdminForm(FlaskForm):

	
	name = StringField(label='Sensor Name:', validators=[DataRequired()])
	submit = SubmitField(label='delete Account')

	
	

    