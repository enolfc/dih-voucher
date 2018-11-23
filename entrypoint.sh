#!/usr/bin/env bash

set -x
echo $*

# edit the config files to get the vars from environ
sed -i "s#%SERVER_NAME%#$SERVER_NAME#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_URL%#$CHECKIN_URL#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_CLIENT%#$CHECKIN_CLIENT#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_SECRET%#$CHECKIN_SECRET#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_CRYPTO%#$CHECKIN_CRYPTO#" /etc/apache2/sites-enabled/000-default.conf
sed -i "s#%CHECKIN_REDIRECT%#$CHECKIN_REDIRECT#" /etc/apache2/sites-enabled/000-default.conf

sed -i "s#%DIH_DATABASE%#$DIH_DATABASE#" /var/www/dih/app.wsgi
sed -i "s#%DIH_CONFIG%#$DIH_CONFIG#" /var/www/dih/app.wsgi

cd /var/www/dih
python3 -c 'import dih.database; dih.database.init_db()'
chown www-data:www-data $(echo $DIH_DATABASE | sed s#sqlite://##)

exec "$@"
