# Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /code

# Copy requirements first to leverage Docker caching
COPY itbrat/requirements.txt /code/requirements.txt

# Install requirements
RUN pip install -r /code/requirements.txt

# Copy entire project to container
COPY itbrat /code

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "config.wsgi:application"]
