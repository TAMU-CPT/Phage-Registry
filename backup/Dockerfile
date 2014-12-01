FROM postgres:9.4

MAINTAINER Eric Rasche <rasche.eric@yandex.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /export/

ADD export.sh /etc/cron.daily/export.sh

VOLUME ["/export/"]

CMD ["cron", '-f']
