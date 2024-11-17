FROM python:3.12-bookworm

WORKDIR /home/flask

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]