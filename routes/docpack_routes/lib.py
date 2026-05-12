def need_manager_fld(form):
    perm = form.manager['permissions']
    return form.manager['login']=='admin' or ( ('admin_paids' in perm) and perm['admin_paids'] )

