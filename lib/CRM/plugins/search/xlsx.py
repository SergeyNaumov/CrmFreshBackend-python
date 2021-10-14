
from lib.engine import s
import re
import pandas as pd
from UliPlot.XLSX import auto_adjust_xlsx_column_width


config={
    'name':'search_xls',
    'icon':'fa-file-excel',
    'title':'сохранить в xls'
}


def before_search(form):
    if form.script=='find_objects' and 'plugin' in form.R and form.R['plugin']=='search_xls':
        
        form.not_perpage=1
def after_search(form):
    if form.script=='find_objects' and 'plugin' in form.R and form.R['plugin']=='search_xls':
        filename=form.config+'_'+form.manager['login']+'.xlsx'
        full_path='files/tmp/'+filename
        

        pandas_dataframe={}
        pandas_values={}
        numbers=[]
        
        pandas_values['_number']=[]
        pandas_dataframe['№']=pandas_values['_number']

        for h in form.SEARCH_RESULT['headers']:
            pandas_values[h['n']]=[]
            pandas_dataframe[h['h']]=pandas_values[h['n']]

        j=1
        for tr in form.SEARCH_RESULT['output']:
            
            pandas_dataframe['№'].append(j)
            j+=1

            id=tr['key']
            i=0
            cols=[]
            for d in tr['data']:
                # удаляем тэги html

                data=str(d['value'])
                data=re.sub(r'\<[^>]*\>', '', data)
                cols.append(data)

                pandas_values[d['name']].append(data)

        
        df = pd.DataFrame(pandas_dataframe)
        print(pandas_dataframe,"\n\n")
        # 
        writer = pd.ExcelWriter(full_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        auto_adjust_xlsx_column_width(df, writer, sheet_name="Sheet1", margin=1)
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
        #output.seek(0)

        form.plugin_output={
            'success':1,
            'ready':1,
            'format':'html',
            'search_result':form.SEARCH_RESULT,
            'pandas_dataframe':pandas_dataframe,
            #'pandas_values':pandas_values
            'result':f'''
                 <h2>XLS-файл готов!</h2>
                 <a href="/{full_path}">нажмите, чтобы скачать</a>
            '''
        }
        #print('config:',form.work_table)


def go(form):
    if form.script=='admin_table':
        form.search_plugin.append(config)

    elif form.script=='find_objects' and 'plugin' in form.R and form.R['plugin']=='search_xls':
        if not len(form.events['after_search']):
            form.events['after_search'].append(after_search)
        if form.events['before_search']:
            form.events['before_search'].append(before_search)
    #else:
    #    print('not_active after_search!')
        #form.pre({'R':form.R})