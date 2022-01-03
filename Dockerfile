FROM ubuntu

RUN apt-get update && apt-get install --yes --no-install-recommends \
    python3-pip

WORKDIR /app

COPY . .

RUN pip install -r /app/requirements.txt
