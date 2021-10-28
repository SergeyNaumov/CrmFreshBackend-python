from lib.CRM.form import Form
#from .fields import get_fields
from .events import events


class Config(Form):
    
    def __init__(form,arg):

        super().__init__(arg) 
        
        form.title='Список конференций'
        form.not_edit=1
        form.explain=0
        #form.read_only=1
        #form.make_delete=0
        #form.not_create=1
        form.events=events
        form.headers=[
            {'h':'Название конференции', 'n':'header'},
            {'h':'Дата и время начала','n':'start'},
            #{'h':'Ссылка на конференци','n':'link'},
            #{'h':'Идентификатор конференции','n':'conf_id'},
            #{'h':'Код доступа','n':'access_code'},
            #{'h':'Комментарий','n':'comment'},

        ]
        form.data=[]
        form.sort='ur_lico' # поле, по которому сортируем изначально
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