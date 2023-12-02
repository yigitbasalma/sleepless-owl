from flask import Blueprint, render_template, jsonify
from flask_login import login_required

from w import app, authorize
from w.apps.tasks.models import Tasks

from .models import Providers, Rules
from .forms import ProviderForm, RuleForm
from .controllers import (
    create_new_provider,
    create_new_rule,
    delete_rule_func,
    delete_provider_func,
    update_provider_func,
    update_rule_func
)

notification = Blueprint("notification", __name__, url_prefix="/notification")


@notification.route("/", methods=["GET", "POST"])
@login_required
@authorize.has_role("admin")
def index():
    provider_form = ProviderForm()
    provider_form.provider_name.choices.extend(
        [
            (k, k.title(), {"data-img": k})
            for k in app.config["NOTIFICATION_PROVIDERS"].keys()
        ]
    )
    rule_form = RuleForm()
    rule_form.provider_id.choices.extend(
        [
            (k.id, k.name.title(), {"data-img": k.provider_name})
            for k in Providers.all(conditions=[])
        ]
    )
    rule_form.tasks.choices.extend(
        [
            (k.id, k.name)
            for k in Tasks.all(conditions=[])
        ]
    )

    return render_template(
        "notification/notification.html",
        providers=Providers.all(conditions=[]),
        rules=Rules.all(conditions=[]),
        provider_form=provider_form,
        rule_form=rule_form
    )


@notification.route("/provider", methods=["POST"])
@login_required
@authorize.has_role("admin")
def create_provider():
    provider_form = ProviderForm()
    provider_form.provider_name.choices.extend(
        [
            (k, k.title())
            for k in app.config["NOTIFICATION_PROVIDERS"].keys()
        ]
    )

    if provider_form.validate_on_submit():
        return create_new_provider(form=provider_form)

    _errors = []
    for fieldName, errorMessages in provider_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{provider_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@notification.route("/provider/<int:provider_id>/update", methods=["POST"])
@login_required
@authorize.has_role("admin")
def update_provider(provider_id):
    provider_form = ProviderForm()
    delattr(provider_form, "provider_name")

    if provider_form.validate_on_submit():
        return update_provider_func(form=provider_form, provider_id=provider_id)

    _errors = []
    for fieldName, errorMessages in provider_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{provider_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@notification.route("/provider/<int:provider_id>/delete", methods=["GET"])
@login_required
@authorize.has_role("admin")
def delete_provider(provider_id):
    return delete_provider_func(provider_id=provider_id)


@notification.route("/rule", methods=["POST"])
@login_required
@authorize.has_role("admin")
def create_rule():
    rule_form = RuleForm()
    rule_form.provider_id.choices.extend(
        [
            (k.id, k.name.title(), {"data-img": k.provider_name})
            for k in Providers.all(conditions=[])
        ]
    )
    rule_form.tasks.choices.extend(
        [
            (k.id, k.name)
            for k in Tasks.all(conditions=[])
        ]
    )

    if rule_form.validate_on_submit():
        return create_new_rule(form=rule_form)

    _errors = []
    for fieldName, errorMessages in rule_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{rule_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@notification.route("/rule/<int:rule_id>/update", methods=["POST"])
@login_required
@authorize.has_role("admin")
def update_rule(rule_id):
    rule_form = RuleForm()
    rule_form.tasks.choices.extend(
        [
            (k.id, k.name)
            for k in Tasks.all(conditions=[])
        ]
    )
    delattr(rule_form, "provider_id")

    if rule_form.validate_on_submit():
        return update_rule_func(form=rule_form, rule_id=rule_id)

    _errors = []
    for fieldName, errorMessages in rule_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{rule_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@notification.route("/rule/<int:rule_id>/delete", methods=["GET"])
@login_required
@authorize.has_role("admin")
def delete_rule(rule_id):
    return delete_rule_func(rule_id=rule_id)
