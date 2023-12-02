from lib.core import gen_pas

def events_permission1(form):
    if form.manager['login'] == 'admin':
      form.make_delete=1
      form.read_only=0
      form.not_create=0



def event_after_insert(form):
    form.db.query(
      query='UPDATE permissions set pname=%s where id=%s',
      values=[gen_pas(12),form.id],
    )



events={
  'permissions':[
      events_permission1,
      
  ],
  'after_insert':[
    event_after_insert
  ],
  
}
