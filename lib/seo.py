from transliterate import translit
import re
def url_by_header(form,v):
  url=translit(v.get('header'), language_code='ru',reversed=True)
  url=re.sub(
    r"\s+", "-", url
  )
  url=re.sub(
    r"[^0-9a-zA-Z_\-]", "", url
  )
  
  url=f"/sale/{url}"
  orig_url=url

  need_check=False
  query=f"select id,url from {form.work_table} WHERE url=%s"
  if form.id:
    query += f" AND {form.work_table_id}<>{form.id}"

  exists=form.db.query(
    query=query,
    values=[url],
    onerow=1
  )
  if exists:
    need_check=1

  loop_idx=1

  while need_check:
    url=f"{orig_url}-{loop_idx}"

    exists=form.db.query(
      query=query,
      values=[url],
      onerow=1
    )
    if exists:
      loop_idx+=1
    else:
      need_check=0
      break
    
    if loop_idx>100:
      break

  url_dict={'value':url,"error":''}
  return ['url',url_dict]
