FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
