# Use Python 3.12.5 as the base image
FROM python:3.12.5-slim

# Set environment variables to not buffer output
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
