from lib.core import exists_arg
from lib.all_configs import read_config
#from lib.get_1_to_m_data import normalize_value_row


from .one_to_m_routine.insert_or_update import insert_or_update
from .one_to_m_routine.update_field import update_field
from .one_to_m_routine.slide_sort import slide_sort
from .one_to_m_routine.delete_record import delete_record
from .one_to_m_routine.upload_file import upload_file
def process_one_to_m(**arg):
  R={}
  if exists_arg('R',arg): R=arg['R']
  form=read_config(
    action=exists_arg('action',arg),
    config=exists_arg('config',arg),
    id=exists_arg('id',arg),
    R=exists_arg('R',arg) or {},
    script='1_to_m'
  )
  field_name=exists_arg('field_name',arg)
  if field_name:
    field=exists_arg(field_name,form.fields_hash)
    #print('field:',field)
  if not field:
    return {'success':0,errors:'имя поля не указано или указано не верно'}

  if form.action in ['insert','update']:
    return insert_or_update(form,field,arg)

  elif form.action == 'update_field':
    return update_field(form,field,arg)

  elif form.action == 'sort':
    return slide_sort(form,field)

  elif form.action == 'delete':
    return delete_record(form,field,arg)

  elif form.action == 'upload_file':
    
    return upload_file(form,field,arg)


