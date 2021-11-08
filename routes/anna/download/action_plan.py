from lib.engine import s
import pandas as pd
from fastapi.responses import StreamingResponse
from io import BytesIO
import urllib
from UliPlot.XLSX import auto_adjust_xlsx_column_width
from fastapi.responses import HTMLResponse
from jinja2 import Template

#import dbf
#from simpledbf import Dbf5





def action_plan(format,id):
    db=s.db
    #print('id:',id)
    plan=db.getrow(
        table='action_plan',
        where=f'id={id}'
    )
    #print('plan:',plan)

    good_list=db.query(query='''
        SELECT
          ag.action_plan_id plan_id, g.header,
          if(g.showcase='0','нет','да') showcase,
          g.price, g.code, g.percent
        from 
          action_plan_good ag
          JOIN good g ON ag.good_id=g.id
        WHERE ag.action_plan_id = %s''',
        values=[id],
        
    )
    if format=='xls':
        action_plan=[]
        good=[]
        code=[]
        numbers=[]
        j=1
        for g in good_list:
            numbers.append(j)
            action_plan.append(plan['header'])
            good.append(g['header'])
            code.append(g['code'])
            j+=1
            # h1 -- наименование плана акции
            # h2 -- наименование товара
            # code -- код товара

            #result.append({'h1':plan['header'],'h2':g['header'],'code':g['code']})
            #print('g:',g)


        # write_xls
        # Create a Pandas dataframe from the data.

        df = pd.DataFrame({
            '№': numbers,
            'План акции': action_plan,
            'Наименование товара': good,
            'Код товара': code
        })
        #print('df:',df)
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        output = BytesIO()
        #writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        # автоширина столбцоа
        auto_adjust_xlsx_column_width(df, writer, sheet_name="Sheet1", margin=1)

        # Close the Pandas Excel writer and output the Excel file.
        
        worksheet = writer.sheets['Sheet1']

        for i, col in enumerate(df.columns):
            # find length of column i
            column_len = df[col].astype(str).str.len().max()
            # Setting the length if the column header is larger
            # than the max column value length
            column_len = max(column_len, len(col)) + 2
            # set the column length
            worksheet.set_column(i, i, column_len)
        writer.save()

        output.seek(0)
        filename = urllib.parse.quote(plan['header']+".xlsx")
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        return StreamingResponse(output, headers=headers)
    if format=='dbf':
        
        daemon_id=db.save(
            table='dbf_daemon',
            data={
                'action_plan_id':id
            }
        )
        
        t=Template(
            open('./routes/anna/download/templates/dbf_loader.html').read()
        )
        
        html_content=t.render(
            daemon_id=daemon_id
        )
        
        return HTMLResponse(content=html_content, status_code=200)

    #return {'format':format,'id':id,'result':'ok'}

def dbf_ready(id):
    db=s.db
    r=db.getrow(
        table='dbf_daemon',
        id=id,
    )
    
    if r:
        r['success']=1
        return r
    else:
        r['success']=0
        r['error']='ошибка при формировании dbf'
    return r

#def dbf_download(id):
