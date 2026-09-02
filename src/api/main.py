from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from src.api.graphql.context import get_context
import uvicorn

from src.infra.database.connection import init_db
from src.api.graphql.schema import schema

# 1. Ciclo de Vida: Garante que o banco seja criado ao ligar o servidor


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    print("🚀 Servidor Clean Architecture rodando na porta 4000")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=4000, reload=True)
