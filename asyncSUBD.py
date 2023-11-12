import asyncpg
import asyncio
import threading


async def main():
    mutex = threading.Lock()

    async def Insert_bad_news():
        while True:
            await asyncio.sleep(1)
            # mutex.acquire() # блокировка ресурса БД для операции вставки и удаления
            # await conn.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 1');''')
            values = await conn.fetch('''SELECT * FROM test''')
            for value in values:
                print(value[0])
            # await conn.fetch('''DELETE FROM test WHERE result = 'Выполнен запрос 1';''')
            # mutex.release() # разблокировка ресурса БД для операции вставки и удаления
            await asyncio.sleep(7)

    async def Insert_good_news():
        while True:
            # mutex.acquire()
            # await conn.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 2');''')
            values = await conn.fetch('''SELECT * FROM test''')
            for value in values:
                print(value[0])
            # await conn.fetch('''DELETE FROM test WHERE result = 'Выполнен запрос 1';''')
            # mutex.release()
            await asyncio.sleep(2)

    conn = None
    try:
        conn = await asyncpg.connect(user='USER', password='12345', database='postgres', host='localhost', port=5432)
        await conn.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 2');''')
        await conn.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 1');''')
        await asyncio.gather(Insert_bad_news(), Insert_good_news())  # запуск 2 веток асинхронных потоков
    except Exception as e:
        print(e)
    finally:
        await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
