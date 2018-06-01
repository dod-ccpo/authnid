FROM tiangolo/uwsgi-nginx:python3.6

RUN pip install --upgrade pip
RUN pip install pipenv

ARG env=prod

COPY ssl/*.conf /etc/nginx/conf.d/
COPY ssl/ /etc/ssl/
COPY ./ /app

WORKDIR /app/
RUN pipenv install --system --deploy --ignore-pipfile
ENV UWSGI_INI /app/uwsgi.ini

EXPOSE 80 443