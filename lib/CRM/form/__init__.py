from lib.engine import s
#from lib.core import exists_arg

from .get_search_tables import get_search_tables
from .get_search_where import get_search_where
from .default_config_attr import default_config_attr
from .save_form import save_form
from .edit_form_process_fields import edit_form_process_fields as func_edit_form_process_fields
from .get_values import func_get_values
from .set_orig_types import func_set_orig_types

class Form():
  #def info(self):
  #  print('title:',self.title)
  
  def __init__(self,arg): # Значения по умолчанию
    self.title=''
    
    script=arg['script']
    #self.db=s.db
    self.work_table=''
    self.work_table_id='id'
    self.id=''
    self.script=''
    self.action=''
    self.read_only=0
    self.not_create=0
    self.make_delete=1
    self.not_edit=0
    self.fields=[]
    self.search_links=[]
    self.log=[]
    self.errors=[]
    self.before_filters_html=[]
    self.on_filters=[]
    self.default_find_filter=[]
    
    self.javascript={
      'admin_table':''
    }
    self.explain=0
    self.card_format='vue'

    if script=='admin_table':
      self.filters_groups=[[]]
      self.search_on_load=0
      self.search_plugin=''

    # Поля для edit_form
    if script=='edit_form':
      self.width=''
      self.cols=[]
      self.work_table_foreign_key=''
      self.work_table_foreign_key_value=''
      self.edit_form_fields=[]

    if script=='find_objects':
      self.QUERY_SEARCH=''
      self.query_search={
        'on_filters_hash':{},
        'SELECT_FIELDS':[],
        'WHERE':[],'HAVING':[],'ORDER':[],'TABLES':[],'GROUP':[]
      }
      self.query_hash={}
      self.explain_query=''
      self.out_before_search=[]
      self.out_after_search=[]
      #self.search_result={
      #  'log':form.log,'config':form.config,'headers':[],'card_format':form.card_format
      #}

      #self.QUERY_SEARCH_TABLES=[{'table':self.work_table,'alias':'wt'}]
      
      
      self.priority_sort=[]
      self.not_order=False
      self.page='1'
      self.perpage='20'
      self.not_perpage=False

    self.events={
      'permissions':[],
      'before_search':[],
      'before_search_mysql':[],
      'after_search':[],
      'after_save':[],
      'before_save':[],
      'after_update':[],
      'before_update':[],
      'after_insert':[],
      'before_insert':[],
      'after_delete':[],
      'before_delete':[]
    }
    
    self.GROUP_BY=''
  def get_search_tables(form,query):
    get_search_tables(form,query)
  
  def get_search_where(form,query):
    get_search_where(form,query)
  
  def default_config_attr(form,arg):
    default_config_attr(form,arg)

  def edit_form_process_fields(form): # в perl-версии process_edit_form_fields
    return func_edit_form_process_fields
    #print('edit_form_process_fields не реализована')
    #return {'success':'1'}

  def delete_file(form):
    print('form.delete_file не реализована')
    return {'success':'1'}

  def save(form,**arg): save_form(form,arg)

  def run_event(form,**arg):
    print('run_event:',arg)

  def success(form): # если нет ошибок -- 1
    return (1,0)[len(form.errors)>0]

  def set_default_attributes(form):
    func_set_default_attributes(form)
  
  def set_orig_types(form):
    func_set_orig_types(form)

  def get_values(form):
    func_get_values(form)