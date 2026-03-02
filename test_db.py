import asyncio
from app.db.prisma_client import prisma_db
from app.services.agents.company_agent import run_company_agent

async def main():
    await prisma_db.connect()
    res = await run_company_agent("Give me all companies")
    print(f"OUTPUT: {res}")
    await prisma_db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
