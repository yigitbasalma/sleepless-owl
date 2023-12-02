# Sleepless Owl
### What
Sleepless Owl is an open-source project for tracking site response time and defining alerts.

### Project Architecture
![Project Architecture](docs/images/sleepless-owl-architecture.png)

### Abilities
* Multi-site data collection with agents,
* TCP and HTTP(s) checks,
* Certificate expire check,
* Maintenance windows

### Components
* MySQL
* Redis

### Notification Adapters
* Slack
* Teams

### Install
This project uses the MySQL as a database and the Redis as the Celery backend (for async tasks) and a session storage.

1. Replace the MySQL and the Redis connection string in w/config/config.py,
```python 
# Celery
CELERY_BROKER_URL='redis://127.0.0.1:6379/5',
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/6'

# SQLAlchemy Config
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Qazxsw123*@127.0.0.1:3306/sleepless_owl"
```
2. Change the BASE_URL and the ENV parameters in the w/config/config.py,
```python
# General config
BASE_URL = "owl.warewave.tech"

# Running env
ENV = "development"
```
3. Build the application and the celery as a container,
```bash
# Application
docker build -t sleepless-owl:latest -f docker/application/Dockerfile .

# Celery
docker build -t sleepless-owl-celery:latest -f docker/celery/Dockerfile .
```
4. Docker run for the app and the celery.
```bash
# Application
docker run -d --name sleepless-owl-app -p 8080:8080 sleepless-owl:latest

# Celery
docker run -d --name sleepless-owl-celery  sleepless-owl-celery:latest
```

### Application Configuration
#### Create Initial Admin User
When the installation is completed, you need to create the first user aka admin user. Go to http://<ip-address>:8080 and then click the register button. Remember, the first registered user will be an admin account.

#### Create First Agent
After the initial admin user creation step, you need an agent to start monitoring. After logging in as admin, click the dropdown menu located top right and then click the "Agents" button. On the opened page, click the plus sign next to the "Agents" label. Enter the name and location info belonging to an agent and then click the "Create" button.

#### Configure Agent
1. Configure OS for agent,
```bash
# Create user
useradd sleepless-owl

# Create agent directory and change owner to the sleepless-owl
mkdir /opt/sleepless-owl-agent && chown sleepless-owl. sleepless-owl-agent

# Move agent systemd file to the /etc/systemd/system
mv /opt/sleepless-owl-agent/sleepless-owl-agent.service /etc/systemd/system

# Reload systemd daemon
systemctl daemon-reload
```
2. Change the agent key in the agent config with the key that you created one step before,
```yaml
agent:
  key: <agent-key-here>
```
3. Start and enable agent service.
```bash
systemctl enable --now sleepless-owl-agent.service
```

### Dashboard Explanation
![Dashboard Explanation](docs/images/dashboard-explanation.png)

### Notification Configuration
#### Provider Required Configs
__Slack__
````json
{
  "api_key": "xoxb-not-a-real-token-this-will-not-work"
}
````
__Teams__
````json
{
  "webhook_url": "https://xxxxx.webhook.office.com/xxxxxxxxx"
}
````

#### Rule Default Configs
```json
{
  "channel": "<channel-id>",  // Required if you will use a Slack based rule
  "task-down-alerts": true, 
  "agent-down-alerts": true, 
  "certificate-expire-alerts": true, 
  "certificate-expire-alerts-start-before": "1-Month",  // It can be days or month
  "certificate-expire-alerts-send-ratio": "weekly"  // It can be weekly or daily
}
```
