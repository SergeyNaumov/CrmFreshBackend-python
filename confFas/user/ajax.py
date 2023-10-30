def brand_id(form,v):
  brand_id=v['brand_id']
  after_html=''
  if brand_id:
    brand=form.db.query(
      query='SELECT * from brand where id=%s',
      values=[brand_id],
      onerow=1,
      debug=1
    )
    if brand:
      after_html=f"<img src='/files/logo/{brand['logo']}'>"
    

  
  return ['brand_id',{'after_html':after_html}]

def region_id(form,v):
  region_id=v['region_id']
  result=[]
  
  region = form.db.query(
    query='select if(timeshift>0,concat("+",timeshift), timeshift) ts from region where region_id=%s',
    values=[region_id],
    debug=1,
    onerow=1
  )
  #print('region',region)
  if region:
    result.append('region_id')
    result.append({'after_html':f"Временная зона: {region['ts']}"})


  city_id=v['city_id']
  if city_id=='0': return result
  
  # если регион поменялся и город в этом регионе отсутствует, тогда город обнуляем
  city=form.db.query(
    query="select city_id from city where city_id=%s and region_id=%s",
    values=[city_id,region_id],onevalue=1
  )
  
  if not(city):

    result.append('city_id')
    result.append({'value':'0'})

  return result

def city_id(form,v):
  city_id=v['city_id']
  
  if city_id=='0': return [] # для исключения цикличных запросов

  region_id=0
  if city_id:
    region_id=form.db.query(
      query='select region_id from city where city_id=%s',
      values=[city_id],
      onevalue=1
    )
    if not(region_id): region_id=0

  if str(region_id) != v['region_id'] :
    return ['region_id',{'value':str(region_id) }]  
  else:
    return []
def inn(form,v):
  result=[]
  inn=v['inn']
  if inn.isnumeric() and (len(inn)==10 or len(inn)==12):
    result=['inn',{'after_html':f'<a href="/vue/admin_table/user?find_inn_doubles={inn}" target="_blank">найти дубли</a>'}]

  return result
ajax={
  'brand_id':brand_id,
  'city_id':city_id,
  'region_id':region_id,
  'inn':inn
}