from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from model.image import get_image
from collections import OrderedDict
from hashlib import md5


CACHE_MAX_SIZE = 500
CACHE_IMAGES = OrderedDict()


def get_hash_int(texts: list[str]) -> int:
    result = int(md5("".join(texts).encode()).hexdigest(), 16)
    return result


app = FastAPI()


@app.get("/{char_name:str}.png")
async def get_char_image(char_name: str,  message: str):
    key = get_hash_int([char_name, message])

    if key in CACHE_IMAGES:
        byte_data = CACHE_IMAGES[key]
    else:
        if char_name == "bankan":
            data = await get_image(image_id=30, message=message)
        elif char_name == "gomi":
            data = await get_image(image_id=30, message=message)
        else:
            raise ValueError("is not a valid")

        byte_data = await data.get_bytes()
        CACHE_IMAGES[key] = byte_data

        if len(CACHE_IMAGES) > CACHE_MAX_SIZE:
            CACHE_IMAGES.popitem(False)

    return StreamingResponse(content=byte_data, media_type="image/png")
