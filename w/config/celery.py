imports = [
    "w.async_jobs.tasks.track_task_state",
    "w.async_jobs.tasks.check_ssl_certificate",
    "w.async_jobs.tasks.cleanup_expired_items",
    "w.async_jobs.tasks.track_maintenance",
    "w.async_jobs.alerts.check_certificate_alerts",
    "w.async_jobs.alerts.check_task_alerts",
    "w.async_jobs.maintenance.track_maintenance_state"
]

timezone = "UTC"

beat_schedule = {
    "track-task-state-changes": {
        "task": "w.async_jobs.tasks.track_task_state.track",
        "schedule": 5
    },
    "track-task-certificate-validity": {
        "task": "w.async_jobs.tasks.check_ssl_certificate.track",
        "schedule": 60
    },
    "track-expired-alert-hash": {
        "task": "w.async_jobs.tasks.cleanup_expired_items.track",
        "schedule": 10
    },
    "track-certificate-validity-alerts": {
        "task": "w.async_jobs.alerts.check_certificate_alerts.track",
        "schedule": 10
    },
    "track-task-status-alerts": {
        "task": "w.async_jobs.alerts.check_task_alerts.track",
        "schedule": 10
    },
    "track-maintenance-status": {
        "task": "w.async_jobs.maintenance.track_maintenance_state.track",
        "schedule": 10
    },
    "track-task-maintenance-status": {
        "task": "w.async_jobs.tasks.track_maintenance.track",
        "schedule": 10
    }
}

broker_connection_retry_on_startup = True
