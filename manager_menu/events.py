async def events_permission1(form):
    #print('form: ',form)

    if form.manager['login']=='admin':
        form.read_only=False

    if form.id:
        form.ov = await form.db.query(query=f"SELECT * FROM {form.work_table} WHERE id={form.id}", onerow=1)
        if form.ov and form.ov['path']:
            ids = form.ov['path'][1:].split('/')
            parent_data = await form.db.query(
                query=f"SELECT header FROM {form.work_table} WHERE id IN ({','.join(ids)}) order by length(regexp_replace(path,'[^/]',''))",
                massive=1
            )
            form.title = f"Меню системы / {' / '.join(parent_data)}"

def events_permission2(form):
    print('perm2')

def events_before_code(form):
    print('is_before_code')

async def before_delete(form):
    print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
    events_permission1
  ],
  'before_delete':before_delete,
  #'before_code':events_before_code
}