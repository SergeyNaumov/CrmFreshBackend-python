from lib.send_mes import send_mes
from lib.core import cur_date

def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Наименование',      
      'type':'text',
      'filter_on':1,
      #'regexp_rules':[
      #  '/.{1}/','название обязательно',
      #],
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
      #'regexp_rules':[
      #  '/.{1}/','Обязательно заполните краткое описание',
      #],
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
      'description':'Список получателей / менеджеров АннА',
      'add_description':'если не выбран - отправляем всем',
      'type':'multiconnect',
      'tree_table':'manager',
      'name':'to_managers',
      'relation_table':'manager',
      'relation_save_table':'news_include_manager',
      'relation_table_header':'login',
      'relation_tree_order':'login',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'news_id',
      'relation_save_table_id_relation':'manager_id',
      #'make_add':1,
      #'fast_search':1,
      'cols':4,
      'query':'select id,name header from manager where type=1 order by name',
      'view_only_selected':0,
      #'tab':'tags'
    },
    {
      # before_code=>sub{
      #         my $e=shift;                    
              
      # },
      'description':'Список получателей / юридических лиц',
      'type':'multiconnect',
      'tree_table':'ur_lico',
      'name':'to_ul',
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
    {
      'description':'Список получателей / аптек',
      'add_description':'если не выбран - отправляем всем',
      'type':'multiconnect',
      'tree_table':'apteka',
      'name':'to_apt',
      'relation_table':'apteka',
      'relation_save_table':'news_include_apteka',
      'relation_table_header':'ur_address',
      'relation_tree_order':'ur_address',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'news_id',
      'relation_save_table_id_relation':'apteka_id',
      #'make_add':1,
      'fast_search':1,
      'query':'''
        SELECT
          wt.id, concat(ul.header,' / ',wt.ur_address) header
        FROM
          apteka wt
          JOIN ur_lico ul ON ul.id=wt.ur_lico_id
        ORDER BY ul.header, wt.ur_address
      ''',
      'cols':2,
      'view_only_selected':0,
      #'tab':'tags'
    },
    {
      'description':'Список получателей / фармацевтов',
      'add_description':'если не выбран - отправляем всем',
      'type':'multiconnect',
      'tree_table':'manager',
      'name':'to_pharm',
      'relation_table':'manager',
      'relation_save_table':'news_include_pharm',
      'relation_table_header':'login',
      'relation_tree_order':'login',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'news_id',
      'relation_save_table_id_relation':'manager_id',
      #'make_add':1,
      'fast_search':1,
      'query':'select id,name header from manager where type=4 order by name',
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