FROM python:3.11.3-slim

# RUN adduser --system --no-create-home nonroot

# MIT License Credit:
# https://github.com/iancleary/tasks-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/docker-images/python3.9-slim.dockerfile#L1-L25
# https://github.com/iancleary/tasks-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/LICENSE#L1-L21

# Install all OS dependencies for fully functional requirements.txt install
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    # Common useful utilities
    python3-dev \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY docker-images/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY docker-images/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker-images//gunicorn_conf.py /gunicorn_conf.py

COPY docker-images/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

# Needed /code/app for from app.database to be import path in dockerfile and in venv
COPY docker-images/app /code/app

WORKDIR /code/

ENV PYTHONPATH=/code

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn

# USER nonroot

CMD ["/start.sh"]
