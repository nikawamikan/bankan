import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option, OptionChoice, SlashCommandOptionType


def hacker_chugakuse(name: str, server: str):
    return \
        f"""
こんにちは、Twitterを始めてみました。{name}です。
僕は{server}の住人と会話した事があり、かつ{server}のメンバーです。
ちなみに好きなパソコンは使えれば何でもいいです。
よろしくお願いします🙏
"""


class NankaCog(commands.Cog):

    def __init__(self, bot):
        print("start Nanka init")
        self.bot = bot

    nanka = SlashCommandGroup("nanka", "なんか")

    @nanka.command(name="hacker", description="ハッカーになれるよ")
    async def adding(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, description="名前", default="ハッカー中学生"),
        server: Option(str, description="サーバー名", default="ふぃぼ鯖")
    ):
        await ctx.respond(content=hacker_chugakuse(name, server))


def setup(bot):
    bot.add_cog(NankaCog(bot))
