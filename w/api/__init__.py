from flask import Blueprint
from flask_restful import Api

from w import app

from .agent.routes import AgentPing, AgentMetric

api_router = Blueprint("api_router", __name__, url_prefix=app.config['API_VERSION'])

# Create API resource object
api_resource = Api(api_router)

# Add API resources
api_resource.add_resource(AgentPing, *AgentPing.endpoints)
api_resource.add_resource(AgentMetric, *AgentMetric.endpoints)
