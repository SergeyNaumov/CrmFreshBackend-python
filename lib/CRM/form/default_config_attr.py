from lib.core import create_fields_hash, exists_arg

from .set_default_attributes import set_default_attributes






def default_config_attr(form,arg): # Атрибуты формы по умолчанию

    # Атрибуты по умолчанию
    # общий engine из модуля не использовать (s.form=form) -- при параллельных
    # запросах это общее мутабельное состояние; контекст живёт в request.state
    def form_self():
      return form.request.state.engine
    # read_only
    if not hasattr(form,'read_only'): form.read_only=0

    # make_delete
    if not hasattr(form,'make_delete'):
      if form.read_only:
        form.make_delete=0
      else:
        form.make_delete=1

    # make_create
    if not hasattr(form,'make_create'):
      if form.read_only:
        form.make_create=0
      else:
        form.make_create=1

    
    
    create_fields_hash(form)


    if exists_arg('action',arg): form.action=arg['action']
    if not form.work_table: form.work_table=arg['config']
    






    set_default_attributes(form)
    form.self=form_self
    #print('read_conf: default_config_attr - доделать')
    
    # Доделать!
    #return form