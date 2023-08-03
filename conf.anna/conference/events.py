from lib.core import exists_arg, date_to_rus

def permissions(form):
    if exists_arg('superadmin',form.manager['permissions']):
        form.not_create=0
        form.read_only=0
        form.make_delete=True
        
    if form.script=='page' and form.id:

        d=form.db.query(
            query='select * from conference where id=%s',
            values=[form.id],
            onerow=1
        )
        d['start']=date_to_rus(d['start'])
        form.title=d['header']
        form.blocks=[
            {'type':'html','body':form.template('./conf/conference/templates/dialog.html',d=d)},
            {'type':'link','onclick':''}
        ]
        

    
def before_search(form):
    qs=form.query_search
    #print('QS:',qs['SELECT_FIELDS'])
    #form.pre(qs['SELECT'])

def events_before_code(form):
    pass

def before_delete(form):
    pass

events={
  'permissions': permissions,
  'before_delete':before_delete,
  'before_code':events_before_code,
  #'before_search':before_search
}