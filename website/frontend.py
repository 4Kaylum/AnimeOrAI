from aiohttp.web import HTTPFound, Request, Response, RouteTableDef
from voxelbotutils import web as webutils
import aiohttp_session
import discord
from aiohttp_jinja2 import template


routes = RouteTableDef()


@routes.get("/")
@template("index.htm.j2")
async def index(request: Request):
    """
    The index page for the website that is also the main game page.
    """

    return {}
