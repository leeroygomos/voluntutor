FROM python:3

ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh ./entrypoint.sh

COPY . .
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD python3 manage.py runserver 0.0.0.0:8000

