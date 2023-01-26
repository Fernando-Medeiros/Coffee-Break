from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField("Lembrar-me")


class FormNewAccount(FlaskForm):
    first_name = StringField("Nome", validators=[DataRequired()])
    last_name = StringField("Sobrenome", validators=[DataRequired()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    auth = PasswordField(
        "Confirmação da senha",
        validators=[DataRequired(), EqualTo("password")],
    )


class FormSendToken(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])


class FormNewPassword(FlaskForm):
    password = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    auth = PasswordField(
        "Confirmação da senha",
        validators=[DataRequired(), EqualTo("password")],
    )
