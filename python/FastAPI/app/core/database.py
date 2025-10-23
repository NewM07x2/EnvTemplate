"""Database configuration and Prisma client setup."""

from prisma import Prisma

# Global Prisma client instance
prisma = Prisma()


async def get_db() -> Prisma:
    """
    Dependency for getting database connection.
    
    Usage:
        @app.get("/items")
        async def get_items(db: Prisma = Depends(get_db)):
            items = await db.item.find_many()
            return items
    """
    if not prisma.is_connected():
        await prisma.connect()
    return prisma
