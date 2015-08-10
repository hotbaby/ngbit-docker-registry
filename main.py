#!/usr/bin/env python
# -*- coding: utf-8 -*-

# only needed if not using gunicorn gevent
import gevent.monkey
gevent.monkey.patch_all()

# start new relic if instructed to do so
from registry.extensions import factory
from registry.extras import enewrelic
from registry.server import env
enewrelic.boot(env.source('NEW_RELIC_CONFIG_FILE'),
               env.source('NEW_RELIC_LICENSE_KEY'))
factory.boot()

from registry.app import app 
from registry.user.models import *
from registry.lib.index.db import *
from registry.db import db 
db.create_all()

from registry.tags import * 
from registry.images import * 
from registry.lib import config

cfg = config.load()

from registry.search import *  # noqa
from registry.service  import * #noqa
from registry.upload import *

# If standalone mode is enabled, load the fake Index routes
from registry.index import *  # noqa
from registry.user.models import User
from registry.user.db_adapter import SQLAlchemyAdapter
from registry.user import UserManager

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
app.user_manager = user_manager

app.run(host='127.0.0.1', port=8080, debug=True)
