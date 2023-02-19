from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from model.image import get_image
app = FastAPI()


@app.get("/{char_name:str}.png")
async def get_char_image(char_name: str,  message: str):
    if char_name == "bankan":
        data = await get_image(image_id=30, message=message)
    elif char_name == "gomi":
        data = await get_image(image_id=30, message=message)
    else:
        raise ValueError("is not a valid")

    return StreamingResponse(content=await data.get_bytes(), media_type="image/png")
