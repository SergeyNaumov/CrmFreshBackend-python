def ur_lico_list(form,field):

    brand_list=form.db.query(
        query="SELECT brand_id from manager_email where manager_id=%s",
        values=[form.manager['id']],
        massive=1,
        str=1
    )
    if len(brand_list):
        return form.db.query(
            query=f"""
            SELECT
                ul.id v,ul.firm d
            FROM
                ur_lico ul
                JOIN ur_lico_brand lb ON lb.ur_lico_id=ul.id
            WHERE
                lb.brand_id in ({"".join(brand_list)})
            GROUP BY ul.id ORDER BY ul.firm
            """
        )
            #select id v,firm d from ur_lico order by firm')

    else:
        # если нет ни одного бренда -- список юрлиц не возвращаем
        return []


def get_bills(form,field, R):

  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if R.get('dogovor_id'):
      lst=form.db.query(
        query=f"""
          SELECT
              b.*
          from
              docpack dp
              JOIN bill b ON b.docpack_id=dp.id
          where
              dp.{docpack_foreign_key}=%s and b.docpack_id=%s
          order by b.id desc
        """,
        values=[form.id, R['dogovor_id']]
      )
      perm=form.manager['permissions']

      #pprint(form.manager['permissions'])
      # проставляем make_edit_summ:
      for b in lst:

        # Разрешаем редактировать сумму счёта если:
        if perm.get('admin_paids'):
            # Если это менеджер платежей
            b['make_edit_summ']=True

        elif not(b['paid']) and (b['manager_id']==form.manager['id'] or form.manager['CHILD_GROUPS_HASH'].get(b['group_id']) ) :
            # или менеджер платежа
            # или руководитель менелжера платежа
            b['make_edit_summ']=True

        else:
            b['make_edit_summ']=False

        b['act_list']=[
            {
                'id':1,
                'link':f'/edit_form/act/1',
                'header':'Акт №П008/191223 от 10.12.2023 (25000 руб)'
            }
        ]

        #from pprint import pprint
        #pprint(b)

  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return lst



def bill_number_rule(form,field):
    
    #my $company_role=($form->{old_values}->{company_role}==2)?'З':'П';
    prefix='С'
    
    item=form.db.query(
      query='''
        SELECT
            if(max(number_today),max(number_today)+1,1) number_today_bill,
            DATE_FORMAT(now(), %s) dat_bill
        from
            bill
        WHERE
            registered=curdate()
      ''',
      values='%d%m%y',
      onerow=1,
    )
    number_today=item['number_today_bill']
    dat_bill=item['dat_bill']
    return number_today, f"{prefix}-{number_today}/{dat_bill}"

def dogovor_number_rule(form,field):
    
    prefix='С'
    query="""
                SELECT
                if(max(number_today),max(number_today)+1,1) number_today, DATE_FORMAT(now(), %s) dat
            from
                dogovor
            WHERE
                registered=curdate()
    """
    item=form.db.query(query=query,values='%d%m%y',onerow=1)

    number_today=item['number_today']
    dat=item['dat']

    dogovor_number=f"{prefix}-{number_today}/{dat}"

    #print "number: $dogovor_number\n";
    return dogovor_number,number_today;

fields=[{
  'type':'docpack',
  'name':'docpack',
  'tab':'docpack',
  'not_filter':1,
  'docpack_foreign_key':'user_id',
  'dogovor_number_rule':dogovor_number_rule,
  'bill_number_rule':bill_number_rule,
  'ur_lico_list': ur_lico_list,
  'get_bills':get_bills

}]