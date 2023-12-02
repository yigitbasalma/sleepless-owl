import socket
import ssl

from datetime import datetime
from cryptography import x509
from urllib.parse import urlparse

from w import db, celery
from w.apps.tasks.models import Tasks


@celery.task
def track():
    tasks = Tasks.all(conditions=[
        Tasks.url.like("https://%")
    ])

    for task in tasks:
        _url = urlparse(task.url)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((_url.hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=_url.hostname) as ssock:
                data = ssock.getpeercert(True)
                pem_data = ssl.DER_cert_to_PEM_cert(data)
                cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))

                task.cert_valid_until = cert_data.not_valid_after

                if cert_data.not_valid_after > datetime.now():
                    task.cert_valid = "valid"
                else:
                    task.cert_valid = "expired"

                db.session.commit()
