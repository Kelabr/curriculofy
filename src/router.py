from fastapi import APIRouter, status, Request, HTTPException
from fastapi.responses import JSONResponse
from .schemas import Users, Login, Admin
from .db.connection import connection
from .db.querys import create,filter,login, verify, oneUser
from .security import create_access_token, verify_access_token


router = APIRouter()
coon = connection()

# Cria um usuário
@router.post('/user')
def create_user(user:Users):
        response = create(coon, user.name, user.email, user.phone, user.password, user.occupation.upper())

        if response:
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"menssage": f"Erro ao cadastrar usuário"}
        )

        data = {'name':user.name, 'email':user.email}

        token = create_access_token(data)

        return JSONResponse(content={"menssage": f"Usuário {user.name} criado", 'token':f'{token}'})
     


#Filtra usuários pela profissão
@router.get('/user/occupation/{query}')
def filter_user_occupation(query:str, request:Request):

    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabeçalho Authorization ausente ou mal formatado"
         )

    token = auth_header.split(" ")[1]

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Token invalido ou expirado"
        )
    
    # Jeito errado de dar acesso admin
    # if payload.get('role') != 'admin':
    #      raise HTTPException(
    #           status_code=status.HTTP_403_FORBIDDEN,
    #           detail="Acesso permitido apenas para administradores"
    #      )

    email_payload = payload.get('email')

    user_if_admin = verify(coon, email_payload)

    if user_if_admin != None:
         user = oneUser(coon, email_payload)
         return JSONResponse(
              status_code=status.HTTP_200_OK,
              content={'data': f'{user}'}
         )

    query_format = query.upper()

    return filter(coon, query_format)


@router.post('/login')
def login_user(data:Login):
    response = login(coon, data.email, data.password)

    print(response['menssage'])


    if response['menssage'] == 'Senha incorreta' or response['menssage'] == 'Nenhum usuário encontrado':
        return JSONResponse(
             status_code=status.HTTP_404_NOT_FOUND,
             content={'menssage': 'Erro ao tentar logar'}
        )
    
    token = create_access_token(response)
    

    return JSONResponse(status_code= status.HTTP_200_OK, content={'menssage': f'Usuário {response['menssage']} logado', 'token':f'{token}'})