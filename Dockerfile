FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy configuration files
COPY pyproject.toml pdm.lock README.md /app/

# install dependencies and project
WORKDIR /app
RUN pdm install --prod --no-lock --no-editable

# copy application
COPY ./app /app
