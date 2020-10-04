from discord.ext import commands
from constants import Bot
#from bot.constants import Bot


bot = commands.Bot(command_prefix=commands.when_mentioned_or(Bot.prefix))


# Commands
bot.load_extension("cogs.dso_trivia")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(Bot.token)
