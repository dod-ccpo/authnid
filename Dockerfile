FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install --upgrade pip
RUN pip install flask psycopg2-binary raven[flask] passlib[bcrypt] SQLAlchemy==1.1.13 flask-apispec flask-jwt-extended alembic

ARG env=prod

COPY ssl/*.conf /etc/nginx/conf.d/
COPY ssl/ /etc/ssl/
COPY ./app /app

WORKDIR /app/

# 8080 is not exposed. It just gives us a chance to customize port 80 in redirect_http.conf
ENV LISTEN_PORT 8080

ENV STATIC_PATH /app/app/static

EXPOSE 80 443
