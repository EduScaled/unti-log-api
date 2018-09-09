import sys
import asyncio
import aiomysql

from app.utils import BASE_DIR, get_config

commands = [
    "DROP DATABASE IF EXISTS unti_log;",
    "CREATE DATABASE unti_log CHARACTER SET utf8mb4;",
    "USE unti_log;",
    "GRANT ALL PRIVILEGES ON unti_log.* TO root;",
    "CREATE TABLE log_data (" \
        "id INT NOT NULL PRIMARY KEY AUTO_INCREMENT," \
        "user_id INT NOT NULL," \
        "email VARCHAR(100)," \
        "type VARCHAR(20) NOT NUlL," \
        "action VARCHAR(256) NOT NUlL," \
        "url VARCHAR(512)," \
        "created_at TIMESTAMP NOT NULL" \
    ");"
]

async def create_db(commands, config, loop):
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
            await cursor.execute("".join(commands))
            await conn.commit()

    pool.close()
    await pool.wait_closed()

config = get_config(sys.argv[1:])

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db(commands, config, loop))