def get_fields():
    return [ 
    {
      'name':'date',
      'description':'Дата закупки',
      'type':'text',
      'read_only':1,
      'default_off':1,
      'filter_on':1,
      'filter_code':filter_code_date,
    },
    {
      'name':'manufacturer_id',
      'description':'Производитель',
      'type':'select_from_table',
      'table':'manufacturer',
      'autocomplete':1,
      'tablename':'man',
      'header_field':'header',
      'value_field':'id',
      'before_code':before_code_manufacturer_id,
      'filter_on':1
    }, 
    {
      'name':'action_id',
      'description':'Акция',
      'type':'select_from_table',
      'table':'action',
      'autocomplete':1,
      'tablename':'a',
      'header_field':'header',
      'value_field':'id',
      'filter_code':filter_code_action_id,
      'default_off':1,
      'before_code':before_code_action,
      'filter_on':1
    },
    {
      'description':'Товары',
      'name':'goods',
      'type':'code',
      'code':goods_code
    }

]



def filter_code_action_id(form,field,row):
  #print('row:',row)
  
  return f''' <a href="/edit-form/action/{row['a__id']}" target="_blank">{row['a__header']}</a>'''
  

def filter_code_date(form,field,row):
  return f''' { row["wt__date"] } <a href="/edit-form/purchase/{row['wt__id']}" target="_blank">подробнее</a> '''
  
def goods_code(form,field):
  s=form.self()
  if(form.id):
    good_list=s.db.query(query='''
      SELECT
        wt.header, wt.cnt, wt.summ, wt.code,
        a.ur_address apteka

      from 
        purchase_good wt
        LEFT JOIN apteka a ON a.id=wt.apteka_id
      WHERE purchase_id=%s

      ''',
      values=[form.id]
    )
    result=''
    if len(good_list):
      result='''
        <style>
          table.goodlist{
            border-collapse: collapse;
            width: 100%;
          }
          table.goodlist td {border: 1px solid gray; padding: 2px; }
          table.goodlist td.c {text-align: center;}
          table.goodlist tr.h td {text-align: left; font-weight: bold;}
          
        </style>
        <div style="margin-top: 20px"><b>Товары:</b></div>
        <table class="goodlist">
          <tr class="h">
            <td>Наименование</td>
            <td>Аптека</td>
            <td>Штрих-код</td>
            <td>Кол-во</td>
            <td>Сумма</td>
            
          </tr>
      '''


      for g in good_list:
        
        result+=f"""
          <tr >
            <td>{g['header']}</td>
            <td>{g['apteka']}</td>
            <td class="c">{g['code']}</td>
            <td class="c">{g['cnt']}</td>
            <td class="c">{g['summ']}</td>

          </tr>
        """
      result+='</table>'

    field['after_html']=result

def before_code_action(form,field):
  if form.script == 'edit_form':
    field['type']='code'
    action_name=form.ov["action"]
    if action_name:
      field['after_html']=f'<p><b>Акция:</b> <a href="/edit-form/action/{ field["value"] }" target="_blank">{action_name}</a></p>'
    return ''


def before_code_manufacturer_id(form,field):
  if form.script == 'edit_form':
    field['type']='code'
    manufacturer=form.ov["manufacturer"]
    if manufacturer:
      field['after_html']=f'<p><b>Производитель:</b> <a href="/edit-form/manufacturer/{ field["value"] }" target="_blank">{manufacturer}</a></p>'
    return ''

  

