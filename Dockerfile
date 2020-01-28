FROM python:3.7

ENV FLASK_ENV docker
ENV C_FORCE_ROOT true

WORKDIR /app

COPY . /app

RUN make clean

RUN pip install virtualenv

EXPOSE 5000

CMD ["make", "docker-cmd"]
