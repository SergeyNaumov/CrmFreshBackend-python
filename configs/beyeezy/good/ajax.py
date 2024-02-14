import re
from transliterate import translit

def exists_url(form,url):
  # если такой url занят, то возвращает ошибку
  where='where keyword=%s'
  if form.id:
    where+=f" AND id<>{form.id}"

  exists=form.db.query(
    query=f"select id,header,keyword from good {where}",
    values=[url],
    onerow=1
  )
  if exists:
    return f"url {url} уже занят"
  else:
    return ''

def url(form,v):
  url=v.get('keyword')
  if not(url):
    return [
      'keyword',{
        'error':'url не может быть пустым'
      }
    ]
  if err:=exists_url(form,url):
    return ['keyword',{'error':err}]
  return []

def gen_url(form,v):
  category_id=v.get('category_id')
  old_url=v.get('keyword')
  url=''
  url_error=''
  if category_id:
    category=form.db.query(
      query="select id, header, keyword from category where id=%s",
      values=[category_id],
      onerow=1
    )
    if category:
      header=translit(v.get('header'),'ru',reversed=True)
      header=re.sub(r"[^a-zA-Z-9]+",'-',header)
      header=re.sub(r"--+",'-',header)
      header=re.sub(r"-$",'',header)

      url=f"/{category['keyword']}/{header}/"


  if url:
    url_error=exists_url(form,url)
  else:
    url_error='url не должен быть пустым'

  if old_url!=url or url_error:
    return [
      'keyword',
      {
        'value':url,
        'error':url_error
      }
    ]
  else:
    return []

ajax={

  'url':url,
  'gen_url':gen_url
}