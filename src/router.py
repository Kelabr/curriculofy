from fastapi import APIRouter, status, Request, HTTPException
from fastapi.responses import JSONResponse
from .schemas import Users, Login, Admin
from .db.connection import connection
from .db.querys import create,filter,login, create_admin
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


@router.post('/user/admin')
def create_user(admin:Admin):
     response = create_admin(coon, admin.name, admin.email, admin.password)

     if response:
          return JSONResponse(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               content={'menssage':f'Erro ao cadastrar admin'}
          )
     data = {'name': admin.name, "category":"admin"}

     token = create_access_token(data)

     return JSONResponse(content={'Menssage': f"Usuário admin {admin.name}", 'token': f'{token}'})
    
     


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

    query_format = query.upper()

    return filter(coon, query_format)


@router.post('/login')
def login_user(data:Login):
    response = login(coon, data.email, data.password)

    print(response['menssage'])

    token = create_access_token(response)


    if response['menssage'] == 'Senha incorreta' or response['menssage'] == 'Nenhum usuário encontrado':
        return JSONResponse(
             status_code=status.HTTP_404_NOT_FOUND,
             content={'menssage': 'Erro ao tentar logar'}
        )
    

    return JSONResponse(status_code= status.HTTP_200_OK, content={'menssage': f'Usuário {response['menssage']} logado', 'token':f'{token}'})
         


