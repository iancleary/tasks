FROM python:3.10.8-slim

# RUN adduser --system --no-create-home nonroot

# MIT License Credit: 
# https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/docker-images/python3.9-slim.dockerfile#L1-L25
# https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/d4014223e3d367c9fdf5a9cdd634280e06a84a97/LICENSE#L1-L21

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn

# USER nonroot

CMD ["/start.sh"]