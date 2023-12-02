from wtforms import StringField, validators
from flask_wtf import FlaskForm


class AgentForm(FlaskForm):
    name = StringField(
        'Agent Name',
        [
            validators.DataRequired(message="This field is required."),
            validators.Length(min=5, max=64)
        ],
        render_kw={
            'placeholder': 'London Branch',
            'class': 'form-control',
            'aria-describedby': 'name',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    location = StringField(
        'Agent Location',
        [
            validators.DataRequired(message="This field is required."),
            validators.Length(min=5, max=32)
        ],
        render_kw={
            'placeholder': 'London/England',
            'class': 'form-control',
            'aria-describedby': 'location',
            'autofocus': '',
            'tabindex': '1'
        }
    )
