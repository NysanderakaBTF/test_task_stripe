FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
RUN python manage.py createsuperuser --no-input --username admin
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]