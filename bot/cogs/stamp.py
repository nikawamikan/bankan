import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option, OptionChoice, SlashCommandOptionType
from model import stamp
from view.stamp import StampView


class StampCog(commands.Cog):

    def __init__(self, bot):
        print("start Stamp init")
        self.bot = bot

    stamp = SlashCommandGroup("stamp", "スタンプを推したり追加するコマンド")

    @stamp.command(name="add", description="スタンプを追加するよ")
    async def adding(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, description="画像につける名前を決めてね"),
        image: Option(discord.Attachment, description="画像を添付してね")
    ):
        image: discord.Attachment = image
        stamp.add_stamp(user_id=ctx.user.id, name=name, url=image.url)
        await ctx.respond(f"{name} を登録したよ")

    @stamp.command(name="pong", description="スタンプを貼るよ")
    async def pong(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.interaction.response.send_message(view=StampView(guild_id=ctx.guild.id))


def setup(bot):
    bot.add_cog(StampCog(bot))
