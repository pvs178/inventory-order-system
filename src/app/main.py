from fastapi import FastAPI

from app.api.orders import router as orders_router

app = FastAPI(title="Inventory Order System")
app.include_router(orders_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
