from wtforms import StringField, PasswordField, validators
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        [
            validators.DataRequired(message="This field is required."),
            validators.Email()
        ],
        render_kw={
            'placeholder': 'jd@company.foo',
            'class': 'form-control',
            'aria-describedby': 'email',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    password = PasswordField(
        'Password',
        [
            validators.DataRequired(message="This field is required.")
        ],
        render_kw={
            'placeholder': '************',
            'class': 'form-control form-control-merge',
            'aria-describedby': 'password',
            'tabindex': '2'
        }
    )


class RegisterForm(FlaskForm):
    first_name = StringField(
        'First Name',
        [
            validators.DataRequired(),
            validators.Length(min=3, max=64)
        ],
        render_kw={
            'placeholder': 'John/Jane',
            'class': 'form-control',
            'aria-describedby': 'text',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    last_name = StringField(
        'Last Name',
        [
            validators.DataRequired(),
            validators.Length(min=3, max=64)
        ],
        render_kw={
            'placeholder': 'Doe',
            'class': 'form-control',
            'aria-describedby': 'text',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    email = StringField(
        'Email',
        [
            validators.DataRequired(),
            validators.Email()
        ],
        render_kw={
            'placeholder': 'jd@company.foo',
            'class': 'form-control',
            'aria-describedby': 'email',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    password = PasswordField(
        'Password',
        [
            validators.DataRequired(),
            validators.EqualTo('confirm_password', message='Passwords must match')
        ],
        render_kw={
            'placeholder': '************',
            'class': 'form-control form-control-merge',
            'aria-describedby': 'password',
            'tabindex': '2'
        }
    )
    confirm_password = PasswordField(
        'Confirm Password',
        [
            validators.DataRequired()
        ],
        render_kw={
            'placeholder': '************',
            'class': 'form-control form-control-merge',
            'aria-describedby': 'password',
            'tabindex': '2'
        }
    )
