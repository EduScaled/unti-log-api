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

    async def is_valid(self, data):
        user_id = data.get('user_id', None)
        type = data.get('type', None)
        action = data.get('action', None)
        try:
            is_user_valid = int(str(user_id))
        except ValueError:
            is_user_valid = False

        return is_user_valid and type and action


    async def post(self):
        data = await self.request.json()
        pool = self.request.app['db']

        if not await self.is_valid(data):
            return web.json_response({'error': 'not enough params'}, status=400)

        log = {
            'user_id': data.get('user_id'),
            'email': data.get('email', ''),
            'type': data.get('type'),
            'action': data.get('action'),
            'url': data.get('url', ''),
        }

        await insert_log(pool, log)

        return web.json_response({'log': log})