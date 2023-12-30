# Use an official Python runtime as the base image
FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN apt-get update && apt-get install --no-install-recommends -y postgresql-client libpq-dev python3-dev gcc

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the working directory
COPY . .

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000

# Define the command to run when the container starts
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]