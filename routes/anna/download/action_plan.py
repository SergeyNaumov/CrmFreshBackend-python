from lib.engine import s
import pandas as pd
from fastapi.responses import StreamingResponse
from io import BytesIO
import urllib
from UliPlot.XLSX import auto_adjust_xlsx_column_width

#import dbf
#from simpledbf import Dbf5




def action_plan(format,id):
    db=s.db
    plan=db.getrow(
        table='action_plan',
        id=id
    )

    good_list=db.query(query='''
        SELECT
          ag.action_plan_id plan_id, g.header,
          if(g.showcase='0','нет','да') showcase,
          g.price, g.code, g.percent
        from 
          action_plan_good ag
          JOIN good g ON ag.good_id=g.id
        WHERE ag.action_plan_id = %s''',
        values=[id]
        
    )
    if format=='xls':
        action_plan=[]
        good=[]
        code=[]

        for g in good_list:
            action_plan.append(plan['header'])
            good.append(g['header'])
            code.append(g['code'])
            # h1 -- наименование плана акции
            # h2 -- наименование товара
            # code -- код товара

            #result.append({'h1':plan['header'],'h2':g['header'],'code':g['code']})
            #print('g:',g)


        # write_xls
        # Create a Pandas dataframe from the data.
        df = pd.DataFrame({
            'План акции': action_plan,
            'Наименование товара': good,
            'Код товара': code
        })

        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        output = BytesIO()
        #writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1')

        # автоширина столбцоа
        auto_adjust_xlsx_column_width(df, writer, sheet_name="Sheet1", margin=0)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        output.seek(0)
        filename = urllib.parse.quote(plan['header']+".xlsx")
        headers = {
            'Content-Disposition': f'''attachment; filename="{filename}"'''
        }
        return StreamingResponse(output, headers=headers)
    if format=='dbf':
        table = dbf.Table('temptable', 'name C(30); age N(3,0); birth D')
        return {'outdbf':1}
    #return {'format':format,'id':id,'result':'ok'}