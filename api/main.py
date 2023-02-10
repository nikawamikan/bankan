from datetime import datetime
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI
from model.image import get_image
app = FastAPI()


@app.get("/{char_name:str}")
async def genshin_photo(char_name: str, text: str):
    return
