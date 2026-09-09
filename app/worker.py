from celery import Celery


celery_app = Celery(
    "background_jobs",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.jobs"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)