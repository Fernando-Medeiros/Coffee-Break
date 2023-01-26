from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField("Lembrar-me")

    def dict(self) -> dict:
        return {
            "username": self.email.data,
            "password": self.password.data,
            "remember": self.remember.data,
        }


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

    def dict(self) -> dict:
        return {
            "first_name": self.first_name.data,
            "last_name": self.last_name.data,
            "username": self.username.data,
            "email": self.email.data,
            "password": self.password.data,
            "auth": self.auth.data,
        }


class FormSendToken(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def dict(self) -> dict:
        return {"email": self.email.data}


class FormNewPassword(FlaskForm):
    password = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    confirm = PasswordField(
        "Confirmação da senha",
        validators=[DataRequired(), EqualTo("password")],
    )

    def dict(self) -> dict:
        return {"password": self.password.data, "confirm": self.confirm.data}
