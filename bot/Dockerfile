FROM python:3.10-slim


RUN apt-get clean && apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential gcc
WORKDIR /bot
COPY ./infra/requirements.txt /bot
COPY ./infra/credentials.json /bot
RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
COPY ./bot /bot
COPY ./infra/credentials.json /bot
CMD ["python", "./main.py"]
