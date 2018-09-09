import sys
import string
import random
import asyncio
import aiomysql

from app.utils import BASE_DIR, get_config

AMOUNT = 10000

LEVELS = ['trace', 'debug', 'info', 'warn', 'error', 'critical']

async def create_rows():
    rows = []
    for _ in range(AMOUNT):
        rows.append("INSERT INTO log_data VALUES (NULL, {}, \"{}\", \"{}\", \"{}\", \"{}\", NOW());".format(
            random.randint(1, AMOUNT), 
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)),
            LEVELS[random.randint(0, len(LEVELS)-1)], 
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=50)),
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=50)),
        ))
    return rows

async def populate_db(loop, config):
    pool = await aiomysql.create_pool(
        user=config['mysql']['user'], 
        password=config['mysql']['password'], 
        db=config['mysql']['database'],
        host=config['mysql']['host'], 
        port=config['mysql']['port'], 
        loop=loop
    )
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            rows = await create_rows()
            await cursor.execute("".join(rows))
            await conn.commit()

    pool.close()
    await pool.wait_closed()

config = get_config(sys.argv[1:])

loop = asyncio.get_event_loop()
loop.run_until_complete(populate_db(loop, config))