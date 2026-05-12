from lib.core import get_child_field,exists_arg
from lib.get_1_to_m_data import get_1_to_m_data
def get_slide_data(form,field):
  R=form.R

  if form.success():
    get_1_to_m_data(form,field)

  return {
    'success':1,
    'errors':form.errors,
    #'values':field['values'],
    'field':field
  }

