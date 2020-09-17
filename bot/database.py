import aiomysql
from bot.constants import Database


async def connect():
    return await aiomysql.connect(host=Database.host,
                                  user=Database.user,
                                  db=Database.db,
                                  port=Database.port,
                                  password=Database.password)


async def get_top_n_scores(n: int):
    conn = await connect()
    async with await conn.cursor() as cursor:
        # default is to display top 5
        if n is None:
            n = 5
        await cursor.execute(f"SELECT name, correct_answers FROM score ORDER BY correct_answers DESC LIMIT 0, {n}")

    rows = await cursor.fetchall()

    conn.close()

    return rows


async def increment_score(id_: int, increment: int = None) -> None:
    conn = await connect()
    async with await conn.cursor() as cursor:
        if increment is None:
            increment = 1

        await cursor.execute(f"UPDATE score SET correct_answers = correct_answers + {increment} WHERE name = {id_}")
        await conn.commit()

    conn.close()