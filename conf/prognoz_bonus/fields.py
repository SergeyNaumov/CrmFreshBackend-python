



def get_fields():

  return [ 
    {
      'description':'Информация о прогнозном бонусе',
      'name':'info',
      'type':'code',
      'code':prognoz_bonus
    },
    {
      'description':'Диаграммы',
      'type':'accordion',
      'name':'charts',
      'before_code':charts_before_code,
    }


  ]
def prognoz_bonus(form,field):
  #if form.manager['type']!=1: return
  total_left_to_complete_label='Осталось выполнить в рублях'
  if form.ov['action_plan']['plan']==2:
    total_left_to_complete_label='Осталось выполнить в штуках'

  ov=form.ov
  field['after_html']=form.template(
    f'./conf/{form.work_table}/templates/prognoz_bonus.html',
    ov=ov,
    action_plan=ov['action_plan'],
    action=ov['action'],
    managers=ov['managers'],
    period=ov['period'],
    total_left_to_complete_label=total_left_to_complete_label

  )
  
def charts_before_code(form,field):
    #if form.manager['type']!=1: return
    ov=form.ov
    if ov['action_plan']['plan']==3:
      return ''
    data=[
        {
            'header':'Посмотреть Диаграммы',
            'content':[
                {
                    'type':'chart',
                    'subtype':'circle',
                    'description':'диаграмма выполнения',
                    'labels':[f"""процент выполнения ({ov['percent_complete']})%""",f"""осталось выполнить ({ov['left_to_complete_percent']})%"""],
                    'values':[ov['percent_complete'],ov['left_to_complete_percent']],
                    'width':320,
                    'height':200,
                },
                {
                    'type':'chart',
                    'subtype':'circle',
                    'description':'дистрибьютеры',
                    'labels':[f"""разрешённые дистрибьютеры ({ov['price']})""",f"""остальные дистрибьютеры ({ov['other_distrib_sum']})"""],
                    'values':[ov['price'],ov['other_distrib_sum']],
                    'width':320,
                    'height':200,
                    #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                },
            ]
        }
      ]

    field['data']=data