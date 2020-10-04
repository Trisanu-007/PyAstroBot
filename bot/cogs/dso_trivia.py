import asyncio
import re
import os
import random
from typing import Optional

import discord
from discord.ext import commands

#from bot import database
#from bot.constants import Leaderboard, Trivia
from constants import Leaderboard, Trivia
import database


class Question:
    def __init__(self, path: str):
        self.answer = path.split("/")[1].replace("-", "")
        with open(path, "rb") as image:
            self.image = discord.File(image)

    @staticmethod
    def _fuzzy_search(search: str, target: str) -> float:
        """A simple scoring algorithm based on how many letters are found / total, with order in mind.
        Taken from PyDis' bot
        """
        REGEX_NON_ALPHANUMERIC = re.compile(
            r"\W", re.MULTILINE & re.IGNORECASE)

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
        self.dsos = []

        for dso in Trivia.dsos:
            for file in os.listdir(f"images/{dso}"):
                self.dsos.append(f"images/{dso}/{file}")
        # print(self.dsos)

    @commands.command()
    async def start(self, ctx) -> None:
        while True:
            dso = random.choice(self.dsos)
            print(dso)

            q = Question(dso)
            await ctx.send("What DSO is this?", file=q.image)

            try:
                message = await self.bot.wait_for("message", timeout=Trivia.timeout,
                                                  check=lambda m: q.check_guess(m.content) and not m.author.bot)
                print(message)
            except asyncio.TimeoutError:
                print("Error!")
                return
            else:
                # answered correctly
                await ctx.send(f"{message.author.mention} answered correctly!")
                await database.increment_score(message.author.id)

                print(message.content)

    @commands.command()
    async def leaderboard(self, ctx, n: Optional[int] = None) -> None:
        """
        Display leaderboard with `n` users, or `Leaderboard.default_size` if `n` is not given
        """

        n = n or Leaderboard.default_size

        rows = await database.get_top_n_scores(n)

        message = []
        for i, (id_, score) in enumerate(rows, 1):
            t = ctx.guild.get_member(id_)
            if t is None:
                message.append(f"{i} {self.bot.get_user(id_)} score {score}")
            else:
                message.append(f"{i} {t.nick or t.name} score {score}")

        if not message:
            await ctx.send("No one has answered correctly yet")
            return
        await ctx.send("\n".join(message))


def setup(bot) -> None:
    """Load the DsoTrivia cog."""
    bot.add_cog(DsoTrivia(bot))
