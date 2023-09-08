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
  'docpack_foreign_key':'user_id',
  'dogovor_number_rule':dogovor_number_rule,
  'bill_number_rule':bill_number_rule

}]