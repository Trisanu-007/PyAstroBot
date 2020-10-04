import aiomysql
from constants import Database

from typing import Optional


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


async def get_by_id(id_: int) -> Optional[int]:
    """Return score of user with id `id_` if it exists, else None"""
    conn = await connect()
    async with await conn.cursor() as cursor:
        await cursor.execute(f"SELECT correct_answers FROM score WHERE name={id_}")

    score = await cursor.fetchone()

    conn.close()

    return score


async def create_user(id_: int) -> None:
    """Create a new user in the database"""
    conn = await connect()
    async with await conn.cursor() as cursor:
        await cursor.execute(f"INSERT INTO score VALUES ({id_}, 1)")

        await conn.commit()

    conn.close()


async def increment_score(id_: int) -> None:
    """Increment score of `id_` by `increment`"""
    conn = await connect()
    async with await conn.cursor() as cursor:
        await cursor.execute(f"UPDATE score SET correct_answers = correct_answers + 1 WHERE name = {id_}")
        await conn.commit()

    conn.close()
