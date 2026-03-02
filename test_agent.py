import asyncio
from app.db.prisma_client import prisma_db
from app.services.agents.defect_agent import run_defect_agent

async def main():
    await prisma_db.connect()
    
    print("Testing defect agent...")
    res = await run_defect_agent("Give me all defects and their companies")
    print(f"RAW OUTPUT: {res}")
    
    await prisma_db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
