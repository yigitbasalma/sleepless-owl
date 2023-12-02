from wtforms import StringField, SelectMultipleField, validators
from flask_wtf import FlaskForm


class RegularMaintenanceForm(FlaskForm):
    name = StringField(
        'Name',
        [
            validators.DataRequired(message="This field is required."),
            validators.Length(min=5, max=64)
        ],
        render_kw={
            'placeholder': 'Site upgrade',
            'class': 'form-control'
        }
    )
    since = StringField(
        'Start time',
        [
            validators.DataRequired(message="This field is required.")
        ],
        render_kw={
            'placeholder': 'Maintenance start time',
            'class': 'form-control datetime-pick'
        }
    )
    until = StringField(
        'End time',
        [
            validators.DataRequired(message="This field is required.")
        ],
        render_kw={
            'placeholder': 'Maintenance end time',
            'class': 'form-control datetime-pick'
        }
    )
    tasks = SelectMultipleField(
        'Tasks',
        render_kw={
            'data-placeholder': 'Select Task(s)',
            'class': 'form-select'
        },
        choices=[],
        coerce=int
    )
    task_type = StringField(default="regular")
