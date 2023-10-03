# Use the official Python image
FROM python:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=mydatabaseuser
ENV POSTGRES_PASSWORD=mypassword

# Install PostgreSQL and other dependencies
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Create a working directory
WORKDIR /app

# Copy your Django project's requirements.txt file
COPY myblog/requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your Django project
COPY . /app/

# Make your script executable (if needed)
COPY script.sh /app/script.sh
RUN chmod +x /app/script.sh

# Expose the ports for Django (8000) and PostgreSQL (5432)
EXPOSE 8000
EXPOSE 5432


# Start PostgreSQL and your Django app
CMD service postgresql start && /app/script.sh
