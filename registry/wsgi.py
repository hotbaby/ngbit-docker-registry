#!/usr/bin/env python
# -*- coding: utf-8 -*-

global DOMAIN_URL
DOMAIN_URL = '192.168.1.9'

# only needed if not using gunicorn gevent
if __name__ == '__main__':
    import gevent.monkey
    gevent.monkey.patch_all()

# start new relic if instructed to do so
from .extensions import factory
from .extras import enewrelic
from .server import env
enewrelic.boot(env.source('NEW_RELIC_CONFIG_FILE'),
               env.source('NEW_RELIC_LICENSE_KEY'))
factory.boot()

import logging

from .app import app  # noqa
from .tags import *  # noqa
from .images import *  # noqa
from .lib import config

cfg = config.load()
logger = logging.getLogger(__name__)

logger.debug('config search_backend: {0}'. format(cfg.search_backend))
#if cfg.search_backend:

from .lib import index
DB = index.DB
DB.create_all()

from .search import *  # noqa
from .service  import * #noqa
from .upload import *

logger.debug('config standalone: {0}'.format(cfg.standalone))
if cfg.standalone:
    # If standalone mode is enabled, load the fake Index routes
    from .index import *  # noqa

if __name__ == '__main__':
    host = env.source('REGISTRY_HOST')
    port = env.source('REGISTRY_PORT')
    app.debug = cfg.debug
    app.run(host=host, port=port)
else:
    level = cfg.loglevel.upper()
    if not hasattr(logging, level):
        level = 'INFO'
    level = getattr(logging, level)
    app.logger.setLevel(level)
    stderr_logger = logging.StreamHandler()
    stderr_logger.setLevel(level)
    stderr_logger.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(stderr_logger)
    application = app
