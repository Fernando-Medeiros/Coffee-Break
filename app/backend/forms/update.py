from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField, StringField, DateField
from wtforms.validators import DataRequired, Length, Email, Optional


class FormUploadAvatar(FlaskForm):
    avatar = FileField(
        "Upload",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only"),
        ],
    )


class FormUploadBackground(FlaskForm):
    background = FileField(
        "Upload",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only"),
        ],
    )


class FormUpdateBio(FlaskForm):
    content = TextAreaField(validators=[DataRequired(), Length(3, 254)])

    def dict(self) -> dict:
        return {"bio": self.content.data}


class FormUpdateAccount(FlaskForm):
    first_name = StringField("Nome", validators=[Optional()])
    last_name = StringField("Sobrenome", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])

    def dict(self) -> dict:
        return {
            "first_name": self.first_name.data,
            "last_name": self.last_name.data,
            "email": self.email.data,
        }


class FormUpdateBirthday(FlaskForm):
    date = DateField("Data de nascimento", validators=[Optional()])

    def dict(self) -> dict:
        return {
            "day": self.date.data.day,
            "month": self.date.data.month,
            "year": self.date.data.year,
        }
