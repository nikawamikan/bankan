from copy import copy
from lib.database import DBConnection
from lib.imgen import DrawText
from discord import File, OptionChoice


def color_to_tuple(color: int) -> tuple[int, int, int, int]:
    return (
        color >> 16,
        (color & 0xFF00) >> 8,
        color & 0xFF,
        0xFF
    )


class Color:
    def __init__(self, value: tuple[int, int, int, int], name: str) -> None:
        self.value = value
        self.name = name


class Colors:
    __DATA: dict[int: Color] = {}
    with DBConnection(False) as db:
        data = db.select(
            sql="select color_id, color, name from colors"
        )
        __DATA: dict[int, Color] = {
            v[0]: Color(color_to_tuple(v[1]), v[2]) for v in data
        }

    def get_color_options() -> list[OptionChoice]:
        return [
            OptionChoice(name=v.name, value=k) for k, v in Colors.__DATA.items()
        ]

    def get_color(color_id: int):
        if color_id not in Colors.__DATA:
            return None
        return Colors.__DATA[color_id].value


class Font:
    def __init__(self, value: str, name: str) -> None:
        self.value = value
        self.name = name


class Fonts:

    __DATA: dict[int: Font] = {}

    with DBConnection(False) as db:
        data = db.select(
            sql="select font_id, font_path, name from fonts"
        )
        __DATA: dict[int, Font] = {
            v[0]: Font(v[1], v[2]) for v in data
        }

    def get_font_options() -> list[OptionChoice]:
        return [
            OptionChoice(name=v.name, value=k) for k, v in Fonts.__DATA.items()
        ]

    def get_font(font_id: int):
        if font_id not in Fonts.__DATA:
            return None
        return Fonts.__DATA[font_id].value


class BaseImages:
    def __init__(self, image_path: str, font_path: str, font_color: tuple[int, int, int, int], base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int):
        self.image_path = image_path
        self.font_path = font_path
        self.font_color = font_color
        self.font_size = font_size
        self.base_position = base_positon
        self.max_width = max_width
        self.max_vertical = max_vertical
        self.message: str = None

    async def draw(self):
        with DrawText(
            image_path=self.image_path,
            font_path=self.font_path,
            font_color=self.font_color,
            base_positon=self.base_position,
            font_size=self.font_size,
            max_width=self.max_width,
            max_vertical=self.max_vertical,
            message=self.message
        ) as draw:
            await draw.draw_multitext()
            return await draw.get_discord_file()


def add_image(key: str, image_path: str, font_id: int, base_positon: tuple[int], font_size: int, max_width: int, max_vertical: int, color_id: int):
    with DBConnection() as db:
        db.insert(
            table="image_datas",
            columns="image_path, font_size, font_id, x, y, max_width, max_vertical, color_id",
            values=((image_path, font_size, font_id,
                    base_positon[0], base_positon[1], max_width, max_vertical, color_id),)
        )

        index = db.last_insert_id()

        db.insert(
            table="image_names",
            columns="name, image_id",
            values=((key, index),),
        )
        db.commit()

        __DATA[index] = BaseImages(
            image_path=image_path,
            font_path=db.select(
                sql="select font_path from fonts where font_id = %s",
                values=((font_id,),),
            )[0][0],
            base_positon=base_positon,
            font_size=font_size,
            max_width=max_width,
            max_vertical=max_vertical,
            font_color=Colors.get_color(color_id=color_id)
        )


async def get_image(image_id: int, message: str, font_style: int = None, color: tuple[int, int, int, int] = None) -> BaseImages:
    data: BaseImages = copy(__DATA[image_id])
    data.message = message
    if font_style != None:
        data.font_path = font_style
    if color != None:
        data.font_color = color
    return data


with DBConnection(False) as db:
    tmp = db.select(
        sql="""
        select image_id, image_path, font_size, font_path, x, y, max_width, max_vertical, color
        from image_datas
        inner join fonts using(font_id)
        inner join colors using(color_id)
        """
    )
    __DATA = {v[0]: BaseImages(
        image_path=v[1],
        font_size=v[2],
        font_path=v[3],
        base_positon=(v[4], v[5],),
        max_width=v[6],
        max_vertical=v[7],
        font_color=color_to_tuple(v[8])
    ) for v in tmp}

    print([d for d in tmp])
