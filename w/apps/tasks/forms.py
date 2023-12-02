from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectMultipleField, validators
from flask_wtf import FlaskForm


class TaskForm(FlaskForm):
    name = StringField(
        'Name',
        [
            validators.DataRequired(message="This field is required."),
            validators.Length(min=5, max=64)
        ],
        render_kw={
            'placeholder': 'Production (Germany)',
            'class': 'form-control'
        }
    )
    url = StringField(
        'URL',
        [
            validators.DataRequired(message="This field is required."),
            validators.URL()
        ],
        render_kw={
            'placeholder': 'https://foo.com',
            'class': 'form-control'
        }
    )
    username = StringField(
        'Username',
        render_kw={
            'placeholder': 'foo',
            'class': 'form-control'
        }
    )
    password = PasswordField(
        'Password',
        render_kw={
            'placeholder': 'FooPassword',
            'class': 'form-control'
        }
    )
    headers = TextAreaField(
        'Headers',
        render_kw={
            'placeholder': '{"Authorization": "Bearer qsdassd"}',
            'class': 'form-control'
        }
    )
    data = TextAreaField(
        'Data',
        render_kw={
            'placeholder': '{"foo": "bar"}',
            'class': 'form-control'
        }
    )
    return_codes = StringField(
        'Return Codes',
        render_kw={
            'placeholder': '200,201',
            'class': 'form-control'
        }
    )
    agents = SelectMultipleField(
        'Agents',
        render_kw={
            'data-placeholder': 'Select Agent(s)',
            'class': 'form-select'
        },
        choices=[],
        coerce=int
    )
    period = IntegerField(
        'Period',
        [
            validators.DataRequired(message="This field is required.")
        ],
        render_kw={
            'placeholder': '20',
            'class': 'form-control'
        },
        default=20
    )
    task_type = StringField(default="http")


class TCPTaskForm(FlaskForm):
    name = StringField(
        'Name',
        [
            validators.DataRequired(message="This field is required."),
            validators.Length(min=5, max=64)
        ],
        render_kw={
            'placeholder': 'Production (Germany)',
            'class': 'form-control'
        }
    )
    ip_address = StringField(
        'IP Address',
        [
            validators.DataRequired(message="This field is required."),
            validators.IPAddress()
        ],
        render_kw={
            'placeholder': '192.168.2.20',
            'class': 'form-control'
        }
    )
    port = StringField(
        'Port',
        [
            validators.DataRequired(message="This field is required."),
            validators.Regexp(regex="^[1-6][0-9]{,4}$")
        ],
        render_kw={
            'placeholder': '5432',
            'class': 'form-control'
        }
    )
    agents = SelectMultipleField(
        'Agents',
        render_kw={
            'data-placeholder': 'Select Agent(s)',
            'class': 'form-select'
        },
        choices=[],
        coerce=int
    )
    period = IntegerField(
        'Period',
        [
            validators.DataRequired(message="This field is required.")
        ],
        render_kw={
            'placeholder': '20',
            'class': 'form-control'
        },
        default=20
    )
    task_type = StringField(default="tcp")
