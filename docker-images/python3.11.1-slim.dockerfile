FROM python:3.11.1-slim

# RUN adduser --system --no-create-home nonroot

# MIT License Credit:
# https://github.com/iancleary/ivy-lee-method-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/docker-images/python3.9-slim.dockerfile#L1-L25
# https://github.com/iancleary/ivy-lee-method-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/LICENSE#L1-L21

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

# Needed /code/app for from app.database to be import path in dockerfile and in venv
COPY ./app /code/app
# Copy alembic configuration file
COPY alembic.ini /code/app

WORKDIR /code/

ENV PYTHONPATH=/code

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn

# USER nonroot

CMD ["/start.sh"]
