from discord.ext import commands
from constants import Db
import aiomysql
import asyncio


class DsoTrivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        raise NotImplemented

    @commands.command()
    async def leaderboard(self, ctx):
        conn = await aiomysql.connect(host=Db.host, user=Db.user, db=Db.db, port=Db.port, password=Db.password)

        await conn.cursor()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM score")

        rows = await cursor.fetchall()

        message = "\n".join(f"id {id_} score {score}" for id_, score in rows)

        await ctx.send(message)


def setup(bot) -> None:
    bot.add_cog(DsoTrivia(bot))
