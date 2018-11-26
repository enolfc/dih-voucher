#!/usr/bin/env bash

set -x
echo $*

# edit the config files to get the vars from environ
sed -i "s#%SERVER_NAME%#$SERVER_NAME#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_URL%#$CHECKIN_URL#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_CLIENT_ID%#$CHECKIN_CLIENT_ID#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_CLIENT_SECRET%#$CHECKIN_CLIENT_SECRET#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_CRYPTO%#$CHECKIN_CRYPTO#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_REDIRECT%#$CHECKIN_REDIRECT#" /etc/apache2/sites-enabled/000-default.conf

sed -i "s#%DIH_DATABASE%#$DIH_DATABASE#" /var/www/dih/app.wsgi
sed -i "s#%DIH_CONFIG%#$DIH_CONFIG#" /var/www/dih/app.wsgi

# run as nobody
sed -i "s/export APACHE_RUN_USER=www-data/export APACHE_RUN_USER=nobody/" /etc/apache2/envvars

cd /var/www/dih
python3 -c 'import dih.database; dih.database.init_db()'
chown nobody $(echo $DIH_DATABASE | sed s#sqlite://##)

exec "$@"
