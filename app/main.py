import os
import sys
from aiohttp import web

from app.db import init_db_pool, close_db_pool
from app.views import routes
from app.utils import get_config

def init_app(argv=None):
    app = web.Application(middlewares=[
       web.normalize_path_middleware(append_slash=True, merge_slashes=True),
    ])

    app['config'] = get_config(argv)

    app.on_startup.append(init_db_pool)
    app.on_cleanup.append(close_db_pool)

    app.add_routes(routes)    

    return app

def container():
    argv = None
    if os.environ.get('CONFIG', None):
        argv = [None, '--config', os.environ.get('CONFIG')]
    return init_app(argv)        

def wsgi(config=None):
    if config:
        argv = [None, '--config', config]
        return init_app(argv)

def run(argv=None):
    app = init_app(argv)
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])