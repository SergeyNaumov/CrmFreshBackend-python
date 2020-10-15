from lib.engine import s
#from lib.core import exists_arg

from .get_search_tables import get_search_tables
from .get_search_where import get_search_where
from .default_config_attr import default_config_attr



class Form():
  def info(self):
    print('title:',self.title)
  
  def __init__(self,arg): # Значения по умолчанию
    self.title=''

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
    self.page='1'
    self.perpage='20'
    self.javascript={
      'admin_table':''
    }
    self.priority_sort=None
    self.filters_groups=[]
    self.search_plugin=''
    self.search_on_load=0
    self.card_format='vue'
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