from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import uvicorn

# Importamos a função que liga o banco e o nosso "Cardápio" completo
from src.infra.database.connection import init_db
from src.api.graphql.schema import schema

# 1. Ciclo de Vida: Garante que o banco seja criado ao ligar o servidor


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# 2. Inicializamos o aplicativo FastAPI
app = FastAPI(lifespan=lifespan)

# 3. Configuração do CORS (O porteiro que permite seu Front-end acessar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Conectamos o GraphQL à rota /graphql
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    print("🚀 Servidor Clean Architecture rodando na porta 4000")
    # Passamos o caminho em string para o Uvicorn permitir o "reload" automático
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=4000, reload=True)
