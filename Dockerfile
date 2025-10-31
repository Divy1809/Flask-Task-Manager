FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.main:app
ENV FLASK_ENV=development
ENV SESSION_SECRET=8f42a73d4f9c6e8b3a1d2c0b5e9f7a4chii

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]