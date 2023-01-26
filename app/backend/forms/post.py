from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length


class FormPost(FlaskForm):
    content = TextAreaField(validators=[DataRequired(), Length(3, 999)])
