FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install \
    fastapi \
    uvicorn

COPY ./app /app
