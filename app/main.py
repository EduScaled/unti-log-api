from aiohttp import web

def run():
    app = web.Application()
    web.run_app(app)

if __name__ == '__main__':
    run()