

def permissions(form):
    
    # Для edit_form
    if form.script=='edit_form' and form.id:
        # Декорируем форму
        form.cols=[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},
              {'description':'Тарифы','name':'tarifs','hide':0},
            ],
            [
              #{'description':'Юридические лица','name':'comp','hide':1},
              #{'description':'Аптеки','name':'apteka','hide':1},
              {'description':'Промо','name':'promo','hide':0}
              
            ]
        ]
        ov=form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)


            


events={
    'permissions':permissions
}