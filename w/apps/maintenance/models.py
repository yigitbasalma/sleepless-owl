from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import NVARCHAR

from w import db, Base

MaintenanceRuleTaskPair = db.Table(
    'maintenance_rule_task_pair', db.Model.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('rule_id', db.Integer, db.ForeignKey('maintenance_rules.id'))
)


class MaintenanceRules(Base):
    name = db.Column(NVARCHAR(64))
    completed = db.Column(NVARCHAR(12), default="False")

    # Types: regular, cron
    type = db.Column(NVARCHAR(32))

    # For regular maintenance
    since = db.Column(db.DateTime)
    until = db.Column(db.DateTime)
    duration = db.Column(db.Integer)

    # For cron maintenance
    expression = db.Column(NVARCHAR(32))

    # Unique Constraints
    UniqueConstraint(name, type)

    # Relations
    tasks = db.relationship("Tasks", secondary=MaintenanceRuleTaskPair, backref=db.backref('maintenance_rules', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(MaintenanceRules, self).__init__(**kwargs)

    def __repr__(self):
        return f'<MaintenanceRule ("{self.id}")>'
