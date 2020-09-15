from discord.ext import commands
from constants import Bot


bot = commands.Bot(command_prefix=commands.when_mentioned_or(Bot.prefix))


# Commands
bot.load_extension("cogs.test")
bot.load_extension("cogs.dso_trivia")


bot.run(Bot.token)
