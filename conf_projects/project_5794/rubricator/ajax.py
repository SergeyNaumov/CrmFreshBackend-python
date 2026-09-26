import re
from transliterate import translit

def exists_url(form,url):
  # если такой url занят, то возвращает ошибку
  where='where url=%s'
  if form.id:
    where+=f" AND id<>{form.id}"

  exists=form.db.query(
    query=f"select id,header,url from {form.work_table} {where}",
    values=[url],
    onerow=1
  )
  if exists:
    return f"url {url} уже занят"
  else:
    return ''

def ajax_url(form,v):
  url=v.get('url')
  if not(url):
    return [
      'url',{
        'error':'url не может быть пустым'
      }
    ]

  if err:=exists_url(form,url):
    return ['url',{'error':err}]

  return []

def ajax_gen_url(form,v):

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
    url=f"/catalog/{header}"


  if url:
    url_error=exists_url(form,url)
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
ajax={
  'url':ajax_url,
  'gen_url':ajax_gen_url
}