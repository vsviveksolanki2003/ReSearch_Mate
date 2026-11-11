"""Async database session, connection pool, and migration runner for PostgreSQL + pgvector."""
from pathlib import Path
from typing import List, Optional
from backend.app.config import settings

class DatabaseManager:
    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.database_url = database_url
        self._pool = None

    def load_migration_commands(self) -> List[str]:
        """Read and split schema.sql into individual DDL statements."""
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        if not schema_path.exists():
            return []
        
        with open(schema_path, "r", encoding="utf-8") as f:
            raw_sql = f.read()

        statements = []
        for stmt in raw_sql.split(";"):
            # Strip comment lines
            non_comment_lines = [l for l in stmt.split("\n") if not l.strip().startswith("--")]
            clean = "\n".join(non_comment_lines).strip()
            if clean:
                statements.append(clean + ";")
        return statements

    async def check_connection(self) -> str:
        """Probe PostgreSQL connection status."""
        try:
            import asyncpg
            conn = await asyncpg.connect(self.database_url, timeout=1.0)
            await conn.close()
            return "connected"
        except Exception:
            return "disconnected"

    async def init_pool(self):
        """Initialize connection pool and run pending schema migrations."""
        status = await self.check_connection()
        if status == "connected":
            try:
                import asyncpg
                self._pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=5)
                # Execute schema migrations
                async with self._pool.acquire() as conn:
                    for cmd in self.load_migration_commands():
                        await conn.execute(cmd)
            except Exception:
                pass

    async def close_pool(self):
        """Close connection pool."""
        if self._pool:
            await self._pool.close()

db_manager = DatabaseManager()
