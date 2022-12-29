import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option, SlashCommandOptionType
from view.comic import MessageInput
from model import image
Fonts = image.Fonts
Colors = image.Colors


class ComicCog(commands.Cog):

    def __init__(self, bot):
        print("start Comic init")
        self.bot = bot

    comic = SlashCommandGroup("comic", "comic風の文字埋め込みをするコマンド")

    @comic.command(name="bankan", description="晩柑ちゃんに色々喋らせるよ")
    async def bankan(
        self,
        ctx: discord.ApplicationContext,
        message: Option(
            str,
            description="改行は半角スペース2回",
            required=False
        ),
        mention: Option(
            SlashCommandOptionType.mentionable,
            description="メンションつける場合は追加",
            required=False),
        font_id: Option(
            int,
            name="font_style",
            description="指定しないデフォルトになります",
            choices=Fonts.get_font_options(),
            required=False
        ),
        font_color: Option(
            int,
            description="フォントの色を指定します",
            choices=Colors.get_color_options(),
            required=False
        )
    ):

        image_id = 30
        base_image = await image.get_image(
            image_id=image_id,
            message=message,
            font_style=Fonts.get_font(font_id=font_id),
            color=Colors.get_color(font_color)
        )

        if message == None:
            await ctx.response.send_modal(modal=MessageInput(title="言わせたい事入力してね", base_image=base_image, mention=mention))
            return
        else:
            message: str = message
            base_image.message = message.replace("  ", "\n")

        if mention == None:
            await ctx.response.send_message(file=await base_image.draw())
        else:
            await ctx.response.send_message(content=mention.mention, file=await base_image.draw())

    @comic.command(name="osato", description="おさとうちゃんに色々しゃべらせるよ")
    async def bankan(
        self,
        ctx: discord.ApplicationContext,
        message: Option(
            str,
            description="改行は半角スペース2回",
            required=False
        ),
        mention: Option(
            SlashCommandOptionType.mentionable,
            description="メンションつける場合は追加",
            required=False),
        font_id: Option(
            int,
            name="font_style",
            description="指定しないデフォルトになります",
            choices=Fonts.get_font_options(),
            required=False
        ),
        font_color: Option(
            int,
            description="フォントの色を指定します",
            choices=Colors.get_color_options(),
            required=False
        )
    ):

        image_id = 31
        base_image = await image.get_image(
            image_id=image_id,
            message=message,
            font_style=Fonts.get_font(font_id=font_id),
            color=Colors.get_color(font_color)
        )

        if message == None:
            await ctx.response.send_modal(modal=MessageInput(title="言わせたい事入力してね", base_image=base_image, mention=mention))
            return
        else:
            message: str = message
            base_image.message = message.replace("  ", "\n")

        if mention == None:
            await ctx.response.send_message(file=await base_image.draw())
        else:
            await ctx.response.send_message(content=mention.mention, file=await base_image.draw())

    # @comic.command(name="add", description="画像を追加します")
    # async def add(
    #     self,
    #     ctx: discord.ApplicationContext,
    #     name: Option(str, description="登録名称", ),
    #     image: Option(discord.Attachment, description="画像",),
    # ):
    #     user_id = ctx.user.id


def setup(bot):
    bot.add_cog(ComicCog(bot))
