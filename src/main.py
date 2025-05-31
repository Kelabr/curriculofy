from fastapi import FastAPI
from .router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Libera o frontend que roda em localhost:3000
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Quem pode acessar
    allow_credentials=True,           # Se vai aceitar cookies/autenticação
    allow_methods=["*"],              # Métodos permitidos (GET, POST etc)
    allow_headers=["*"],              # Headers permitidos
)

app.include_router(router)

