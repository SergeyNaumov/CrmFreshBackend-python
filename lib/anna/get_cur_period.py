from datetime import datetime
from lib.core import  cnt_days_period,cur_date
def get_cur_period(form,prev=0):
  datetime.now().year
  year = int(datetime.now().year)
  
  mon = int(datetime.now().month)
  #year=2021
  #mon=1

  if prev:
    if mon<4:
      mon=12
      year-=1
    else:
      mon-=3
  
  querter_begin_day=str(year)+'-01-01'
  querter_end_day=str(year)+'-03-31'

  querter=0
  
  
  if mon<4:
    querter=1
    
  elif mon<7:
    querter=2
    querter_begin_day=str(year)+'-04-01'
    querter_end_day=str(year)+'-06-30'
  elif mon<10:
    querter=3
    querter_begin_day=str(year)+'-07-01'
    querter_end_day=str(year)+'-09-30'
  else:
    querter=4
    querter_begin_day=str(year)+'-10-01'
    querter_end_day=str(year)+'-12-31'

  
  #print(querter_begin_day,cur_date())
  period=form.db.query(
    query='SELECT * from prognoz_bonus_period where year=%s and querter=%s',
    values=[year,querter],
    onerow=1
  )
  
  querter_begin_days=cnt_days_period(querter_begin_day,cur_date())+1
  querter_total_days=cnt_days_period(querter_begin_day,querter_end_day)
  if not period:
    period={'id':None,'querter':querter}
  
  period['querter_begin_days']=querter_begin_days
  period['querter_begin_day']=querter_begin_day
  period['querter_total_days']=querter_total_days
  period['year']=str(year)
  period['prev']=prev # предыдущий?
  return period
  

def get_period(form,id):
  datetime.now().year
  year = int(datetime.now().year)
  mon = int(datetime.now().month)-3

  


  querter=0

  period=form.db.query(
    query='SELECT *, if(date_end<curdate(),1,0) prev from prognoz_bonus_period where id=%s',
    values=[id],
    onerow=1,
    debug=1
  )
  querter_begin_day=period['date_begin']
  querter_end_day=period['date_end']

  querter_begin_days=cnt_days_period(querter_begin_day,cur_date())
  querter_total_days=cnt_days_period(period['date_begin'],period['date_end'])
  #querter_total_days=cnt_days_period(querter_begin_day,querter_end_day)
  #form.pre({'period':period,'querter_total_days':querter_total_days,'d1':period['date_begin'],'d2':str(period['date_end']), 'bd':querter_begin_day, 'ed':querter_end_day })
  if not period:
    period={'id':None,'querter':querter}
  
  period['querter_begin_days']=querter_begin_days
  period['querter_begin_day']=querter_begin_day
  period['querter_total_days']=querter_total_days
  #period['year']=str(year)
  period['prev']=False
  return period

  #return querter,querter_begin_days