import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!")

bot.load_extension(f"cogs.test")

bot.run(os.environ.get("BOT_TOKEN"))
