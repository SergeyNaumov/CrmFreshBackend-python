def goods_field(form,field):
  s=form.self()
  if(form.id):
    good_list=s.db.query(query='''
      SELECT
        g.header, g.showcase, g.price, g.code, g.percent
      from 
        action_plan_good ag
        JOIN good g ON ag.good_id=g.id
      WHERE ag.action_plan_id=%s

      ''',
      values=[form.id]
    )
    result=''
    if len(good_list):
      result='''
        <style>
          table.goodlist{
            border-collapse: collapse
          }
          table.goodlist td {border: 1px solid gray; padding: 2px; }
          table.goodlist td.c {text-align: center;}
          table.goodlist tr.h td {text-align: left; font-weight: bold;}
          
        </style>
        <p>Для товаров:</p>
        <table class="goodlist">
          <tr class="h">
            <td>Наименование</td>
            <td>Витрина</td>
            <td>Сип-цена</td>
            <td>Штрих код товара</td>
            <td>Начисления<br> по бонусу</td>
          </tr>
      '''


      for g in good_list:
        g['showcase']='да' if g['showcase'] else 'нет'
        result+=f"""
          <tr >
            <td>{g['header']}</td>
            <td class="c">{g['showcase']}</td>
            <td class="c">{g['price']}</td>
            <td class="c">{g['code']}</td>
            <td class="c">{g['percent']}%</td>
            
          </tr>
        """
      result+='</table>'

    field['after_html']=result


def action_filter_code(form,field,row):
  if row["a__id"]:
    return f'<a href="/edit-form/action_plan/{row["a__id"]}" target="_blank">{row["a__header"]}</a>'
  else:
    return ''


def get_fields():
    return [ 
    # {
    #   'name':'action_id',
    #   'description':'Акция',
    #   'type':'select_from_table',
    #   'header_field':'header',
    #   'value_field':'id',
    #   'table':'action',
    #   'read_only':1,
    #   'filter_on':1
    # },
    {
      'name':'header',
      'description':'Наименование акции',
      'type':'text',
      'filter_code':action_filter_code,
      'filter_on':1
    }, 
    # # Производителя убрал по просьбе Тани
    # {
    #   'name':'manufacturer_id',
    #   'description':'Производитель',
    #   'type':'select_from_table',
    #   'header_field':'header',
    #   'value_field':'id',
    #   'table':'manufacturer',
    #   'tablename':'man',
    #   'read_only':1,
    #   'filter_on':1
    # },
    {
      'name':'begin_date',
      'description':'Дата начала',
      'type':'date',
      'default_off':1,
      'filter_on':1
    },
    {
      'name':'end_date',
      'description':'Дата окончания',
      'type':'date',
      'default_off':1,
      'filter_on':1
    },
    # {
    #   'name':'plan',
    #   'description':'План',
    #   'type':'select_values',
    #   'values':[
    #     {'v':'1','d':'суммовой'},
    #     {'v':'2','d':'колличественный'},
    #     {'v':'3','d':'только процент за любые закупки'},
    #   ],
    #   'default_off':1,
    #   'filter_on':1
    # },
    # {
    #   'name':'value',
    #   'description':'сумма или количество',
    #   'type':'text',
    #   'filter_type':'range',
    #   'default_off':1,
    #   'filter_on':1
    # },
    # {
    #   'name':'reward_percent',
    #   'description':'% вознаграждения (для суммовой акции)',
    #   'type':'text',
    #   'filter_type':'range',
    #   'default_off':1,
    #   'filter_on':1
    # },
    # {
    #   'name':'allgood',
    #   'description':'Для всех товаров',
    #   'type':'checkbox',
    #   'default_off':1,
    #   'filter_on':1
    # },
    {
      'description':'Товары',
      'type':'code',
      'name':'goods',
      'code':goods_field,
      'after_html':'html'
    }

]
