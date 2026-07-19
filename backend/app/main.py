from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.document_router import router as document_router
from app.routers.collection_router import router as collection_router
from app.routers.conversation_router import router as conversation_router
from app.routers.admin_router import router as admin_router
from app.routers.log_router import router as log_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "RAG API is running"}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(document_router)
app.include_router(collection_router)
app.include_router(conversation_router)
app.include_router(admin_router)
app.include_router(log_router)