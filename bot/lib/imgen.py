from lib.database import DBConnection
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord import File


class DrawText:

    def __init__(self, image_path: str, font_path: str, font_color: tuple[int, int, int, int], base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int, message: str):
        self.image = Image.open(fp=image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = font_size
        self.font_path = font_path
        self.font_color = font_color
        self.base_position = base_positon
        self.max_width = max_width
        self.max_vertical = max_vertical
        self.xy_per = max_vertical / max_width
        self.message = message
        self.outline = (0x4B, 0x4b, 0x4b, 0xFF)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.image.close()

    async def draw_text(self, text: str, position: tuple[int, int]):
        x = self.base_position[0] + position[0]
        y = self.base_position[1] + position[1]
        self.draw.text((x, y), text=text, fill=self.font_color)

    async def draw_multitext(self):
        font_size = self.width
        texts = self.message.split("\n")
        lines = len(texts)

        max_text = ""
        for v in texts:
            if len(max_text) < len(v):
                max_text = v

        font = ImageFont.truetype(font=self.font_path, size=font_size)

        vertical_size = self.draw.textlength(
            text=max_text,
            font=font,
            direction="ttb"
        )

        width_size = self.width * lines
        if vertical_size > self.max_vertical or width_size > self.max_width:
            if vertical_size > width_size * self.xy_per:
                font_size = int(font_size * (self.max_vertical/vertical_size))
            else:
                font_size = int(font_size * (self.max_width/width_size))

            font = ImageFont.truetype(font=self.font_path, size=font_size)

            vertical_size = self.draw.textlength(
                text=max_text,
                font=font,
                direction="ttb"
            )

        y = self.base_position[1] + (self.max_vertical - vertical_size)/2

        x = self.base_position[0] + (font_size * (lines-1))/2

        for v in texts:
            self.draw.text(
                xy=(x, y),
                text=v, fill=self.font_color,
                anchor="mt",
                font=font,
                direction="ttb",
                language="ja",
                stroke_width=3,
                stroke_fill=self.outline,
            )
            x -= font_size

    async def show(self):
        self.image.show()

    async def get_discord_file(self):
        fileio = BytesIO()
        self.image.save(fileio, format="png")
        fileio.seek(0)
        return File(fp=fileio, filename="image.png")

    async def save(self, file_path: str):
        self.image.save(fp=file_path, format="png")
