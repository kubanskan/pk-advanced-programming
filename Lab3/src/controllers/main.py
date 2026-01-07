import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..infrastructure.db.database import init_db, SessionLocal
from .cart_controller import router as cart_router
from ..infrastructure.db.repository import SQLAlchemyCartRepository
from ..infrastructure.background_jobs.cleanup_service import CartCleanupService
import uvicorn


async def run_cleanup_loop():
    while True:
        try:

            db = SessionLocal()
            repo = SQLAlchemyCartRepository(db)
            service = CartCleanupService(repo)

            service.clean_old_carts(inactivity_minutes=5)

            db.close()
        except Exception as e:
            print(f'Błąd w zadaniu czyszczącym: {e}')

        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    cleanup_task = asyncio.create_task(run_cleanup_loop())

    yield

    cleanup_task.cancel()


app = FastAPI(
    title='System Koszyka Zakupowego',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(cart_router)

if __name__ == '__main__':
    uvicorn.run('src.controllers.main:app', host='127.0.0.1', port=8000, reload=True)
