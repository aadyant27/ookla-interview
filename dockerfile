FROM python:3.9

# Creates & sets working directory to 'app/'
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code to /app
COPY . .

# This serves as just an informative directive, it doesn't expose container's post to host machine.
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 




