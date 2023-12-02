from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import NVARCHAR

from w import db, Base

NotificationRuleTaskPair = db.Table(
    'notification_rule_task_pair', db.Model.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('rule_id', db.Integer, db.ForeignKey('rules.id'))
)


class Providers(Base):
    name = db.Column(NVARCHAR(64))
    config = db.Column(NVARCHAR(512))
    provider_name = db.Column(NVARCHAR(64))
    provider_image = db.Column(NVARCHAR(64))

    # Unique Constraints
    UniqueConstraint(name, provider_name)

    # Relations
    rules = db.relationship("Rules", back_populates="providers")

    def __init__(self, **kwargs):
        super(Providers, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Provider ("{self.id}")>'


class Rules(Base):
    name = db.Column(NVARCHAR(64))
    provider_id = db.Column(db.Integer, db.ForeignKey("providers.id", ondelete="CASCADE"))
    config = db.Column(NVARCHAR(512))

    # Unique Constraints
    UniqueConstraint(name, provider_id, config)

    # Relations
    providers = db.relationship("Providers", back_populates="rules")
    tasks = db.relationship("Tasks", secondary=NotificationRuleTaskPair, backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Rules, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Rule ("{self.id}")>'


class AlertHash(Base):
    alert_hash = db.Column(NVARCHAR(256))
    expire = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(AlertHash, self).__init__(**kwargs)

    def __repr__(self):
        return f'<AlertHash ("{self.id}")>'
