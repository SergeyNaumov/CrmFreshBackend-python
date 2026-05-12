import os, shutil
from lib.core import get_ext
from lib.all_configs import read_config
from fastapi import UploadFile
async def upload_scan_app(request, config, field_name, form_id, app_id, attach):

    # get extension from oroginal file name


    # get extension from oroginal file name


    form = await read_config(
        request=request,
        action='upload_scan_app',
        config=config,
        script='docpack',
        field_name=field_name,
        id=form_id
    )
    app = await form.db.query(
        query="select id,date(registered) registered from dogovor_app where id=%s",
        values=[app_id],
        onerow=1
    )
    ext=get_ext(attach.filename) ; result=''

    if not(app):
        form.append('не найдено приложение')
    elif not(app['registered']):
        form.append('не указана дата создания приложения')
    else:
        registered=str(app['registered'])
        save_dir=f"./files/dogovor_app-scan/{'/'.join(registered.split('-'))}"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_filename=f"{app_id}.{ext}"

        scan_file=f"{save_dir}/{save_filename}"
        # save binary file
        with open(scan_file, "wb") as buffer:
            shutil.copyfileobj(attach.file, buffer)
            result=scan_file.replace('./','/')
            await form.db.query(
                query="update dogovor_app set attach=%s where id=%s",
                values=[save_filename,app_id],
                debug=1,
                errors=form.errors
            )

    return {'success': form.success(), 'errors': form.errors, 'attach': result,'scan_file':scan_file}

async def remove_scan_app(request, config, field_name, form_id, app_id):
    form=await read_config(
        request=request,
        action='remove_scan_app',
        config=config,
        script='docpack',
        field_name=field_name,
        id=form_id
    )
    print('errors: ',form.errors)
    app = await form.db.query(
        query="select * from dogovor_app where id=%s",
        values=[app_id],
        onerow=1
    )
    if app:

        if app['attach']:
            registered=str(app['registered'])
            # remove file
            save_dir=f"./files/dogovor_app-scan/{'/'.join(registered.split('-'))}"
            scan_file=f"{save_dir}/{app['attach']}"

            if os.path.exists(scan_file):
                os.remove(scan_file)

            await form.db.query(
                query="update dogovor_app set attach='' where id=%s",
                values=[app_id],
                errors=form.errors
            )
    return {'success': form.success(), 'errors': form.errors}
