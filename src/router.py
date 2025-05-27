from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .schemas import Users, Login
from .db.connection import connection
from .db.querys import create,filter,login
from .security import create_access_token


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

        data = {'name':user.name}

        token = create_access_token(data)

        return JSONResponse(content={"menssage": f"Usuário {user.name} criado", 'token':f'{token}'})


#Filtra usuários pela profissão
@router.get('/user/occupation/{query}')
def filter_user_occupation(query:str):
    query_format = query.upper()

    return filter(coon, query_format)


@router.post('/login')
def login_user(data:Login):
    response = login(coon, data.email, data.password)

    print(response['menssage'])

    token, minuted_valided = create_access_token(response)


    if response['menssage'] == 'Senha incorreta' or response['menssage'] == 'Nenhum usuário encontrado':
        return JSONResponse(
             status_code=status.HTTP_404_NOT_FOUND,
             content={'menssage': 'Erro ao tentar logar'}
        )
    

    return JSONResponse(status_code= status.HTTP_200_OK, content={'menssage': f'Usuário {response['menssage']} logado', 'token':f'{token}', 'minuted_valid':f'{minuted_valided}m'})
         
    
   
    
 
     
