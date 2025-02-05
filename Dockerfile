FROM python:3.11-slim

RUN mkdir /bot

COPY requirements.txt /bot/

RUN python -m pip install -r /bot/requirements.txt

COPY . /bot

WORKDIR /bot

ENTRYPOINT ["python", "core.py"]