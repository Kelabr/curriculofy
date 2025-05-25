from fastapi import status
from fastapi.responses import JSONResponse
import bcrypt


def create(coon, name, email, phone, password, occupation):

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        with coon.cursor() as cur:
            cur.execute('INSERT INTO users (name, email, phone, password, occupation) VALUES (%s, %s, %s, %s, %s)', (name, email, phone, password_hash, occupation))
        coon.commit()

    except Exception as e:
        print(f"erro: {e}")
        coon.rollback()
        return JSONResponse(status_code=500, content={"menssage": f"Erro ao cadastrar usuário - {str(e)}"})
    

def filter(coon, path):
        with coon.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE occupation=%s', (path,))
            result = cur.fetchall()

            print(result)

            if not result:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"menssage": "Nenhum usuário encontrado"}
                )
        
        filtered = [{"name":r[1], "email":r[2]} for r in result]
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"menssage": filtered}
        )


def login(coon, email, password):
    with coon.cursor() as cur:
        cur.execute('SELECT * FROM users WHERE email=%s', (email,))
        user = cur.fetchone()


        if not user:
            return {'menssage': 'Nenhum usuário encontrado'}
            
    
        password_storege_hash = user[4].encode('utf-8')
        password_hash = bcrypt.checkpw(password.encode('utf-8'), password_storege_hash )
        

        if not password_hash:
            return {'menssage': 'Senha incorreta'}

        
        return {'menssage': f'{user[1]}'}
        
        
        


        
    


