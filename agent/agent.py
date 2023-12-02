import logging
import time
import json
import requests
import socket

from yaml import load, FullLoader
from bunch import bunchify
from threading import Thread

# Application config
CONFIG = bunchify(load(open("config.yaml", "r").read(), Loader=FullLoader))

# Logging config
logging.basicConfig(
    format=CONFIG.logging.format,
    level=CONFIG.logging.level
)


class Agent(requests.Session):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger("agent-manager")
        self.base_url = CONFIG.agent.backend
        self.headers.update({
            "Content-Type": "application/json",
            "Authorization": CONFIG.agent.key
        })
        self.verify = False

    def ping(self):
        while 1:
            try:
                ping = self.get(
                    f"{self.base_url}/ping",
                )
            except requests.exceptions.ConnectionError:
                self.log.error(f"Could not connect to backend {self.base_url}")
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
                self.log.error(f"Getting timeout when trying to connect the backend {self.base_url}")
            except Exception as e:
                self.log.error(f"Unknown exception {e}")
            else:
                self.log.debug(f"Successfully pinged to the backend. Response: {ping.json()}")

            time.sleep(10)

    def get_task_list(self):
        try:
            return self.get(
                f"{self.base_url}/metric",
            ).json()
        except requests.exceptions.ConnectionError:
            self.log.error(f"Could not connect to backend {self.base_url}/metric")
            return []
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            self.log.error(f"Getting timeout when trying to connect the backend {self.base_url}/metric")
            return []
        except Exception as e:
            self.log.error(f"Unknown exception {e}")
            return []

    def update_metric(self, metric, task_id, error=None):
        try:
            if error:
                return self.post(
                    f"{self.base_url}/metric",
                    data=json.dumps({"task_id": task_id, "value": metric, "error": error})
                ).json()

            return self.post(
                f"{self.base_url}/metric",
                data=json.dumps({"task_id": task_id, "value": metric})
            ).json()
        except requests.exceptions.ConnectionError:
            self.log.error(f"Could not connect to backend {self.base_url}/metric")
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            self.log.error(f"Getting timeout when trying to connect the backend {self.base_url}/metric")
        except Exception as e:
            self.log.error(f"Unknown exception {e}")


class HttpAgent(requests.Session):
    def __init__(self, config):
        super().__init__()
        self.log = logging.getLogger("http-agent-manager")
        self.task_name = config["name"]
        self.task_id = config["id"]
        self.period = config["period"]
        self.url = config["url"]
        self.data = config.get("data")
        self.headers.update(config.get("headers", {}))
        self.valid_return_codes = [int(i) for i in config["return_codes"].split(",")]

        if config.get("username") and config.get("password"):
            self.auth = (config["username"], config["password"])

    def check(self):
        while 1:
            try:
                req = self.get(
                    self.url,
                    data=self.data,
                    timeout=self.period
                )

                if req.status_code in self.valid_return_codes:
                    elapsed = req.elapsed.total_seconds() * 1000
                    self.log.info(f"Successfully requested {self.url}({self.task_name}). "
                                  f"Response time: {elapsed}")
                    agent.update_metric(metric=elapsed, task_id=self.task_id)
            except requests.exceptions.ConnectionError:
                self.log.error(f"Could not connect to url {self.url}({self.task_name})")
                agent.update_metric(metric=0, task_id=self.task_id,
                                    error=f"Could not connect to url {self.url}({self.task_name})")
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
                self.log.error(f"Getting timeout when trying to connect the url {self.url}({self.task_name})")
                agent.update_metric(
                    metric=0,
                    task_id=self.task_id,
                    error=f"Getting timeout when trying to connect the url {self.url}({self.task_name})")
            except Exception as e:
                self.log.error(f"Unknown exception '{e}' for {self.url}({self.task_name})")
                agent.update_metric(metric=0, task_id=self.task_id, error=f"{e}")

            time.sleep(self.period)

    def update(self, config):
        self.task_name = config["name"]
        self.period = config["period"]
        self.url = config["url"]
        self.data = config.get("data")
        self.headers.update(config.get("headers", {}))
        self.valid_return_codes = [int(i) for i in config["return_codes"].split(",")]

        if config.get("username") and config.get("password"):
            self.auth = (config["username"], config["password"])


class TCPAgent:
    def __init__(self, config):
        self.log = logging.getLogger("tcp-agent-manager")
        self.task_name = config["name"]
        self.task_id = config["id"]
        self.period = config["period"]
        self.target_host = config["ip_address"]
        self.target_port = config["port"]

    def check(self):
        while 1:
            try:
                start = time.perf_counter()
                with socket.socket() as sock:
                    sock.settimeout(self.period)
                    _ = sock.connect((self.target_host, self.target_port))
                    sock.recv(512)
                    sock.close()
                elapsed = (time.perf_counter() - start) * 1000
                self.log.info(f"Successfully requested {self.target_host}:{self.target_port}({self.task_name}). "
                              f"Response time: {elapsed}")
                agent.update_metric(metric=elapsed, task_id=self.task_id)
            except OSError as e:
                self.log.error(f"Unknown exception '{e}' for {self.target_host}:{self.target_port}({self.task_name})")
                agent.update_metric(metric=0, task_id=self.task_id, error=f"{e}")

            time.sleep(self.period)

    def update(self, config):
        self.task_name = config["name"]
        self.period = config["period"]
        self.target_host = config["ip_address"]
        self.target_port = config["port"]


if __name__ == "__main__":
    # Init ping manager
    agent = Agent()
    Thread(target=agent.ping, daemon=True).start()

    # Initial variables
    task_thread_list = {}
    task_types = dict(http=HttpAgent, tcp=TCPAgent)

    while 1:
        for task in agent.get_task_list():
            if not task_thread_list.get(task["id"]):
                _agent = task_types.get(task["type"])(config=task)
                thread = Thread(target=_agent.check, daemon=True)
                task_thread_list[task["id"]] = _agent
                thread.start()
            else:
                _agent = task_thread_list.get(task["id"])
                _agent.update(task)

        time.sleep(10)
