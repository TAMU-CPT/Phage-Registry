FROM debian:wheezy

MAINTAINER Eric Rasche <rasche.eric@yandex.ru>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update && apt-get install --no-install-recommends -y \
        python python-dev python-distribute python-pip gunicorn libpq-dev \
        build-essential make gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD . /registry/
WORKDIR /registry/
RUN pip install -r requirements.txt

EXPOSE 8000
VOLUMES ["/registry/phageregistry/whoosh_index/"]
CMD /registry/startup.sh
