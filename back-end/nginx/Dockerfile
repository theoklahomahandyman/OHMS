# Fetching latest nginx image
FROM nginxinc/nginx-unprivileged:1-alpine

# Copying new conf.d into conf.d nginx image
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Use root user to create static directory and set permissions
USER root
RUN mkdir -p /vol/static/ && \
    chmod 755 /vol/sstatic
USER nginx
