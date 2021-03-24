ARG FROM_TAG=latest
#FROM registry.gitlab.com/viralcreation/retargeting-images/rt-python3:${FROM_TAG}
#FROM python:alpine
FROM python:3.8-alpine


# Package installation

# Base
RUN apk --no-cache add uwsgi-python3 nginx supervisor

# Binary needed
#RUN apk --no-cache add mariadb-connector-c-dev py3-gdal gdal-dev geos-dev binutils \
#    libpng libjpeg-turbo

# Development dependencies
RUN apk add --no-cache --virtual .build-deps g++ gcc musl-dev \
    libjpeg-turbo-dev zlib-dev

# Build ENV
ENV DATABASE_DEFAULT_URL="sqlite:///:memory:"
ENV APP_ENV="local"
ENV DJANGO_SETTINGS_MODULE=settings.env.${APP_ENV}

# copy configs
COPY automation/docker/conf/nginx.conf /etc/nginx/nginx.conf
COPY automation/docker/conf/uwsgi.ini /etc/uwsgi/
COPY automation/docker/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY automation/docker/script/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY automation/docker/script/shutdownifonedown.sh /usr/local/bin/shutdownifonedown.sh

# Add application
RUN mkdir -p /app
WORKDIR /app

# copy app into container
COPY apps/ ./apps
COPY settings/ ./settings
COPY wsgi/ ./wsgi
COPY manage.py requirements.txt ./

# Upgrade pip
RUN pip install --upgrade pip
# Install requirements 
RUN pip install -r requirements.txt
# Remove development packages
RUN apk del .build-deps
# Collect static files
RUN python3 /app/manage.py collectstatic

HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:80 || exit 1
EXPOSE 80
ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
