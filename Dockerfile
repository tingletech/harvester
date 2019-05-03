FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    git \
    mercurial \
    python-dev \
    python-pip \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code/dpla/ingestion
WORKDIR /code/dpla
ADD ingestion /code/dpla/ingestion
WORKDIR /code/dpla/ingestion
RUN pip install configparser && pip install --no-deps --ignore-installed -r requirements.txt

ADD ./akara.ini.tmpl /code/dpla/ingestion/akara.ini

RUN mkdir -p /code/harvester
ADD . /code/harvester
WORKDIR /code/harvester
RUN python setup.py install

ADD ./run.sh /run.sh
RUN chmod 755 /*.sh

EXPOSE 8889 

CMD ["/run.sh"]
