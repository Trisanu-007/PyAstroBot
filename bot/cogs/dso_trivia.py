import re
import discord
from discord.ext import commands
from bot.constants import Db, Image
import aiomysql


class Question:
    def __init__(self, dso: str, n: int):
        self.answer = dso.replace("-", "")

        with open(f"images\\{dso}\\{n}", "rb") as image:
            self.image = discord.File(image)

    @staticmethod
    def _fuzzy_search(search: str, target: str) -> float:
        """A simple scoring algorithm based on how many letters are found / total, with order in mind."""
        REGEX_NON_ALPHANUMERIC = re.compile(r"\W", re.MULTILINE & re.IGNORECASE)

        current, index = 0, 0
        _search = REGEX_NON_ALPHANUMERIC.sub('', search.lower())
        _targets = iter(REGEX_NON_ALPHANUMERIC.split(target.lower()))
        _target = next(_targets)

        try:
            while True:
                while index < len(_target) and _search[current] == _target[index]:
                    current += 1
                    index += 1
                index, _target = 0, next(_targets)
        except (StopIteration, IndexError):
            pass
        return current / len(_search) * 100

    def check_guess(self, guess: str) -> bool:
        return Question._fuzzy_search(guess, self.answer) > 0.80


class DsoTrivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        raise NotImplemented

    @commands.command()
    async def leaderboard(self, ctx, n: int = None) -> None:
        conn = await aiomysql.connect(host=Db.host, user=Db.user, db=Db.db, port=Db.port, password=Db.password)

        async with await conn.cursor() as cursor:
            # default is to display top 5
            if n is None:
                n = 5
            await cursor.execute(f"SELECT name, correct_answers FROM score ORDER BY correct_answers DESC LIMIT 0, {n}")

        rows = await cursor.fetchall()

        message = "\n".join(f"id <@{id_}> score {score}" for id_, score in rows)

        await ctx.send(message)

    @commands.command()
    async def test(self, ctx):
        # haven't changed file names yet, still using real name for testing
        q = Question("3c273", "3c 273 optical")
        await ctx.send(file=q.image)


def setup(bot) -> None:
    """Load the DsoTrivia cog."""
    bot.add_cog(DsoTrivia(bot))
