# Set base image
FROM python:3.11.2-bullseye

ENV PYTHONUNBUFFERED=1

# Update pip version and install latest version of pipenv
RUN pip install --upgrade pip==24.0

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY ./social_network_manager .

# Start the Django development server on port 8000
CMD ["bash", "-c", \
    "python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000"]

# Expose port 8000
EXPOSE 8000
