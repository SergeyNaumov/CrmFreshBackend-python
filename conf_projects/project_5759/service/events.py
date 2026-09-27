
from lib.CRM.plugins.InExtUrl import InExtUrl






            
        
async def permissions(form):
    # После поля header добавляем поле in_ext_url:
    await InExtUrl(form,
     {
        'foreign_key':'project_id',
        'foreign_key_value':'5759',
        'dependence_field':'header',
        'in_url':'/service/<%id%>',
        'after_field':'header',
        'url_prefix':'/service/',
        'tab':'main',
     }
    )

    # Для edit_form


        
        
    if form.script=='edit_form' and form.id:
        # Декорируем форму
        form.cols=[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},
              {'description':'Блок "Тарифы"','name':'tarifs','hide':0},
              {'description':'Блок "Тарифы2"','name':'tarifs2','hide':0},
            ],
            [
              #{'description':'Юридические лица','name':'comp','hide':1},
              #{'description':'Аптеки','name':'apteka','hide':1},
              {'description':'Промо','name':'promo','hide':0},
              {'description':'Этапы выполнения работ','name':'stages','hide':0},
              {'description':'Вопросы и ответы','name':'faq','hide':0},
              {'description':'Вас заинтересует','name':'interest','hide':0},
              
            ]
        ]
        
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)


            


events={
    'permissions':permissions
}