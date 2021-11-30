from lib.CRM.form import Form
#from .fields import get_fields
from .events import events


class Config(Form):
    
    def __init__(form,arg):

        super().__init__(arg) 
        
        form.title='Сводные данные юр. лица'
        form.not_edit=1
        form.explain=0
        #form.read_only=1
        #form.make_delete=0
        #form.not_create=1
        form.events=events
        form.headers=[
            
            {'h':'период','n':'querter'},
            {'h':'маркетинговое мероприятие','n':'action'},
            {'h':'%выполнения','n':'percent_complete'},
            {'h':'осталось выполнить в %','n':'left_to_complete_percent'},
            {'h':'осталось выполнить в рублях / штуках','n':'left_to_complete_rub'},

        ]
        form.sort='action' # поле, по которому сортируем изначально
        form.sort_desc=False
        # form.data_query="""
        #      SELECT 
        #      from
        #         prognoz_bonus wt
        #         JOIN ur_lico ul ON wt.ur_lico_id=ul.id
        #     WHERE

        # """
        # form.data_values=[]

        

"""
create table test(
    id int primary key auto_increment,
    address varchar(255) not null default '',
    textarea text,
    wysiwyg text,
    checkbox tinyint unsigned not null default '0',
    switch  tinyint unsigned not null default '0',
    f_datetime datetime,
    status  tinyint unsigned not null default '0'
) engine=innodb default charset=utf8;
"""