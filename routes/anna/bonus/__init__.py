from fastapi import  APIRouter, File, UploadFile
from lib.engine import s
from routes.anna.permissions import get_manager_data
from lib.save_base64_file import save_base64_file
from lib.send_mes import send_mes



router = APIRouter()
@router.post('/order/{bonus_id}')
async def x(bonus_id: int, R:dict): # attach: UploadFile = File(...)
    print('R:',R)
    form_errors={}
    errors=[]

    success=1
    if not R['attach']:
        form_errors['attach']='необходимо выбрать файл'
        success=0
    
    if not R['comment']:
        R['comment']=1
    
    manager=get_manager_data()
#    print("\n\n\nmanager:",manager)
    bonus=s.db.query(
        query='''
            SELECT
                b.*,ul.header ur_lico
            from
                bonus b
                LEFT join ur_lico ul ON b.partner_id=ul.id
            WHERE b.id=%s
        ''',
        values=[bonus_id],
        onerow=1
    )
#    print("bonus:",bonus)
    
    if not (bonus['partner_id'] in manager['ur_lico_hash']):
        errors.append('У Вас нет прав оставлять заявку для данного бонуса')
        success=0

    if success:

        # Сохраняем форму
        insert_id=s.db.save(
            table='bonus_order',
            data={
                'comment':R['comment'],
                'bonus_id':bonus_id,
                'manager_id':manager['id']
            }
        )
        
        if insert_id: # Сохраняем файл
            
            filename=save_base64_file(
                orig_filename=R['attach']['orig_name'],
                src=R['attach']['src'],
                filedir=f"./files/bonus_order",
                #filename=f"{random_filename()}.{ext}"
                
            )
            
            if filename:
                s.db.query(
                    query='UPDATE bonus_order SET attach=%s where id=%s',
                    values=[filename,insert_id],
                )
                
                send_mes(
                    to=manager['ma_email'],
                    subject=f"отправка акта с сайта {s.env['host']} {manager['ma_name_f']} {manager['ma_name_i']} {manager['ma_name_o']}",
                    message=f"""
                        Акт №{bonus['number']}<br>
                        <p>{manager['name_f']} {manager['name_i']} {manager['name_o']}<br>
                        
                        Юридическое лицо: {bonus['ur_lico']}<br>
                        <a href="https://{s.env["host"]}/files/bonus_order/{filename}">файл акта</a>
                    """
                )

        
        

    return {'success':success, 'form_errors':form_errors,'errors':errors}


