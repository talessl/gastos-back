import jwt
from fastapi import Request, HTTPException

from src.infra.config import SECRET_KEY, ALGORITHM


async def get_context(request: Request):
    # 1. Olha o cabeçalho da requisição HTTP
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        # Se não tiver token, dizemos que não há usuário (ID = None)
        return {"usuario_id": None}

    # 2. Separa a palavra "Bearer" do token em si
    token = auth_header.split(" ")[1]

    try:
        # 3. A "Luz Negra": Faz a matemática com a SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 4. Devolve o ID do usuário para o GraphQL usar
        return {"usuario_id": payload.get("sub")}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expirado. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")
