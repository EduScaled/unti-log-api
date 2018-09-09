import sys
from aiohttp import web

from db import init_db_pool, close_db_pool
from views import routes
from utils import get_config

def run(argv=None):
    app = web.Application(middlewares=[
       web.normalize_path_middleware(append_slash=True, merge_slashes=True),
    ])

    app['config'] = get_config(argv)

    app.on_startup.append(init_db_pool)
    app.on_cleanup.append(close_db_pool)

    app.add_routes(routes)    

    web.run_app(app, host=app['config']['host'], port=app['config']['port'])

if __name__ == '__main__':
    run(sys.argv[1:])