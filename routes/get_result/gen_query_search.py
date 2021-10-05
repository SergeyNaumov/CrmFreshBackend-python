def gen_query_search(form):
  query=''
  query_count=''
  qs=form.query_search
 # if exists_arg('ORDER',qs):
 #   if not isinstance(qs,list): qs['ORDER']=[qs['ORDER']]
 # else:
 #   qs['ORDER']=[]

  perpage=int(form.perpage)
  page=int(form.page)

  if form.QUERY_SEARCH:
      if qs['WHERE'] and len(qs['WHERE']):
        where_list=' AND '.join(qs['WHERE'])
        form.QUERY_SEARCH=form.QUERY_SEARCH.replace('<%WHERE%>',where_list)
      else:
        form.QUERY_SEARCH=form.QUERY_SEARCH.replace('<%WHERE%>','')

      query=form.QUERY_SEARCH
      
      if not form.not_perpage:
        query=query+' LIMIT '+form.page+','+form.perpage
  else:
      SELECT_FIELDS = ', '.join(qs['SELECT_FIELDS'])
      TABLES = "\n".join(qs['TABLES'])
      
      WHERE=''
      if len(qs['WHERE']):
        WHERE = ' WHERE '+' AND '.join(qs['WHERE'])

      GROUP=''
      if len(qs['GROUP']):
        GROUP = ' GROUP BY '+', '.join(qs['GROUP'])
      
      HAVING=''
      if len(qs['HAVING']):
        HAVING = ' HAVING '+', '.join(qs['HAVING'])

      query = 'SELECT '+SELECT_FIELDS + ' FROM ' + TABLES + WHERE + GROUP + HAVING

      if qs['ORDER']:
        query = query + ' ORDER BY '+', '.join(qs['ORDER'])

      if not form.not_perpage:
        query = query + ' LIMIT '+str( (page-1)*perpage ) +', '+form.perpage

      if 'query_count' in qs:
        query_count=qs['query_count']
      
      else:
        if len(qs['GROUP']):
          query_count = f'SELECT count(*) cnt FROM (select wt.{form.work_table_id } FROM {TABLES} {WHERE} {GROUP} {HAVING}) x'
        else:
          query_count = ' SELECT count(*) cnt from ' + TABLES + WHERE + GROUP + HAVING
      
      #print('query:',query)
  return query, query_count