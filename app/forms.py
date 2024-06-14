from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, StringField, TextAreaField, DateField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('sponsor', 'Sponsor'), ('influencer', 'Influencer')], 
                       validators=[DataRequired()])
    submit = SubmitField('Register')

class ApproveSponsorForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Approve')

class FlagForm(FlaskForm):
    submit = SubmitField('Flag')

class CampaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    goals = TextAreaField('Goals')
    submit = SubmitField('Submit')

class AdRequestFormSponsor(FlaskForm):
    influencer_id = StringField('Influencer ID', validators=[DataRequired()])
    messages = TextAreaField('Messages')
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    category = StringField('Category')
    niche = StringField('Niche')
    reach = FloatField('Reach')
    submit = SubmitField('Update Profile')

class AdRequestFormInfluencer(FlaskForm):
    sponsor_id = StringField('Sponsor ID', validators=[DataRequired()])
    messages = TextAreaField('Messages')
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')