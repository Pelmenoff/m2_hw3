FROM python:latest

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

ENV FLASK_APP=web.web

VOLUME /app/web/storage

EXPOSE 3000 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]