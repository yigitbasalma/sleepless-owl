from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask import url_for
from flask_login import login_user, logout_user

from w import db
from w.helpers.x_tools import calculate_hash, response_create

from .models import Users, Roles


def login_customer_user(form):
    user_email = form.email.data
    user_password = calculate_hash(form.password.data)

    user = Users().first([
        Users.email == user_email,
        Users.password == user_password
    ])

    if not user:
        return response_create(
            data=dict(
                status="error",
                message="Incorrect username/password."
            )
        )

    login_user(
        user=user,
        duration=timedelta(days=30)
    )

    return response_create(
        data=dict(
            status="success",
            message="Successful login.",
            redirect=url_for("dashboard.index")
        )
    )


def register_customer_user(form):
    first_name = form.first_name.data.title()
    last_name = form.last_name.data.upper()
    email = form.email.data
    password = calculate_hash(form.password.data)

    # User count
    _users = Users.all(conditions=[])
    role_name = "user" if len(_users) > 0 else "admin"

    # Create user
    try:
        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            roles=[Roles.query.filter(Roles.name == role_name).first()]
        )
        db.session.add(user)
    except IntegrityError:
        return response_create(
            data=dict(
                status="error",
                message=f"Something went wrong."
            )
        )

    db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Your account is created.",
            redirect=url_for("index.welcome")
        )
    )


def logout_customer_user():
    logout_user()

    return response_create(
        data=dict(
            status="success"
        ),
        response_code=301,
        headers=dict(Location=url_for("index.welcome"))
    )
