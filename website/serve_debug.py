from aiohttp import web
import asyncio
import jinja2 
import aiohttp_jinja2
import os

import frontend, backend

app = web.Application(loop=asyncio.get_event_loop())

app.add_routes(frontend.routes)
app.add_routes(backend.routes)

app['static_root_url'] = '/static'
app.router.add_static('/static', os.getcwd() + '/static', append_version=True)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.getcwd() + '/templates'))

web.run_app(app)
