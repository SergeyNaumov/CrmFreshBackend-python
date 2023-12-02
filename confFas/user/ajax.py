def brand_id(form,v):
  brand_id=v['brand_id']
  after_html=''
  if brand_id:
    brand=form.db.query(
      query='SELECT * from brand where id=%s',
      values=[brand_id],
      onerow=1,

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

  if not(form.id) and (len(inn)==10 or len(inn)==12):
    # если нет id и inn 10 или 12 цифр, то проверяем, не создана ли та же картах в рамках этого бренда
    if group_id:=form.manager['group_id']:
      if brand_id:=form.db.query(query="select brand_id from manager_group where id=%s",values=[group_id],onevalue=1 ):
        # В рамках бренда запрещено создавать карту с тем же ИНН
        exists=form.db.query(
          query="select firm,id from user where inn=%s and brand_id=%s",
          values=[inn,brand_id],
          onerow=1
        )

        if exists:
          result=['inn',{
            'after_html':f'<a href="/edit_form/user/{exists["id"]}" target="_blank">{exists["firm"]}</a>',
            'error':f'в рамках данного бренда уже есть карты с инн {inn}'
          }]
          return result

  if inn.isnumeric() and (len(inn)==10 or len(inn)==12):
    result=['inn',{'after_html':f'<a href="/vue/admin_table/user?find_inn_doubles={inn}" target="_blank">найти дубли</a>'}]

  return result
ajax={
  'brand_id':brand_id,
  'city_id':city_id,
  'region_id':region_id,
  'inn':inn
}