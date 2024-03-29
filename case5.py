from aiohttp import web
from aiohttp_basicauth_middleware import basic_auth_middleware
import datetime

routes = web.RouteTableDef()


@routes.get('/async-api')
async def handler(request):
    data = str(datetime.datetime.now().time())
    return web.json_response(data)

app = web.Application()
app.add_routes(routes)
app.middlewares.append(basic_auth_middleware(('/async-api',),{'user': 'passwor'},))
web.run_app(app)




