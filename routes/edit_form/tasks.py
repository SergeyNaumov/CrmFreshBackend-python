import re
from lib.all_configs import read_config
from fastapi import APIRouter, Request
from pydantic import BaseModel, validator

router = APIRouter()
"""
drop table task_alarm;
create table task_alarm(
    id int unsigned primary key auto_increment,
    config varchar(50) not null default '',
    card_id int unsigned not null default '0',
    registered timestamp default current_timestamp comment 'Время создания',
    header varchar(255) not null default '',
    type tinyint unsigned not null default '0',
    priority tinyint unsigned not null default '0',
    alarm_time timestamp,
    manager_id int unsigned,
    sended tinyint unsigned not null default '0' comment 'Отправлена',
    constraint foreign key(manager_id) references manager(id) on update cascade on delete cascade,
    key(card_id,config,manager_id)
) engine=innodb default charset=utf8;

create table task_priority(
id tinyint unsigned primary key auto_increment,
sort tinyint unsigned not null default '0',
header varchar(100) not null default '',
color varchar(30) not null default ''
) engine=innodb default charset=utf8;

create table task_type(
id tinyint unsigned primary key auto_increment,
sort tinyint unsigned not null default '0',
header varchar(100) not null default ''
) engine=innodb default charset=utf8;

"""

@router.get('/{config}/{card_id}')
async def load_tasks(config:str,card_id:int, request:Request):
    # Загрузка задач в карту пользователя
    form = await read_config(
        request=request,
        id=card_id,
        script='edit_form/tasks',
        action='load_list',
        config=config,
    )
    _list=[]
    if form.success():
        db=form.db
        _list = await db.query(
            query="""
                SELECT
                    id, if(alarm_time>=now(),'active','expired') tab, header,
                    DATE_FORMAT(alarm_time, %s) _time,
                    type, priority
                FROM
                    task_alarm
                WHERE
                    config=%s and card_id=%s and manager_id=%s
                ORDER BY alarm_time desc

            """,
            values=['%d.%m.%Y %H:%i', config, card_id, form.manager['id']]
        )


    return {
        'success':form.success(),
        'errors':form.errors,
        'list':_list,
        'type_list': await db.query(query="select id v, header d from task_type order by sort"),
        'priority_list':await db.query(query="select id v, header d, color c from task_priority order by sort"),
    }

class task_alarm(BaseModel):
    header: str
    type: int
    priority: str
    alarm_time: str
    @validator('alarm_time')
    def validate_alarm_time(cls, value):
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'
        if not re.match(pattern, value):
            raise ValueError("Invalid alarm time format. Expected format: YYYY-MM-DD HH:MM")
        return value

@router.post('/{config}/{_id}')
async def create_task(config: str, R: task_alarm, _id:int, request:Request):
    #url=f"/edit-form/{config}/{_id}"

    form = await read_config(
        request=request,
        id=_id,
        script='edit_form/tasks',
        action='create_task',
        config=config,

    )
    if form.success():
        await form.db.save(
            table='task_alarm',
            errors=form.errors,
            data={
                #'url':url,
                'config':config,
                'card_id':_id,
                'header':R.header,
                'type':R.type,
                'priority':R.priority,
                'alarm_time':R.alarm_time,
                'manager_id':form.manager['id'],
            }
        )

    return {
      'success':form.success(),
      'errors':form.errors,
    }


@router.delete('/{config}/{card_id}/{task_id}')
async def delete_task(config: str, card_id: int, task_id: int, request: Request):
    form = await read_config(
        request=request,
        id=card_id,
        script='edit_form/tasks',
        action='delete_task',
        config=config
    )

    await form.db.query(
        query="DELETE FROM task_alarm where id=%s and manager_id=%s",
        debug=1,
        values=[task_id,form.manager['id']]
    )
    return {
      'success':form.success(),
      'errors':form.errors,
    }
