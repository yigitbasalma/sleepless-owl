from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import NVARCHAR, FLOAT

from w import db, Base
from w.helpers.x_tools import generate_token


class Agents(Base):
    name = db.Column(NVARCHAR(64), unique=True)
    location = db.Column(NVARCHAR(32))
    token = db.Column(NVARCHAR(256), unique=True)
    last_seen = db.Column(db.DateTime)
    color = db.Column(db.String(32))

    # Relations
    agent_metrics = db.relationship("AgentMetrics", back_populates="agents")

    def __init__(self, **kwargs):
        self.token = generate_token()
        super(Agents, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Agent ("{self.id}")>'


class AgentMetrics(Base):
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"))
    value = db.Column(FLOAT)

    # Relations
    agents = db.relationship("Agents", back_populates="agent_metrics")

    def __init__(self, **kwargs):
        super(AgentMetrics, self).__init__(**kwargs)

    def __repr__(self):
        return f'<AgentMetric ("{self.id}")>'


class AgentTaskStates(Base):
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"))
    state = db.Column(db.String(12))

    # Relations
    agent = db.relationship("Agents", backref="agent_task_states")

    # Unique constraints
    UniqueConstraint(agent_id, task_id)

    def __init__(self, **kwargs):
        super(AgentTaskStates, self).__init__(**kwargs)

    def __repr__(self):
        return f'<AgentTaskState ("{self.id}")>'


class AgentTaskLogs(Base):
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"))
    log = db.Column(db.String(512))
    count = db.Column(db.Integer, default=0)

    # Relations
    agent = db.relationship("Agents", backref="agent_task_logs")

    # Unique constraints
    UniqueConstraint(agent_id, log)

    def __init__(self, **kwargs):
        super(AgentTaskLogs, self).__init__(**kwargs)

    def __repr__(self):
        return f'<AgentTaskLog ("{self.id}")>'
