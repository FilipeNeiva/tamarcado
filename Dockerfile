FROM python:3.10.4-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements/dev.txt

CMD ["python", "manage.py", "runserver", "0:8000"]