FROM python:3.12-slim

RUN apt-get update && \
    apt-get install curl -y

WORKDIR /home/flask

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser
RUN chown -R flaskuser:flaskuser /home/flask
USER flaskuser

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]