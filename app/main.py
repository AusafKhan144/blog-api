from app.dependencies import validate_token
from app.endpoints import article
from fastapi import FastAPI, Depends
from app.db import init_db
import uvicorn
from fastapi_pagination import add_pagination


def startup():
    """Initializing Databse on startup"""
    init_db()


def shutdown():
    pass


app = FastAPI(
    title="Blog Service API",
    description="A basic blog service API",
    on_startup=[startup],
    on_shutdown=[shutdown],
)

app.include_router(article.router, dependencies=[Depends(validate_token)])
add_pagination(app)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"detail": "Server Is Running!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
