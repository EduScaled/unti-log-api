from aiohttp import web
from service import insert_log, get_logs

routes = web.RouteTableDef()

@routes.view('/logs/list/')
class LogListView(web.View):

    async def post(self):
        pool = self.request.app['db']
        params = await self.request.json()
        data = {
            'logs': await get_logs(pool, params)
        }
        
        return web.json_response(data)

@routes.view('/logs/add/')
class LogAddView(web.View):

    async def post(self):
        data = await self.request.json()
        pool = self.request.app['db']
        # TODO validate incoming data from request
        log = {
            'user_id': data.get('user_id', 0),
            'email': data.get('email', 'empty email'),
            'type': data.get('type', 'empty type'),
            'action': data.get('action', 'empty action'),
            'url': data.get('url', 'empty url'),
        }
        await insert_log(pool, log)

        return web.json_response({'log': log})