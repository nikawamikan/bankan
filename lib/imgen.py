from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord import File


class Colors:
    PALE_PINK = (0xF2, 0xB3, 0xD6, 0xff)
    PINK = (0xF2, 0x4B, 0xC6, 0xff)
    SKY_BLUE = (0xA0, 0xF2, 0xE3, 0xff)
    LIGHT_GREEN = (0x04, 0xD9, 0x8B, 0xff)
    YELLOW = (0xF2, 0xE6, 0x41, 0xff)
    GRAY = (0x4B, 0x4b, 0x4b, 0xFF)


class DrawText:

    def __init__(self, image_path: str, font_path: str, base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int):
        self.image = Image.open(fp=image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = font_size
        self.font_path = font_path
        self.base_position = base_positon
        self.max_width = max_width
        self.max_vertical = max_vertical

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.image.close()

    async def draw_text(self, text: str, position: tuple[int, int], color: tuple[int, int, int, int]):
        x = self.base_position[0] + position[0]
        y = self.base_position[1] + position[1]
        self.draw.text((x, y), text=text, fill=color)

    async def draw_multitext(self, text: str, color: tuple[int, int, int, int]):
        font_size = self.width
        texts = text.split("\n")
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
            if vertical_size > width_size * 1.87:
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
                text=v, fill=color,
                anchor="mt",
                font=font,
                direction="ttb",
                language="ja",
                stroke_width=3,
                stroke_fill=Colors.GRAY,
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


class BaseImages:
    def __init__(self, image_path: str, font_path: str, base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int):
        self.image_path = image_path
        self.font_size = font_size
        self.font_path = font_path
        self.base_position = base_positon
        self.max_width = max_width
        self.max_vertical = max_vertical

    __DATA = {}

    def add_image(key: str, image_path: str, font_path: str, base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int):
        BaseImages.__DATA[key] = BaseImages(
            image_path=image_path,
            font_path=font_path,
            base_positon=base_positon,
            font_size=font_size,
            max_width=max_width,
            max_vertical=max_vertical
        )

    async def get_imege(key: str, message: str) -> File:
        data: BaseImages = BaseImages.__DATA[key]
        with DrawText(
            image_path=data.image_path,
            font_path=data.font_path,
            base_positon=data.base_position,
            font_size=data.font_size,
            max_width=data.max_width,
            max_vertical=data.max_vertical
        ) as draw:
            await draw.draw_multitext(text=message, color=Colors.SKY_BLUE)
            return await draw.get_discord_file()
