from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email


class EmailPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class LoginForm(EmailPasswordForm):
    submit = SubmitField("Login")


class RegisterForm(EmailPasswordForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class AddToCartForm(FlaskForm):
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Add to Cart")
