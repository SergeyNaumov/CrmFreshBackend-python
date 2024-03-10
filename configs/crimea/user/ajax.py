def login(form,v):
  result=[]
  print('v:',v)
  #result=['inn',{
  # 'after_html':f'<a href="/edit_form/user/{exists["id"]}" target="_blank">{exists["firm"]}</a>',
  # 'error':f'в рамках данного бренда уже есть карты с инн {inn}'
  #}]
  where=["login=%s"]
  if form.id:
    where.append(f"id<>{form.id}")
  exists=form.db.query(
    query="select * from user where "+' AND '.join(where),
    values=[v.get('login')],
    onerow=1,
    debug=1
  )
  if exists:
    result+=['login',
      {
        'error':f"логин <b>{v['login']}</b> уже существует, придумайте другой"
      }
    ]


  return result

ajax={
	'login':login,
	'snt_id':login
}