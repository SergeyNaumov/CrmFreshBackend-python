from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    
    def __init__(form,arg):

        super().__init__(arg) 
        
        form.title='Сводные данные'
        form.not_edit=1
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.not_create=1
        form.QUERY_SEARCH_TABLES=[
            {'t':'bill','alias':'b'},


        ]
        
        #form.GROUP_BY='wt.id'
        
        form.filters_groups=[]
        form.fields=get_fields()

    

        form.events=events
        form.sort='ur_lico' # поле, по которому сортируем изначально
        form.sort_desc=False


        

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