FROM debian:wheezy

MAINTAINER Eric Rasche <rasche.eric@yandex.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update && apt-get install --no-install-recommends -y \
        python python-dev python-distribute python-pip gunicorn libpq-dev \
        build-essential make gcc nginx netcat postgresql-client-common postgresql-client-9.1\
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY phageregistry /registry/phageregistry
COPY registry /registry/registry
COPY static /registry/static
COPY env.sh manage.py startup.sh /registry/
WORKDIR /registry/

ADD proxy.conf /etc/nginx/sites-enabled/default

EXPOSE 80
VOLUME ["/registry/phageregistry/whoosh_index/"]
CMD /registry/startup.sh
