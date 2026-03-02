from prisma import Prisma
from app.core.config import settings

# Global Prisma Client instance initialized with the dynamic URL from config
prisma_db = Prisma(
    datasource={
        "url": settings.DATABASE_URI
    }
)
