FROM python:alpine

COPY ./api_project /var/www/html/
ADD ./docker/entrypoint.sh /entrypoint.sh
ADD ./requirements.txt /tmp/requirements.txt

RUN chmod +x /entrypoint.sh

RUN apk update \
    && apk add postgresql-dev \
    && apk add --no-cache --virtual build-deps gcc musl-dev apache2-mod-wsgi \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del --purge build-deps

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
CMD ["runserver 0.0.0.0:80"]
