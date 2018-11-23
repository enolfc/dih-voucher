FROM ubuntu:bionic

RUN apt-get update \
    && apt-get install -y apache2 libapache2-mod-wsgi-py3 libapache2-mod-auth-openidc python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY default.conf /etc/apache2/sites-enabled/000-default.conf

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /var/www/dih
COPY app.wsgi  /var/www/dih/app.wsgi 

COPY dih /var/www/dih/dih

EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
