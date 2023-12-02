from datetime import datetime

from sqlalchemy.exc import IntegrityError

from w import db, celery
from w.apps.tasks.models import Tasks
from w.apps.agents.models import AgentMetrics, AgentTaskStates


@celery.task
def track():
    for task in Tasks.all(conditions=[]):
        # Variables
        failed_agents = []

        for agent in task.agents:
            last_send_from_agent = AgentMetrics.all(conditions=[
                AgentMetrics.task_id == task.id, AgentMetrics.agent_id == agent.id
            ], limit=1)

            if not last_send_from_agent or \
                    (datetime.now() - last_send_from_agent[0].created_at).total_seconds() > task.period + 5:
                failed_agents.append(True)

                try:
                    db.session.add(
                        AgentTaskStates(
                            agent_id=agent.id,
                            task_id=task.id,
                            state="error"
                        )
                    )
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    agent_task_state = AgentTaskStates.first(conditions=[
                        AgentTaskStates.agent_id == agent.id, AgentTaskStates.task_id == task.id
                    ])
                    agent_task_state.state = "error"
                    db.session.commit()

            elif last_send_from_agent[0].value == 0:
                failed_agents.append(True)
            else:
                failed_agents.append(False)

        if all(failed_agents):
            task.status = "down"
        elif any(failed_agents):
            task.status = "partial"
        else:
            task.status = "up"

        db.session.commit()
