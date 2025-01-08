FROM python:latest

RUN apt-get update && apt-get install -y \
    && apt-get clean

RUN pip install --no-cache-dir boto3 requests

WORKDIR /var/apps3

COPY botos3.py /var/apps3/botos3.py

CMD ["python", "/var/apps3/botos3.py"]
