import random
import io
from base64 import b64encode

import aiohttp
from aiohttp.web import HTTPFound, Request, RouteTableDef, json_response
import aiohttp_session
from PIL import Image

import os

VOTES_FILE = os.path.join(os.path.dirname(__file__), "static", "votes.txt")

routes = RouteTableDef()
QUERY = """
query ($page: Int) {
  Page(page: $page, perPage: 1) {
    characters(id_not: -1) {
      name {
        full
      }, image {
        large
      },
      media(sort: ID) {
        nodes {
          title {
            english
          },
          type
        }
      }
    }
  }
}
"""


def get_image_b64(image: bytes) -> bytes:
    return b64encode(image).decode()


async def get_random_fake(request: Request) -> io.BytesIO:
    """
    Get a random image from the API, crop it, and resize it.
    """

    # Get the original
    async with aiohttp.ClientSession() as session:
        file_key = f"psi-{random.randint(3, 20) / 10:.1f}/seed{random.randint(0, 99999):0>5}"
        url = f"https://thisanimedoesnotexist.ai/results/{file_key}.png"
        async with session.get(url) as r:
            data = await r.read()

    # Crop it
    image_bytes = io.BytesIO(data)
    image = Image.open(image_bytes)
    image = image.crop((92, 0, 92 + 328, 512))

    # Resize it
    image = image.resize((230, 358))

    # Save it
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # Encode the image
    encoded = get_image_b64(output.read())

    # Return it
    return {
        "key": f"tadne/{file_key}",
        "name": None,
        "anime": None,
        "image": encoded,
    }


async def get_random_real(request: Request) -> dict:
    """
    Get a random image from the API, crop it, and resize it.
    """

    # Get the original
    async with aiohttp.ClientSession() as session:
        url = f"https://graphql.anilist.co"
        json = {
            "query": QUERY,
            "variables": {
                "page": random.randint(1, 18_000),
            },
        }
        async with session.post(url, json=json) as r:
            data = await r.json()
        character = data['data']['Page']['characters'][0]
        if character['image']['large'] == "https://s4.anilist.co/file/anilistcdn/character/large/default.jpg":
            return await get_random_real(request)
        async with session.get(character['image']['large']) as r:
            data = await r.read()

    # Return it
    return {
        "key": f"real/{character['media']['nodes'][0]['title']['english']}/{character['name']['full']}",
        "name": character['name']['full'],
        "anime": character['media']['nodes'][0]['title']['english'],
        "image": get_image_b64(data),
    }


@routes.get("/api/random")
async def api_get_random(request: Request):
    """
    Get a random set of anime picture from the internet
    """

    if random.randint(0, 1):
        data = await get_random_fake(request)
    else:
        data = await get_random_real(request)
    return json_response(data)

@routes.post("/api/savevote")
async def api_save_vote(request: Request):
    """
    Register a response by writing file id / 
    """
    result = await request.json()
    with open(VOTES_FILE, 'a') as f:
        f.write(str(result["key"]) + " " + str(result["vote"]) + "\n")
    return(json_response({"status": "ok"}))
    
