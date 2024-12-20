FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERFED 1
ENV PATH="/scripts:${PATH}"

# Set the working directory
WORKDIR / app

# Install and update dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev && \
    python3 -m pip install pip --upgrade pip && \
    pip install -r requirements.txt

# Copy application code and set the working directory
RUN mkdir /app
COPY . /app
WORKDIR /app

# Copy utility scripts and give executable permissions
COPY ./scripts /scripts
RUN chmod +x /scripts/*

# Create storage directories for media and static files
RUN mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static

# Create user in container and gives ownership of new directories
RUN adduser --disabled-password --no-create-home user && \
    chown -R user:user /vol && \
    chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]

