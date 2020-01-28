import os

from sqreened_app import create_app, celery


app = create_app(celery=celery)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"],
            debug=app.config["DEBUG"])
