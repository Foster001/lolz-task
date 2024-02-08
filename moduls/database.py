import asyncio
import aiosqlite


async def register_base(base: str, start_sql_request: str = None) -> aiosqlite.Connection:
    db = await aiosqlite.connect(base)
    if start_sql_request is not None:
        # Перебор всех sql запросов, и отправление каждого из них (если сразу отправить это все одним запросом, то не работает)
        [await db.execute(j + ';') for j in start_sql_request.split(';')]
        await db.commit()
    return db

class Base(): # Это мой личный модуль базы данных, если будете брать его в свои проекты - прошу уведомить меня об этом
    def __init__(self, base: str, start_sql_request: str = None):
        loop = asyncio.get_event_loop()
        self.db = loop.run_until_complete(register_base(base, start_sql_request))

    async def __get_dict_from_request(self, *args, q: tuple) -> dict:
        # Получение значения из базы данных в виде списка, не понимаете что это такое - не используйте

        args = str(args[0])
        s = {}
        splits = args.split('SELECT')[1].split('FROM')[0].split(',')
        for c in range(len(splits)):

            # Это надо что бы было красиво
            j = splits[c].replace(' ', '').replace(".", "_").replace('`', '')

            if len(j.split('(')) >= 2: j = j.split('(')[1].replace(')', '')
            s[j] = q[c]
        return s

    async def fetchone(self, *args, is_dict: bool = False) -> dict | tuple:
        q = await self.db.execute(*args)
        q = await q.fetchone()
        if is_dict is True and q is not None:
            s = await self.__get_dict_from_request(*args, q=q)
            return s
        return q

    async def fetchall(self, *args, is_dict: bool = False) -> dict | tuple:
        q = await self.db.execute(*args)
        q = await q.fetchall()
        if is_dict is True:
            s = []
            for j in q:
                s_ = await self.__get_dict_from_request(*args, q=j)
                s.append(s_)
            return s
        return q

    async def execute(self, *args) -> bool:
        await self.db.execute(*args)
        return True

    async def commit(self) -> bool:
        await self.db.commit()
        return True