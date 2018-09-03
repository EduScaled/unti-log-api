from aiohttp import web

from db import init_db_pool, close_db_pool
from views import routes
from utils import get_config

def run():
    app = web.Application()

    app['config'] = get_config()

    app.on_startup.append(init_db_pool)
    app.on_cleanup.append(close_db_pool)

    app.add_routes(routes)    

    web.run_app(app)

if __name__ == '__main__':
    run()