from sqreened_app import celery, create_app, init_celery

app = create_app(celery=celery)
