from w import db
from w.helpers.x_tools import response_create
from w.apps.auth.models import Users, Roles


def delete_user_func(user_id):
    user = Users.first(conditions=[Users.user_id == user_id])

    if user:
        admin_users = Users.all(conditions=[Users.roles.any(name="admin")])

        if len(admin_users) == 1 and user.roles[0].name in ("admin", ):
            return response_create(
                data=dict(
                    status="error",
                    message="You have only one admin user."
                )
            )

        db.session.delete(user)
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="User removed.",
            refresh=True
        )
    )


def toggle_user_role_func(user_id):
    user = Users.first(conditions=[Users.user_id == user_id])
    role_name = "Undefined user"

    if user:
        admin_users = Users.all(conditions=[Users.roles.any(name="admin")])

        if len(admin_users) == 1 and user.roles[0].name in ("admin", ):
            return response_create(
                data=dict(
                    status="error",
                    message="You have only one admin user."
                )
            )

        role_name = "user" if user.roles[0].name in ("admin", ) else "admin"
        user.roles = [Roles.query.filter(Roles.name == role_name).first()]
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message=f"User role changed to {role_name.title()}.",
            refresh=True
        )
    )
