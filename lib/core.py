import random
import datetime

def cur_year():
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=0)
  return dat.strftime("%Y")

def exists_arg(key,dict):
  if (key in dict) and dict[key]:
    return True
  return False

def gen_pas(length=8):
  letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  return ''.join(random.choice(letters) for i in range(length))
  
def cur_date(delta=0,format="%Y-%m-%d"):
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=delta)
  return dat.strftime(format)

def success(errors):
  if(len(errors)):
    return 0
  return 1

def is_errors(form):

  if isinstance(form,dict):
    return ( ('errors' in form) and len(form['errors']) )
  else:
    return (hasattr(form,'errors') and len(form.errors))



def create_fields_hash(form):
  form.fields_hash={}
  for f in form.fields:
    form.fields_hash[f['name']]=f
