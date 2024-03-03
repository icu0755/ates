ARG DEPENDENCY_PROXY=""
ARG FROM_BUILD="pythonbase"

FROM ${DEPENDENCY_PROXY}python:3.11-slim-bullseye AS pythonbase
ENV PYTHONUNBUFFERED 1
ENV DEV_LIBS \
    default-libmysqlclient-dev \
    libjpeg-dev \
    libffi-dev
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    $DEV_LIBS \
    gcc \
    make \
    git \
    awscli \
    default-mysql-client \
    pkg-config
WORKDIR /code
ENV PYTHONUNBUFFERED=1
ENV DOCKERIZE_VERSION=v0.7.0
RUN apt-get update \
    && apt-get install --no-install-recommends -y ssh wget gettext \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin

FROM ${FROM_BUILD} AS accounting
COPY accounting/requirements/requirements.prod.txt requirements/requirements.prod.txt
RUN pip install --no-cache-dir pip==23.1 pip-tools \
    && pip-sync requirements/requirements.prod.txt
RUN apt-get purge -y $DEV_LIBS \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -d /code -s /bin/bash app
COPY accounting /code
RUN chown app:app -R /code
USER app
RUN ./manage.py collectstatic --noinput
CMD ["uwsgi", "--ini", "conf/uwsgi.ini"]
EXPOSE 8000

FROM ${FROM_BUILD} AS auth
COPY auth/requirements/requirements.prod.txt requirements/requirements.prod.txt
RUN pip install --no-cache-dir pip==23.1 pip-tools \
    && pip-sync requirements/requirements.prod.txt
RUN apt-get purge -y $DEV_LIBS \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -d /code -s /bin/bash app
COPY auth /code
RUN chown app:app -R /code
USER app
RUN ./manage.py collectstatic --noinput
CMD ["uwsgi", "--ini", "conf/uwsgi.ini"]
EXPOSE 8000

FROM ${FROM_BUILD} AS task_tracker
COPY task_tracker/requirements/requirements.prod.txt requirements/requirements.prod.txt
RUN pip install --no-cache-dir pip==23.1 pip-tools \
    && pip-sync requirements/requirements.prod.txt
RUN apt-get purge -y $DEV_LIBS \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -d /code -s /bin/bash app
COPY task_tracker /code
RUN chown app:app -R /code
USER app
RUN ./manage.py collectstatic --noinput
CMD ["uwsgi", "--ini", "conf/uwsgi.ini"]
EXPOSE 8000
