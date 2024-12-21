# Stage 1: Build stage
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Stage 2: Final Image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PATH="/scripts:${PATH}"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application code and wheels from builder  stage
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels
COPY . /app

# Copy utility scripts and set permissions
COPY ./scripts /scripts
RUN chmod +x /scripts/entrypoint.sh

# Create storage directories for media and static files
RUN mkdir -p /vol/web/media /vol/web/static && \
    chown -R 1000:1000 /vol && \
    chmod -R 755 /vol/web

# Switch to a non-root user
USER 1000

# Set the entrypoint script
CMD ["scripts/entrypoint.sh"]
