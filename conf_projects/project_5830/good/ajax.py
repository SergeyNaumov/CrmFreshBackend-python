import re
from transliterate import translit

async def exists_url(form,url):
  # если такой url занят, то возвращает ошибку
  project_id=form.request.state.project['project_id']
  where='where ieu.ext_url=%s'
  if form.id:
    where+=f" AND wt.id<>{form.id}"

  exists= await form.db.query(
    query=f"""
      select 
        wt.id,wt.header,url
      from
        {form.work_table} wt
        JOIN in_ext_url ieu ON ieu.project_id={project_id} and ieu.in_url=concat('/good/',wt.id)
      {where}
    """,
    values=[url],
    onerow=1,
    debug=1
  )
  print('exists: ',exists)
  if exists:
    return f"url {url} уже занят"
  else:
    return ''

async def ajax_gen_url(form,v):

  title=''
  old_url=v.get('url')
  url=''
  url_error=''
  if header:=v.get('header'):
    print('header:',header)
    if form.id and not(form.ov['promo_title']):
        title=header

    header=translit(v.get('header'),'ru',reversed=True)
    header=re.sub(r"[^a-zA-Z0-9]+",'-',header)
    header=re.sub(r"--+",'-',header)
    header=re.sub(r"-$",'',header)
    url=f"/good/{header}"


  if url:
    url_error=await exists_url(form,url)
  else:
    url_error='url не должен быть пустым'

  response=[]

  # if title:
  #   response+=[
  #     'promo_title',
  #     { 'value':title }
  #   ]

  if old_url!=url or url_error:
    response+=[
      'url',
      {
        'value':url.lower(),
        'error':url_error
      }
    ]

  return response

async def in_ext_url(form,v):

  title=''
  old_url=v.get('url')
  url=''
  url_error=''
  if header:=v.get('header'):
    #print('header:',header)
    if form.id and not(form.ov['promo_title']):
        title=header

    header=translit(v.get('header'),'ru',reversed=True)
    header=re.sub(r"[^a-zA-Z0-9]+",'-',header)
    header=re.sub(r"--+",'-',header)
    header=re.sub(r"-$",'',header)
    url=f"/good/{header}"

  url=url.lower()
  if url:
    url_error=await exists_url(form,url)
  else:
    url_error='url не должен быть пустым'

  response=[]

  if old_url!=url or url_error:
    response+=[
      'in_ext_url',
      {
        'value':url.lower(),
        'error':url_error,
      },
    ]
  if url_error:
      response+=['header',
        {
          'error':'скорректируйте url'
        }
      ]

  return response

async def ajax_url(form,v):
  url=v.get('url')
  if not(url):
    return [
      'url',{
        'error':'url не может быть пустым'
      }
    ]

  if err:=await exists_url(form,url):
    return ['url',{'error':err}]

  return []
  
ajax={
  'url':ajax_url,
  'gen_url':ajax_gen_url,
  'in_ext_url':in_ext_url
}