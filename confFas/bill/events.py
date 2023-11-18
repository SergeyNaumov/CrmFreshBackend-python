from .get_values import get_values

def permissions(form):
    form.ov=None
    form.is_admin=True

    perm=form.manager['permissions']
    if perm['admin_paids']:
        form.is_admin=True
        form.read_only=False
        form.make_delete=True
    
    if form.id:
        form.ov=get_values(form)


def after_save(form):
    form.nv=get_values(form)

events={
  'permissions':[
      permissions,
      
  ],
  'after_save':after_save
  #'before_delete':before_delete,
  #'before_code':events_before_code
}