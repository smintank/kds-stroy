FROM python:3.11
WORKDIR /app

RUN pip install gunicorn==20.1.0
RUN apt-get update && apt-get install -y ca-certificates
RUN apt-get install -y iputils-ping

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get install -y net-tools

COPY . .

CMD ["gunicorn", "--bind", "0:8000", "kds_stroy.wsgi"]