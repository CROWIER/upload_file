import traceback
from src.api.router import router
from src.config.database import engine
from fastapi import FastAPI, HTTPException
from src.config.minio_client import create_minio_client, init_minio_bucket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda x: None)
        client = create_minio_client()
        init_minio_bucket(client)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Database connection failed")
