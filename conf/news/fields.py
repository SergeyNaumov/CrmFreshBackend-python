from lib.send_mes import send_mes
from lib.core import cur_date

def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Наименование',      
      'type':'text',
      'filter_on':1,
      'regexp_rules':[
        '/.{1}/','название обязательно',
      ],
    },
    {
      'description':'Вкл',
      'name':'enabled',
      'filter_on':1,
      'type':'switch',
      'before_code':enabled_before_code
    },
    {
      'description':'Отправить в рассылку',
      'name':'to_subscribe',
      'type':'switch'
    },
    {
      'description':'Дата',
      'type':'date',
      'name':'registered',
      'before_code':registered_before_code
    },
    {
      'description':'Анонс',
      'type':'textarea',
      'filter_on':1,
      'name':'anons',
      'regexp_rules':[
        '/.{1}/','Обязательно заполните краткое описание',
      ],
    },
    {
      'description':'Текст новости',
      'type':'wysiwyg',
      'name':'body',
      'regexp_rules':[
        '/.{1}/','Напишите текст новости',
      ],
    },

    {
      # before_code=>sub{
      #         my $e=shift;                    
              
      # },
      'description':'Список юридических лиц для получения рассылки',
      'type':'multiconnect',
      'tree_table':'ur_lico',
      'name':'includes',
      'relation_table':'ur_lico',
      'relation_save_table':'news_include_ur_lico',
      'relation_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'news_id',
      'relation_save_table_id_relation':'ur_lico_id',
      #'make_add':1,
      'fast_search':1,
      'cols':4,
      'view_only_selected':0,
      #'tab':'tags'
    },
]

def enabled_before_code(form,field):
  if form.action == 'new':
    field['value']=1

def count_sec_before_code(form,field):
  if form.action == 'new':
    field['value']='0'

def registered_before_code(form,field):
    if form.action == 'new':
      field['value']=cur_date()