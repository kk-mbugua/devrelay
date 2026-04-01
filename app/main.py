from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session

@asynccontextmanager
async def lifespan_context_manager(app):
    print("Application 'Devrelay' has been initiated")
    # anything that needs to calculated before and after should be started here and concluded after the yield
    yield
    print("Application 'Devrelay' is shuting down...")

app = FastAPI(lifespan=lifespan_context_manager)
    
    
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    return {"status": "ok", "service": "devrelay"}
