from fastapi.responses import Response
from fastapi import FastAPI
from model.image import get_image, Colors, Fonts

from collections import OrderedDict
from hashlib import md5


CACHE_MAX_SIZE = 500
CACHE_IMAGES = OrderedDict()


def get_hash_int(texts: list[str]) -> int:
    result = int(md5("".join(texts).encode()).hexdigest(), 16)
    return result


app = FastAPI()


# jsonを出力するとこ
@app.get("/color.json")
async def get_color_json():
    return Colors.get_color_options()


@app.get("/font.json")
async def get_font_json():
    return Fonts.get_font_options()


# 画像よぶとこ
@app.get("/{char_name:str}.png")
async def get_char_image(char_name: str,  message: str = "なんかよう？"):
    key = get_hash_int([char_name, message])

    if key in CACHE_IMAGES:
        byte_data = CACHE_IMAGES[key]
    else:
        # ここの処理をif文からdictから検索する方法に変更する

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

    return Response(content=byte_data, media_type="image/png")
