from fastapi import APIRouter, Header
from lib.engine import s

SECRET_KEY='7x4B_p9qYTnJ8GjRwK3ZlQfO0M1N6bVcSdU2XvCgEiI'

router = APIRouter()

# def convert_date_format(date_str):
#     # Регулярное выражение для проверки формата dd.mm.YYYY
#     date_pattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
    
#     # Проверка соответствия строки регулярному выражению
#     match = date_pattern.match(date_str)
    
#     if match:
#         # Извлечение групп (день, месяц, год)
#         day, month, year = match.groups()
#         # Преобразование в формат YYYY-MM-DD
#         converted_date_str = f"{year}-{month}-{day}"
#         return converted_date_str
#     else:
#         date_str

@router.post('/add-contract-termination')
async def add_contract_termination(R:dict, auth_key: str = Header(None)):
  # Парсер Мокрякова
  if auth_key != SECRET_KEY:
    return {'success':False,'message':'False auth_key!'}
  else: 
    reestr_number=R.get("Рег. номер")
    link=R.get('Ссылка с решением об отказе')
    inn=R.get("ИНН поставщика")
    name_org=R.get("Наименование поставщика",'')
    purchase_object=R.get("Наименование (тендера)")
    customer_inn=R.get("ИНН заказчика",'')
    customer_name=R.get("Наименование заказчика",'')
    registered_date=R.get("Дата отправки",'')
    #registered_date=R.get("Дата отправки",'')
    print_form_id=R.get("printFormId")
    
    if reestr_number and link and inn and print_form_id:
      exists= await s.db.query(
        query="select * from contract_termination where print_form_id=%s limit 1",
        values=[print_form_id],
        onerow=1
      )
      if exists:
        return {'success':False,'message':'Запись уже существует'}
      else:
        item={
          'reestr_number': reestr_number.replace('№ ',''),
          'link': link,
          'source':4,
          'inn': inn,
          'name_org':name_org,
          'registered_date':registered_date,
          'customer_inn':customer_inn,
          'customer_name':customer_name,
          'purchase_object':purchase_object,
          'print_form_id':print_form_id
        }
        await s.db.save(
          table="contract_termination",
          data=item
        )

        return {'success':True}
    else:
      return {'success':False,'message':'не достаточно данных'}

@router.post('/add-rejection')
async def add_rejection(R:dict, auth_key: str = Header(None)):
  """
Пример отправки (уклонения):
curl -X POST "https://fas.crm-dev.ru/backend/fas/api/add-rejection" \
     -H "Content-Type: application/json" \
     -H "Auth-Key: 7x4B_p9qYTnJ8GjRwK3ZlQfO0M1N6bVcSdU2XvCgEiI" \
     -d '{
  "reg_number":[регистрационный_номер],
  "start_price":[начальная минимальная цена контракта (НМЦК) - сумма],
  "contract_obesp":[Обеспечение исполнения контракта (сумма)],
  "bg_sum":[Сумма ГО (сумма)],
  "application_guarantee":[размер обеспечения заявки],
  "customer_inn":[ИНН заказчика],
  "customer_name":[Наименование заказчика],
  "inn":[ИНН поставщика],
  "org_name":[Наименование поставщика],
  "header": [Наименование контракта],
  "revenue_last_year":[Выручка в прошлом году],
  "profit_last_year":[Прибыль в прошлом году],
  "registered":[дата и время регистрации: YYYY-MM-DD hh:mm:ss],
  "reason1":[Причина отказа1],
  "reason2":[Причина отказа2],
  "inclusion_statistics":[уклонений в течение года]  
  "link":[ссылка],
  "print_form_id":[уникальный идентификатор уклонения],
}'
  """
  if auth_key != SECRET_KEY:
    return {'success':False,'message':'False auth_key!'}
  reg_number=R.get('reg_number')
  inn = R.get('inn')
  header=R.get('header')
  print_form_id=R.get('print_form_id')
  if reg_number and inn and header and print_form_id:
    exists= await s.db.query(
        query="select * from rejection where print_form_id=%s limit 1",
        values=[print_form_id],
        onerow=1
    )
    
    if exists:
      return {'success':False,'message':'Запись уже существует'}
    else:
        await s.db.save(
          table="contract_termination",
          data=item
        )
        return {'success':True}
  
  else:
    return {'success':False,'message':'не достаточно данных'}