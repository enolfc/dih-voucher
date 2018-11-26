from datetime import datetime, timezone
import json
import os

import dateutil.parser
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_humanize import Humanize
import requests

from dih.database import db_session
from dih.models import User, VO

app = Flask(__name__)
app.config.from_object('dih.defaults')
try:
    app.config.from_envvar('DIH_CONFIG')
except:
    # whatever, no config...
    pass
Humanize(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(500)
def error500(e):
    print(e)
    return render_template('500.html'), 500


def get_user():
    env = request.environ
    if 'HTTP_OIDC_SUB' not in env:
        raise Exception('Unable to get Check-in stuff!')
    env_user = {
        'epuid': env.get('HTTP_OIDC_SUB'),
        'email': env.get('HTTP_OIDC_EMAIL'),
        'name': env.get('HTTP_OIDC_NAME'),
    }
    user = User.query.filter(User.epuid == env_user['epuid']).first()
    if not user:
        user = User(**env_user)
        db_session.add(user)
        db_session.commit()
    # Get info about the VOs
    user_url = '/'.join([app.config['CHECKIN_VO_URL'], user.epuid])
    r = requests.get(user_url,
                     auth=(app.config['CHECKIN_USER'],
                           app.config['CHECKIN_PWD']))
    r.raise_for_status()
    user_vos = r.json()
    if user_vos:
        # We default to expired...
        user.status = 'Expired'
        for vos in user_vos:
            status = vos['status']
            now = datetime.now(timezone.utc)
            valid_from = dateutil.parser.parse(vos['valid_from'])
            valid_through = dateutil.parser.parse(vos['valid_through'])
            if status == 'Active':
                if now >= valid_from and now <= valid_through:
                    user.valid_through = valid_through
                    user.status = status
    return user


@app.route('/')
def index():
    user = get_user()
    return render_template('index.html', user=user)


@app.route('/enroll')
def enroll():
    user = get_user()
    if user.status in ['Active', 'Expired']:
        # do not try to abuse, bye!
        flash("You have already redeemed your voucher, can't get another one!")
        return redirect(url_for('index'))
    # get available VO
    vo = VO.query.filter(VO.used == False).first()
    if not vo:
        # no more available, bye!
        flash('There are no vouchers left! '
              'Stay tuned for upcoming promotions!')
        return redirect(url_for('index'))
    # Enrolling the user in the VO
    now = datetime.now(timezone.utc)
    valid_through = now + app.config['VOUCHER_TIME']
    body = {
        "RequestType": "VoMembers",
        "Version": "1.0",
        "VoMembers": [
            {
                "Version": "1.0",
                "VoId": "%s" % vo.name,
                "Person": {
                    "Type": "CO",
                    "Id": "%s" % user.epuid
                },
                "Status": "Active",
                "ValidFrom": "%s" % now.isoformat(), 
                "ValidThrough": "%s" % valid_through.isoformat(),
            }
        ]
    }
    r = requests.post(app.config['CHECKIN_VO_URL'],
                      auth=(app.config['CHECKIN_USER'],
                            app.config['CHECKIN_PWD']),
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(body))
    r.raise_for_status()
    # update stuff once we had ok from Check-in
    vo.used = True
    db_session.commit()
    flash('Your voucher is now active!')
    return redirect(url_for('index'))
