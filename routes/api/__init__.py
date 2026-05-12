from fastapi import APIRouter, Request, Header, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()



"""
create table translab_tg_account(
id bigint unsigned primary key comment 'account telegram',
username varchar(50) not null default '',
first_name varchar(100) not null default '',
last_name varchar(100) not null default '',
phone varchar(50) not null default '',
registered datetime
) engine=innodb default charset=utf8 comment 'известные боту translab пользователи';

create table translab_tg_account
curl -X POST "http://127.0.0.1:5000/api/translab-create-tg-user" \
-H "X-API-Key: 4e7b8c1d9f2a3c5e6d7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6" \
-H "Content-Type: application/json" \
-d '{"id":815516108, "username": "john_doe", "first_name": "Вася", "last_name":"Прошкин"}'

"""

class UserCreateRequest(BaseModel):
    id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""


#def valid_key(k):
#    return k=='4e7b8c1d9f2a3c5e6d7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6'
def validate_key(x_api_key: str = Header(None)):
    valid_key = '4e7b8c1d9f2a3c5e6d7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6'
    if x_api_key != valid_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

async def get_tg_user(user: UserCreateRequest):
    db=get_db()
    return await db.query(
        query="SELECT * FROM translab_tg_account where id=%s",
        values=[user.id],
        onerow=1
    )

# Проверка (создание) пользователя из бота
@router.post('/translab-create-tg-user')
async def create_tg_user(
    user: UserCreateRequest,
    x_api_key: str = Depends(validate_key)
):
    db=get_db()
    if user.id and (type(user.id)==int):
        exists_user=await get_tg_user(user)
        print('exists_user:',exists_user)
        data={
            'id':user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
        }
        if exists_user:
            # пользователь существует?
            if exists_user['username']!=user.username or exists_user['first_name']!=user.first_name or exists_user.last_name !=user.last_name:
                # если нужно -- обновляем
                await db.save(
                    table='translab_tg_account',
                    data=data,
                    update=1,
                    where=f"id={user['id']}",
                    debug=1
                )
        else:
            data['registered']='func:now()'
            await db.save(
                table='translab_tg_account',
                data=data,
                debug=1
            )

@router.post('/translab-tg_user-request/{number_auto}')
async def save_request(    user: UserCreateRequest, number_auto: str, x_api_key: str = Header(None)):
    # Сохраняем информацию о запросе пользователя
    exists_user=get_tg_user(user)
    if not(exists_user):
        ...
    if exists_user:
        await db.save(
            table=''
        )


