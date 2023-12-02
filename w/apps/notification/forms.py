from wtforms import TextAreaField, StringField, SelectField, SelectMultipleField, validators
from flask_wtf import FlaskForm


class ProviderForm(FlaskForm):
    provider_name = SelectField(
        'Provider Name',
        [
            validators.DataRequired()
        ],
        render_kw={
            'class': 'form-select'
        },
        choices=list()
    )
    name = StringField(
        'Channel Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=128)
        ],
        render_kw={
            'placeholder': 'Foo company slack',
            'class': 'form-control',
            'aria-describedby': 'text',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    config = TextAreaField(
        'Config',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=512)
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': '',
            'tabindex': '1',
            'style': 'height: 100px'
        }
    )


class RuleForm(FlaskForm):
    name = StringField(
        'Name',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=128)
        ],
        render_kw={
            'placeholder': 'Foo alert',
            'class': 'form-control',
            'aria-describedby': 'text',
            'autofocus': '',
            'tabindex': '1'
        }
    )
    provider_id = SelectField(
        'Provider Name',
        [
            validators.DataRequired()
        ],
        render_kw={
            'class': 'form-select'
        },
        choices=list(),
        coerce=int
    )
    config = TextAreaField(
        'Config',
        [
            validators.DataRequired(),
            validators.Length(min=2, max=512)
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': '',
            'tabindex': '1',
            'style': 'height: 100px'
        }
    )
    tasks = SelectMultipleField(
        'Tasks',
        [
            validators.DataRequired()
        ],
        render_kw={
            'class': 'form-select-without-img'
        },
        choices=list(),
        coerce=int
    )
