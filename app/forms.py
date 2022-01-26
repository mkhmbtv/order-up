from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    SelectMultipleField,
    StringField, SubmitField,
    PasswordField
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    employee_number = StringField('Employee number', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


class TableAssignementForm(FlaskForm):
    tables = SelectField('Tables', coerce=int)
    servers = SelectField('Servers', coerce=int)
    assign = SubmitField('Assign')


class MenuItemAssignementForm(FlaskForm):
    menu_item_ids = SelectMultipleField('Menu Items', coerce=int)
