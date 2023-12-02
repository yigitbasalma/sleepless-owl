FROM python:3.10-slim-bullseye

WORKDIR /app

COPY w/ w/
COPY run.py run.py
COPY requirements.txt requirements.txt

RUN apt update && \
    apt install -y git && \
    pip3 install -r requirements.txt && \
    pip3 install --force-reinstall Werkzeug==2.3.0 \

CMD ["/usr/local/bin/python", "run.py"]