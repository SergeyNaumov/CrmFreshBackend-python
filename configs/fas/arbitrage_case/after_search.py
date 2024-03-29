def after_search(form):
  result_plaintiff={} ; result_resp={}
  output = form.SEARCH_RESULT.get('output')

  ids=[]
  fields_planttiff={} ; fields_resp={}
  for o in output:
    case_id=str(o.get('key'))
    ids.append(case_id)
    for d in o['data']:
      if d['name']=='pl':
        fields_planttiff[case_id]=d

      elif d['name']=='resp':
        fields_resp[case_id]=d

  if not len(ids):
    return
  # собираем исцов
  plaintiff_list=form.db.query(
    query=f"""
      select
        pl.case_id, pl.name, e.inn, e.kpp, e.shortname, e.fullname,
        if(e.fio,e.fio,'') fio, if(e.regdate,e.regdate,'') regdate,
        if(e.address,e.address,'') address, if(e.okved,e.okved,'') okved, reg.name region,
        group_concat(ph.phone) phones, group_concat(em.email) emails
      from
        arbitrage_case_plaintiff pl
        LEFT join arbitrage_egrul e ON e.id=pl.egrul_id
        LEFT join arbitrage_region reg ON reg.id=e.region_id
        LEFT JOIN arbitrage_egrul_phone ph ON ph.egrul_id=e.id
        LEFT JOIN arbitrage_egrul_email em ON em.egrul_id=e.id
      where pl.case_id in ({','.join(ids)}) group by pl.id
    """,
    errors=form.errors
  )

  for p in plaintiff_list:
    case_id=str(p['case_id'])
    #form.pre(case_id)
    if not(case_id in result_plaintiff):
      result_plaintiff[case_id]=[]

    result_plaintiff[case_id].append(p)

  for case_id in fields_planttiff:
    fld=fields_planttiff[case_id]
    if _list:=result_plaintiff.get(case_id):
      fld['value']+=form.template('./conf/arbitrage_case/templates/plaintiff.html',list=_list)

  # собирает ответчиков
  respondent_list=form.db.query(
    query=f"""
      select
        pl.case_id, pl.name, e.inn, e.kpp, e.shortname, e.fullname,
        if(e.fio,e.fio,'') fio, if(e.regdate,e.regdate,'') regdate,
        if(e.address,e.address,'') address, if(e.okved,e.okved,'') okved, reg.name region,
        group_concat(ph.phone) phones, group_concat(em.email) emails
      from
        arbitrage_case_respondent pl
        LEFT join arbitrage_egrul e ON e.id=pl.egrul_id
        LEFT join arbitrage_region reg ON reg.id=e.region_id
        LEFT JOIN arbitrage_egrul_phone ph ON ph.egrul_id=e.id
        LEFT JOIN arbitrage_egrul_email em ON em.egrul_id=e.id
      where pl.case_id in ({','.join(ids)}) group by pl.id
    """,
    errors=form.errors
  )

  for p in respondent_list:
    case_id=str(p['case_id'])
    #form.pre(case_id)
    if not(case_id in result_resp):
      result_resp[case_id]=[]

    result_resp[case_id].append(p)

  for case_id in fields_resp:
    fld=fields_resp[case_id]
    if _list:=result_resp.get(case_id):
      fld['value']+=form.template('./conf/arbitrage_case/templates/plaintiff.html',list=_list)


  #form.pre(form.SEARCH_RESULT)
