from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config
#import datetime as dt
from lib.save_base64_file import save_base64_file
from lib.core import  get_ext
import os

router = APIRouter()
@router.post('/get')
async def get_list(R:dict): # 
    form=read_config(
        action='get',
        config=R['config'],
        #id=exists_arg('id',arg),
        R=R,
        script='const'
    )
    response={}
    
    if not len(form.errors):
        
        where=''
        
        if form.foreign_key:
            where=f'WHERE {form.foreign_key}={form.foreign_key_value}'
        values={}
        for v in form.db.query(
            query=f"select {form.name_field} name, {form.value_field} value from {form.work_table} {where}",
            errors=form.errors
        ):
            values[v['name']]=v['value']

        #print('values:',values)
        if not len(form.errors):
            pass
    
        result_list=[]
        for f in form.fields:
            value=''
            item={'header':f['description'],'name':f['name'],'type':f['type']}
            if f['name'] in values:
              value=values[f['name']]
            
            # Для чекбоксов 
            if f['type'] in ['checkbox','switch'] and value:
                value=int(value)

            if f['name'] in values: item['value']=value

            result_list.append(item)
        response['list']=result_list

    success=True
    if len(form.errors):
        success=False
    #print('MANAGER:',form.manager)
    response['filedir']=form.manager['filedir_http']
    response['success']=success
    response['errors']=form.errors
    return response

    # insert into const()

# Сохранение константы
@router.post('/save_value')
async def save_value(R:dict):
    form=read_config(
        action='save_value',
        config=R['config'],
        #id=exists_arg('id',arg),
        R=R,
        script='const'
    )
    const_fld=None

    if not('name' in R) or not('value' in R):
        form.errors.append('параметры name и value обязательны, обратитесь к разработчику')
    else:
        for f in form.fields:
            if f['name']==R['name']:
                const_fld=f
        if not(const_fld):
            form.errors.append('"не найдено поле с именем $R->{name}"')
    
    if not len(form.errors):

        query_for_old_record=f'select * from {form.work_table} WHERE name=%s'
        values_for_old_record=[R["name"]]

        if form.foreign_key:
            query_for_old_record+=f' AND {form.foreign_key}=%s'
            values_for_old_record.append(form.foreign_key_value)

        # Пытаемся получить уже существующую запись
        const_record=form.db.query(
            query=query_for_old_record,
            values=values_for_old_record,
            errors=form.errors,
            debug=1,
            onerow=1
        )

        if const_fld['type']=='file':
            if 'src' in R:
                
                ext=get_ext(R['value'])
                if ext:
            
                    filename=R['name']+'.'+ext
                    
                    if const_record: # файл ранее был загружен
                        #print('remove:',form.filedir+'/'+const_record['value'])
                        if os.path.isfile(form.filedir+'/'+const_record['value']):
                            os.remove(form.filedir+'/'+const_record['value'])

                    save_base64_file(
                        filedir=form.filedir,
                        filename=filename,
                        src=R['src'],
                        orig_filename=R['value']
                    )
                    # Для того, чтобы имя файла для константы записалось в базу:
                    const_fld['type']='text'
                    R['value']=filename
                    
                else:
                    form.errors.append('Не известно расширение файла, не загружаем')
            pass
        
        if const_fld['type'] in ['text','textarea','wysiwyg','checkbox','switch']: # Стандартный тип, просто сохраняем
            #print('const_fld ok:',const_fld)
            # Получаем старое значение в базе

            if const_record:
               # print('const_record exists:',const_record)
                
                form.db.query(
                    query=f"UPDATE {form.work_table} SET {form.value_field}=%s where {form.work_table_id}=%s",
                    values=[R['value'],const_record[form.work_table_id]]
                )
                

            else:
                #print('const_record NOT exists')
                data={
                    form.name_field:R['name'],form.value_field:R['value']
                }
                if form.foreign_key:
                    data[form.foreign_key]=form.foreign_key_value
                
                form.db.save(
                    table=form.work_table,
                    data=data,
                    debug=1,
                    errors=form.errors
                )
            
            form.run_event('after_save_const')


    success=( True if len(form.errors) else False)
    if not len(form.errors): success=False
    response={'success':True,'errors':form.errors,'value':R['value']}
    return response
