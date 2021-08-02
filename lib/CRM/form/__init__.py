from lib.engine import s
#from lib.core import exists_arg
from lib.check_field import check_field
from .get_search_tables import get_search_tables
from .get_search_where import get_search_where
from .default_config_attr import default_config_attr
from .save_form import save_form
from .edit_form_process_fields import edit_form_process_fields as func_edit_form_process_fields
from .get_values import func_get_values
from .set_orig_types import func_set_orig_types
from .run_event import run_event as func_run_event
from .upload_file import upload_file as func_upload_file
from .delete_file import delete_file as func_delete_file
from .template import template as func_template


class Form():
  #def info(self):
  #  print('title:',self.title)
  
  def __init__(self,arg): # Значения по умолчанию
    
    self.title=''
    
    script=arg['script']
    #self.db=s.db
    self.run_js=''
    self.work_table=arg['config']
    self.work_table_id='id'
    self.id=''
    self.sort=0
    self.tree_use=0
    self.sort_field=''
    self.header_field='header'
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
    self.R={}
    self.before_filters_html=[]
    self.on_filters=[]
    self.default_find_filter=[]
    self.engine='mysql'
    self.javascript={
      'admin_table':'','find_objects':'','edit_form':''
    }
    

    self.explain=0
    self.card_format='vue'
    # для проектов
    self.work_table_foreign_key=''
    self.work_table_foreign_key_value=''
    
    if script=='admin_tree':
      self.tree_select_header_query=''
      self.default_find_filter=''
      self.max_level=0
    


    if script=='admin_table':
      self.search_plugin=[]
      self.filters_groups=[[]]
      self.search_on_load=0
      


    # Поля для edit_form
    if script=='edit_form':
      self.width=''
      self.cols=[]
      self.tabs=[]

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
      # Если что-то отдаёт плагин -- выводим его данные
      self.plugin_output=False
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
    
    return func_edit_form_process_fields(form)
    #print('edit_form_process_fields не реализована')
    #return {'success':'1'}

  def delete_file(form):
    print('form.delete_file не реализована')
    return {'success':'1'}

  def save(form,**arg): save_form(form,arg)

  def run_event(form,event_name,field=None):
    func_run_event(form,event_name,field)


  def success(form): # если нет ошибок -- 1
    return (1,0)[len(form.errors)>0]

  def set_default_attributes(form):
    func_set_default_attributes(form)
  
  def set_orig_types(form):
    func_set_orig_types(form)

  def get_values(form):
    func_get_values(form)

  def UploadFile(form):
    return func_upload_file(form)

  def check(form): # проверяем new_values
    for field in form.fields:
      if field['name'] in form.new_values:
        check_field(form,field,form.new_values[field['name']])
  
  # запускаем before_code для всех полей
  def run_all_before_code(form): 
    field_idx=0
    for field in form.fields:
      if 'before_code' in field:
        
        #form.run_event(form,'before_code for '+f['name'],f)
        try:
          new_field=field['before_code'](form=form,field=field)
          if new_field:
            # если в before_code подменили имя поля -- подменяем его и в fields_hash
            if new_field['name'] != field['name']:
              if field['name'] in form.fields_hash:
                del form.fields_hash[field['name']] 
              form.fields_hash[new_field['name']]=new_field
              form.fields[field_idx]=new_field
            

            field=new_field
          
        except AttributeError as e:
          form.errors.append(str(e))
        # except ValueError as e:
        #   form.errors.append(str(e))
        # finally:
        #   form.errors.append('Ошибка')

      field_idx+=1

  def DeleteFile(form): return func_delete_file(form)

  def pre(form,data): form.log.append(data)

  # для отладки
  def field_names(form):
    lst=[]
    for f in form.fields:
      lst.append(f['name'])
    return lst

  def get_field(form,field_name):
    for f in form.fields:
      if(f['name']==field_name): return f
    return None
  
  def remove_field(form,name):
    new_fields=[]
    for f in form.fields:
      if f['name']!=name:
        new_fields.append(f)
    
    form.fields=new_fields



  def template(form,filename,**values): return func_template(form,filename,**values)