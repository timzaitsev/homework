from aiohttp import web
import datetime

routes = web.RouteTableDef()


@routes.get('/async-api')
async def handler(request):
    data = str(datetime.datetime.now().time())
    return web.json_response(data)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
