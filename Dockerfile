FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# install pip
RUN pip install -U pip setuptools wheel

# copy configuration files
COPY requirements.txt README.md /app/

# install dependencies and project
WORKDIR /app
RUN pip install -r requirements.txt

# copy application
COPY ./app /app
