FROM python:latest
RUN apt update 
RUN pip install boto3
RUN pip install requests
WORKDIR /var/apps3
COPY botos3.py /var/apps3/botos3.py
CMD ["sh", "-c", "python /var/apps3/botos3.py"]
