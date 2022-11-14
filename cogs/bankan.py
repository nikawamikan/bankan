import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option
from view.bankan import MessageInput
from lib.imgen import BaseImages


class BankanCog(commands.Cog):

    def __init__(self, bot):
        print("start bankan init")
        self.bot = bot

    bankan = SlashCommandGroup("bankan", "晩柑ちゃんを晩柑するコマンド")

    @bankan.command(name="comic", description="色々喋らせるよ")
    async def comic(
        self,
        ctx: discord.ApplicationContext,
        message: Option(str, description="改行は半角スペース2回", required=False)
    ):
        if message == None:
            await ctx.response.send_modal(modal=MessageInput(title="言わせたい事入力してね"))
            return
        message: str = message

        await ctx.response.send_message(file=await BaseImages.get_imege(key="bankan", message=message.replace("  ", "\n")))


def setup(bot):
    bot.add_cog(BankanCog(bot))
