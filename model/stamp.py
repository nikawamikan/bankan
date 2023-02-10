from discord import Interaction, InputTextStyle, File, SelectOption
from lib.database import DBConnection
from typing import Optional


class Stamp:
    def __init__(self, id: int, name: str, url: str) -> None:
        self.id = id
        self.name = name
        self.url = url


def add_stamp(user_id: int, name: str, url: str):
    with DBConnection() as db:
        db.insert(
            table="stamps",
            columns="name,url",
            values=((name, url),),
        )
        stamp_id = db.last_insert_id()
        db.insert(
            table="user_stamps",
            columns="user_id,stamp_id",
            values=((user_id, stamp_id,),),
        )


def get_stamp(value: str):
    with DBConnection(False) as db:
        id, name, url = db.select(
            sql="""
                select stamp_id, name, url
                from stamps
                where stamp_id = %s
                """,
            values=(int(value),)
        )[0]

    return Stamp(id, name, url)


def get_select_option_by_guild_id(guild_id: int):
    with DBConnection(False) as db:
        tmp = db.select(
            sql="""
            select name, url
            from stamps
            inner join guild_stamps using(stamp_id)
            where guild_id = %s 
            """,
            values=(guild_id,)
        )
        if len(tmp) == 0:
            raise Exception()
        select_options = [
            SelectOption(
                label=v[0], value=str(v[1])
            ) for v in tmp
        ]
        return select_options


def get_select_option_by_user_id(user_id: Optional[int]):
    with DBConnection(False) as db:
        tmp = db.select(
            sql="""
            select name, url
            from stamps
            inner join user_stamps using(stamp_id)
            where user_id = %s 
            """,
            values=(user_id,)
        )
        select_options = [
            SelectOption(
                label=v[0], value=str(v[1])
            ) for v in tmp
        ]
        return select_options
