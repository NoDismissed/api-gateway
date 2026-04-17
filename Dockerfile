FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV FLASK_APP=app.app
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=${PORT:-5000}"]
