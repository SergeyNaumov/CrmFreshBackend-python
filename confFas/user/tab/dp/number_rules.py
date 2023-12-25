def dogovor_number_rule(form,field, ur_lico_id):

    prefix=form.db.query(
        query="select prefix from ur_lico where id=%s",
        values=[ur_lico_id],
        onevalue=1
    )

    query="""
        SELECT
            if(max(d.number_today),max(d.number_today)+1,1) number_today, DATE_FORMAT(now(), %s) dat
        from
            docpack dp
            JOIN dogovor d ON d.docpack_id=dp.id
        WHERE
            dp.ur_lico_id=%s and d.registered=curdate()
    """

    item=form.db.query(
        query=query,
        values=['%d%m%y',ur_lico_id],
        onerow=1,

    )


    number_today=item['number_today']
    dat=item['dat']
    if prefix:
        dogovor_number=f"{prefix}-{number_today}/{dat}"
    else:
        dogovor_number=f"{number_today}/{dat}"


    return dogovor_number,number_today;

def bill_number_rule(form,field,ur_lico_id):

    #my $company_role=($form->{old_values}->{company_role}==2)?'З':'П';
    prefix=form.db.query(
        query="select prefix from ur_lico where id=%s",
        values=[ur_lico_id],
        onevalue=1
    )

    item=form.db.query(
      query='''
        SELECT
            if(max(b.number_today),max(b.number_today)+1,1) number_today,
            DATE_FORMAT(now(), %s) dat_bill
        from
            docpack dp
            JOIN bill b ON b.docpack_id=dp.id
        WHERE
            dp.ur_lico_id=%s and b.registered=curdate()
      ''',
      values=['%d%m%y',ur_lico_id],
      onerow=1,
    )
    number_today=item['number_today']
    dat_bill=item['dat_bill']

    if prefix:
        bill_number=f"{prefix}-{number_today}/{dat_bill}"
    else:
        bill_number=f"{number_today}/{dat_bill}"

    return number_today, bill_number

def act_number_rule(form,field,registered, ur_lico_id):
    prefix=form.db.query(
        query="select prefix from ur_lico where id=%s",
        values=[ur_lico_id],
        onevalue=1
    )

    item=form.db.query(
      query='''
        SELECT
            if(max(a.number_today),max(a.number_today)+1,1) number_today,
            DATE_FORMAT(now(), %s) dat
        from
            act a
            join bill b ON b.id=a.bill_id
            join docpack dp ON dp.id=b.docpack_id
        WHERE
            a.registered=%s
      ''',
      values=['%d%m%y',registered],
      onerow=1,
    )
    if item:
        number_today=item['number_today']
    else:
        number_today=1

    if prefix:
        number=f"{prefix}-{number_today}/{ item['dat'] }"
    else:
        number=f"{number_today}/{ item['dat'] }"

    return number_today, f"{prefix}-{number_today}/{ item['dat'] }"