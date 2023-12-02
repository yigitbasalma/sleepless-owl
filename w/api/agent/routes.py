import logging
import datetime

from flask_restful import Resource, request
from sqlalchemy.exc import IntegrityError

from w import db
from w.helpers.x_tools import response_create
from w.apps.agents.models import Agents, AgentMetrics, AgentTaskStates, AgentTaskLogs
from w.apps.tasks.models import Tasks

LOGGER = logging.getLogger("api.agent")


class AgentPing(Resource):
    # Register resources
    endpoints = [
        "/agent/ping"
    ]

    @staticmethod
    def get():
        token = request.headers.get("Authorization")

        agent = Agents.first(
            conditions=[Agents.token == token],
        )

        if agent:
            agent.last_seen = datetime.datetime.now()
            db.session.commit()
            return response_create(data=dict(pong=True))

        return response_create(data=dict(error=True, message="You have to set 'Authorization' header in your request."),
                               response_code=401)


class AgentMetric(Resource):
    # Register resources
    endpoints = [
        "/agent/metric"
    ]

    @staticmethod
    def get():
        token = request.headers.get("Authorization")

        agent = Agents.first(
            conditions=[Agents.token == token],
        )

        if agent:
            return [i.as_dict() for i in Tasks.all(conditions=[Tasks.agents.any(id=agent.id)])]

        return response_create(data=dict(error=True, message="You have to set 'Authorization' header in your request."),
                               response_code=401)

    @staticmethod
    def post():
        token = request.headers.get("Authorization")

        agent = Agents.first(
            conditions=[Agents.token == token],
        )

        if agent:
            # Get request
            request_body = request.get_json()

            if not Tasks.first(conditions=[Tasks.agents.any(id=agent.id), Tasks.id == request_body["task_id"]]):
                return response_create(
                    data=dict(error=True, message="This agent is not part of this task."),
                    response_code=401)

            if request_body.get("error"):
                # Log error
                try:
                    db.session.add(
                        AgentTaskLogs(
                            agent_id=agent.id,
                            task_id=request_body["task_id"],
                            log=request_body["error"]
                        )
                    )
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    log = AgentTaskLogs.first(conditions=[AgentTaskLogs.agent_id == agent.id,
                                                          AgentTaskLogs.log == request_body["error"]])
                    log.count += 1
                    db.session.commit()

                # If agent state not found, create agent state
                try:
                    db.session.add(
                        AgentTaskStates(
                            agent_id=agent.id,
                            task_id=request_body["task_id"],
                            state="error"
                        )
                    )
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    agent_state = AgentTaskStates.first(conditions=[AgentTaskStates.agent_id == agent.id,
                                                                    AgentTaskStates.task_id == request_body["task_id"]])
                    # If agent state found, change state to error
                    if agent_state.state in ("success", ):
                        agent_state.state = "error"
                        db.session.commit()

                db.session.add(
                    AgentMetrics(
                        agent_id=agent.id,
                        task_id=request_body["task_id"],
                        value=0
                    )
                )
                db.session.commit()
            else:
                db.session.add(
                    AgentMetrics(
                        agent_id=agent.id,
                        task_id=request_body["task_id"],
                        value=request_body["value"]
                    )
                )

                try:
                    db.session.add(
                        AgentTaskStates(
                            agent_id=agent.id,
                            task_id=request_body["task_id"],
                            state="success"
                        )
                    )
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    agent_state = AgentTaskStates.first(conditions=[AgentTaskStates.agent_id == agent.id,
                                                                    AgentTaskStates.task_id == request_body["task_id"]])
                    if agent_state.state in ("error",):
                        agent_state.state = "success"
                        db.session.commit()

            return response_create(data=dict(created=True), response_code=201)

        return response_create(data=dict(error=True, message="You have to set 'Authorization' header in your request."),
                               response_code=401)
