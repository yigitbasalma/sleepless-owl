from sqlalchemy import event
from sqlalchemy.dialects.mysql import NVARCHAR

from flask_login import UserMixin
from flask_authorize import AllowancesMixin

from w import db, Base
from w.helpers.x_tools import generate_id

INITIAL_ROLE_DATA = [
    dict(
        name="admin",
        allowances=dict(),
        description="Admin role."
    ),
    dict(
        name="user",
        allowances=dict(),
        description="Standard user role."
    )
]

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE")),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Users(Base, UserMixin):
    user_id = db.Column(NVARCHAR(12), unique=True)
    first_name = db.Column(NVARCHAR(64), nullable=False)
    last_name = db.Column(NVARCHAR(64), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    # Relations
    roles = db.relationship("Roles", secondary=UserRole, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.user_id = generate_id()
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User ("{self.user_id}")>'

    def is_active(self):
        return self.status == "active"

    def has_role(self, role_name):
        return role_name in [i.name for i in self.roles]

    @property
    def human_readable_roles(self):
        return ",".join([i.name.replace("_", " ").title() for i in self.roles])


class Roles(db.Model, AllowancesMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super(Roles, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Role ("{self.name}")>'


def create_initial_roles(*_, **__):
    # Create initial roles
    for role in INITIAL_ROLE_DATA:
        db.session.add(Roles(**role))

    db.session.commit()


event.listen(Roles.__table__, "after_create", create_initial_roles)
