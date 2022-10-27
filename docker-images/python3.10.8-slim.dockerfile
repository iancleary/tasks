FROM python:3.10.8-slim

RUN adduser --system --no-create-home nonroot

WORKDIR /usr/src/app

# # install pip
# RUN pip install -U pip setuptools wheel

# copy configuration files
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# copy application
COPY ./app .

EXPOSE 80

USER nonroot

CMD [ "python", "main.py" ]