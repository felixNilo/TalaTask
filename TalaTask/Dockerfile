FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

#to production consider to use gunicorn in order to improve the performance and concurrence.
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TalaTask.wsgi:application"]

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]