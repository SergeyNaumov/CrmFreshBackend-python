from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config


from lib.core import  get_ext, join_ids


router = APIRouter()

def get_ids(form):
    # Получение и проверка параметра ids
    ids=form.R.get('ids')
    if ids and isinstance(ids,list):

        if all(isinstance(v,int) for v in ids):
            if len(ids):

                return ids
            else:
                form.errors.append('Ни одной записи не было выбрано')
        else:
            # если в списке хотя бы один элемент не int
            form.errors.append('В списке есть недопустимые значения, операция не будет выполнена')
    else:
        form.errors.append('отсутствует параметр ids')
    return ids

async def set_all_value_field(form,ids):
    # Установить значение для множества записей
    R=form.R
    v=R.get('value')

    if form.read_only:
        form.errors.append('Вам запрещено изменять значения')

    name=R.get('name')
    if not(name):
        form.errors.append('отсутствует параметр name')
    else:
        field=form.get_field(R.get('name'))
        if field:
            query=f"UPDATE {form.work_table} SET {name}=%s WHERE {form.work_table_id} IN ({join_ids(ids)})"
            values=[v]
            await form.db.query(
                query=query,
                values=values,
            )
        else:
            form.errors.append(f"Поле {name} не найдено")

def delete_records(form,ids):
    if form.make_delete:
       query=f"DELETE FROM {form.work_table} WHERE {form.work_table_id} IN ({join_ids(ids)})"
       print(query)
    else:
        form.errors.append('Вам запрещено удалять записи')
async def change_price(form,ids):
    R=form.R
    value=R.get('value')

    name=R.get('name')
    if not(name):
        form.errors.append('отсутствует параметр name')
        return

    field=form.get_field(R.get('name'))
    if not(field):
        form.errors.append(f"Поле {name} не найдено")

    if not(value):
        form.errors.append('Параметр value не указан')

    if not(isinstance(value,dict)):
        form.errors.append('Параметр value не корректен {{value}}')
        return

    v=value.get('value')

    if not(v) or not(isinstance(v,str)) or not(v.isnumeric()):
        form.errors.append('Параметр value.value не корректен {{v}}')

    operation=value.get('operation')
    if not(operation in ('plus','minus')):
        form.errors.append('Параметр operatopn не корректен')

    t=value.get('type')

    if not(t in ('cnt','percent')):
        form.errors.append('Параметр type не корректен')

    if form.success():
        v=int(v)
        if operation=='minus':
            v=v*-1

        if t=='cnt':
            set_field=f"{name} + ({v})"
        else:
            set_field=f"{name} + {name}*{v}/100"

        query=f"UPDATE {form.work_table} SET {name} = {set_field} WHERE {form.work_table_id} IN ({join_ids(ids)})"
        await form.db.query(
            query=query,
        )






# Выполняем действие над несколькими записями
@router.post('/{config}')
async def process(config:str, R:dict):
    form=read_config(
        action='save_value',
        config=config,
        R=R,
        script='multiaction'
    )

    if not(hasattr(form, 'search_multi_action')):
        form.errors.append('отсутствует параметр конфига search_multi_action, обратитесь к разработчику')

    ids=get_ids(form)
    subaction=R.get('subaction')

    if form.success():
        if subaction == 'set_all_value_field':
            set_all_value_field(form,ids)

        elif subaction == 'delete':
            delete_records(form,ids)

        elif subaction == 'change_price':
            change_price(form,ids)
        else:
            form.errors.append(f"неизвестное действие: {subaction}")

    return {'success':form.success(),'errors':form.errors}
