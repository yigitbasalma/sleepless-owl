from sqlalchemy.dialects.mysql import NVARCHAR

from w import db, Base


AgentTasks = db.Table(
    'agent_tasks', db.Model.metadata,
    db.Column('agent_id', db.Integer, db.ForeignKey('agents.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id', ondelete="CASCADE"))
)


class Tasks(Base):
    name = db.Column(NVARCHAR(64), unique=True)
    # Statuses: unknown, up, down, partial
    status = db.Column(NVARCHAR(16), default="unknown")
    # Check period, min 20 seconds
    period = db.Column(db.Integer)

    # Certificate info
    cert_valid = db.Column(db.String(16), default="unknown")
    cert_valid_until = db.Column(db.DateTime)

    # Types: http, https, tcp
    type = db.Column(NVARCHAR(32))

    # Http/Https type configs
    url = db.Column(NVARCHAR(512))
    username = db.Column(NVARCHAR(64))
    password = db.Column(NVARCHAR(64))
    headers = db.Column(NVARCHAR(512))
    data = db.Column(NVARCHAR(512))
    return_codes = db.Column(NVARCHAR(64))
    reverse_check = db.Column(NVARCHAR(12), default="False")  # Upside down

    # TCP type config
    ip_address = db.Column(NVARCHAR(128))
    port = db.Column(db.Integer)

    # Maintenance config
    maintenance_active = db.Column(NVARCHAR(12), default="False")
    maintenance_since = db.Column(db.DateTime)
    maintenance_until = db.Column(db.DateTime)

    # Relations
    agents = db.relationship("Agents", secondary=AgentTasks, backref=db.backref('Tasks', lazy='dynamic'))
    agent_metrics = db.relationship("AgentMetrics", cascade="delete")
    agent_task_states = db.relationship("AgentTaskStates", cascade="delete")
    agent_task_logs = db.relationship("AgentTaskLogs", cascade="delete")

    def __init__(self, **kwargs):
        super(Tasks, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Task ("{self.id}")>'
