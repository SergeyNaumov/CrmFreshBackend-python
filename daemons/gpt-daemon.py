import sys
import os
from lib.gpt_daemon.get_const import get_const
from lib.gpt_daemon.yandex import process_yandexgpt

parent_dir = os.path.dirname(  os.path.dirname(__file__) )
sys.path.append(parent_dir)
from config import config
from db import db
from pprint import pprint
from time import sleep

shop_id = os.getenv("shop_id", 1)
BaсkendBase = config.get('BaсkendBase')


if not BaсkendBase:
    print('Отсутствует BaсkendBase')
    quit()
while True:
    print('.')
    const=get_const(db,shop_id)
    _list=db.query(
        query="SELECT * FROM crm_gptassist where status in (0)" # 1,3 -- убрать!
    )

    for item in _list:
        print('item: ',item)
        engine=item.get('engine_id')

        if engine==1:
            process_yandexgpt(BaсkendBase, db,const,item)
        # elif engine==1:
        #   process_gigachatgpt()

    # включить бесконечный цикл
    sleep(1)


"""
create table crm_gptassist(
    id int unsigned primary key auto_increment,
    taks_id varchar(50),
    engine_id tinyint unsigned not null default '1',
    temperature decimal(4,2),
    sys_text text ,
    ask text,
    registered timestamp not null default current_timestamp
) engine=innodb default charset=utf8;
"""
#print('shop_id:',shop_id)



#   pprint(l)

