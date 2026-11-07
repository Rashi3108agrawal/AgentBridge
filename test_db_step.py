import asyncio
from agentbridge.db import Database, _alembic_upgrade

async def main():
    print("1. Creating Database...")
    db = Database('sqlite+aiosqlite:///:memory:')
    print("2. Entering db.engine.begin()...")
    async with db.engine.begin() as conn:
        print("3. Inside begin! Connection acquired.")
        print("4. Running _alembic_upgrade...")
        await conn.run_sync(_alembic_upgrade, "head")
        print("5. Upgrade finished!")
    print("6. Complete!")

asyncio.run(main())

