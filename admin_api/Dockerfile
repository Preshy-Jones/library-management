FROM python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies directly
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv requirements > requirements.txt && \
    pip install -r requirements.txt

# Copy application code
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]