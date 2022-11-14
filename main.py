import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from lib.imgen import BaseImages

BaseImages.add_image(
    key="bankan",
    image_path="./image/bankan_fukidashi.png",
    font_path="./font/uzura.ttf",
    base_positon=(1005, 175),
    font_size=100, max_width=346, max_vertical=648
)

intents = discord.Intents.default()
bot = commands.Bot(
    debug_guilds=[956778581160247366, 879288794560471050], intents=intents)
load_dotenv()
TOKEN = os.getenv('TOKEN')


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


@bot.slash_command()
async def test(ctx: discord.ApplicationContext):
    await ctx.respond("test")


bot.load_extensions(
    'cogs.bankan',
    store=False
)

bot.run(TOKEN)
