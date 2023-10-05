# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /project

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat-traditional instead of netcat
RUN apt-get update && apt-get install -y netcat-traditional

# Copy the rest of your backend code into the container
COPY . .

# Entrypoint
ENTRYPOINT [ "sh", "entrypoint.sh" ]
