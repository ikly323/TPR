import asyncpg
import asyncio
import threading


async def main():
    async def Insert_bad_news():
        while True:
            await asyncio.sleep(1)
            await conn1.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 1');''')
            # Команда внесения данных в БД
            values = await conn1.fetch('''SELECT * FROM test''')
            # Команда вывода данных из БД
            for value in values:
                print(value[0])
            await conn1.fetch('''DELETE FROM test WHERE result = 'Выполнен запрос 1';''')
            # Команда для удаления данных из БД
            await asyncio.sleep(7)
            # Команда засыпания на 7 секунд

    async def Insert_good_news():
        while True:
            await conn2.fetch('''INSERT INTO test (result) VALUES ('Выполнен запрос 2');''')
            values = await conn2.fetch('''SELECT * FROM test''')
            for value in values:
                print(value[0])
            await conn2.fetch('''DELETE FROM test WHERE result = 'Выполнен запрос 2';''')
            await asyncio.sleep(2)

    conn1 = None
    conn2 = None
    try:
        conn1 = await asyncpg.connect(user='USER', password='12345', database='postgres', host='localhost', port=5432)
        # Первое соединение с БД
        conn2 = await asyncpg.connect(user='USER', password='12345', database='postgres', host='localhost')
        # Второе соединение с БД
        await asyncio.gather(Insert_bad_news(), Insert_good_news())  # запуск 2 веток асинхронных потоков
    except Exception as e:
        print(e)
    finally:
        await conn1.close()
        await conn2.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
