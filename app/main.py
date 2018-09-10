import sys
from aiohttp import web

from app.db import init_db_pool, close_db_pool
from app.views import routes
from app.utils import get_config

def init_app():
    app = web.Application(middlewares=[
       web.normalize_path_middleware(append_slash=True, merge_slashes=True),
    ])

    app['config'] = get_config()

    app.on_startup.append(init_db_pool)
    app.on_cleanup.append(close_db_pool)

    app.add_routes(routes)    

    return app

async def async_run():
    return init_app()

def sync_run():
    app = init_app()
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])