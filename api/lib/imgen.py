from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord import File


class DrawText:
    """画像に対して指定座標にテキストを合成するためのクラスです。with句によって利用されることが好ましいです。
    """

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

    async def draw_multitext(self) -> None:
        """縦方向に対して複数行のテキストを合成します。
        """
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

        x = self.base_position[0] + self.max_width/2
        x += (font_size * (lines-1))/2
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
        """画像を表示します。これはデバッグ用であるため、本番環境で利用は推奨されません。
        """
        self.image.show()

    async def get_bytes(self):
        fileio = BytesIO()
        self.image.save(fileio, format="png")
        fileio.seek(0)
        return fileio

    async def get_discord_file(self):
        return File(fp=await self.get_bytes(), filename="image.png")

    async def save(self, file_path: str):
        """画像をファイルを保存します。
        Args:
            file_path (str): ファイルのパスを指定します。png形式で保存するため名称にpngが含まれている必要があります。"""
        self.image.save(fp=file_path, format="png")
