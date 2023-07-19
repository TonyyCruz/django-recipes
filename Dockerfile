FROM python:3

WORKDIR /usr/src/app

COPY dev-requirements.txt ./

RUN pip install --no-cache-dir -r dev-requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]