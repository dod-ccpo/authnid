FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install --upgrade pip
RUN pip install flask psycopg2-binary raven[flask] passlib[bcrypt] SQLAlchemy==1.1.13 flask-apispec flask-jwt-extended alembic

ARG env=prod
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

ENV STATIC_PATH /app/app/static

EXPOSE 80
