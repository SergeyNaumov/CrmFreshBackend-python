import os, shutil
from lib.core import get_ext
from lib.all_configs import read_config
from fastapi import UploadFile
from lib.send_mes_tg_and_email import send_mes_tg_and_email

async def upload_scan(request, config, field_name, form_id, docpack_id, attach):
            
    # get extension from oroginal file name
    
        
    # get extension from oroginal file name

    
    form = await read_config(
        request=request,
        action='upload_scan',
        config=config,
        script='docpack',
        field_name=field_name,
        id=form_id
    )
    dogovor = await form.db.query(
        query="""
            select
                d.number, d.registered, u.manager_id u__manager_id,
                u.firm, u.id u__id
            from
                dogovor d
                join docpack dp ON dp.id=d.docpack_id
                join user u ON u.id=dp.user_id
            where d.docpack_id=%s
        """,
        values=[docpack_id],
        onerow=1
    )
    ext=get_ext(attach.filename) ; result=''

    if not(dogovor):
        form.append('не найден договор')
    elif not(dogovor['registered']):
        form.append('не указана дата создания договора')
    else:
        registered=str(dogovor['registered'])
        save_dir=f"./files/dogovor-scan/{'/'.join(registered.split('-'))}"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_filename=f"{docpack_id}.{ext}"

        scan_file=f"{save_dir}/{save_filename}"
        # save binary file
        with open(scan_file, "wb") as buffer:
            shutil.copyfileobj(attach.file, buffer)
            result=scan_file.replace('./','/')
            await form.db.query(
                query="update dogovor set attach=%s where docpack_id=%s",
                values=[save_filename,docpack_id],
                errors=form.errors
            )
            print('u_manager_id: ',dogovor['u__manager_id'])
            if dogovor['u__manager_id']:
                to={dogovor['u__manager_id']: True}
                scan_file=scan_file.replace('./','/')
                print('send scan message to: ',to)
                link=f'''<a href="{form.s.config['system_url']}edit_form/user/{dogovor['u__id']}">{dogovor['firm']}</a>'''
                link_scan=f'''<a href="{form.s.config['system_url']}{scan_file.replace('./','')}">скан</a>'''

                await send_mes_tg_and_email(
                    to.keys(),
                    f"Новый скан договора для {dogovor['firm']}",
                    f"Наименование компании: {link}<br>"+\
                    f"Менеджер: {form.manager['name']} только что загрузил новый {link_scan} для договора №{dogovor['number']}"
                )
        
    return {'success': form.success(), 'errors': form.errors, 'attach': result}

async def remove_scan(request, config, field_name, form_id, docpack_id):
    form=await read_config(
        request=request,
        action='remove_scan',
        config=config,
        script='docpack',
        field_name=field_name,
        id=form_id
    )
    dogovor = await form.db.query(
        query="select * from dogovor where docpack_id=%s",
        values=[docpack_id],
        onerow=1
    )
    if dogovor:

        if dogovor['attach']:
            registered=str(dogovor['registered'])
            # remove file
            save_dir=f"./files/dogovor-scan/{'/'.join(registered.split('-'))}"
            scan_file=f"{save_dir}/{dogovor['attach']}"
            #print('scan_file:',scan_file)
            if os.path.exists(scan_file):
                os.remove(scan_file)
            
            await form.db.query(
                query="update dogovor set attach='' where docpack_id=%s",
                values=[docpack_id],
                errors=form.errors
            )

    return {'success': form.success(), 'errors': form.errors}
