import re
from lib.core import exists_arg
def move(form,R):
      to=exists_arg('to',R) or ''
    
      if not form.id:
        form.errors.append('Параметр id не указан, обратитесь к разработчику')

      elif form.read_only or not form.tree_use:
        form.errors.append('Запрещено перемещать элементы в дереве! операция не выполнена')

      elif not to.isnumeric():
        form.errors.append('Параметр to не указан, обратитесь к разработчику')

      elif to == id:
        form.errors.append('Нельзя перенести в себя')

      else:
          from_path, to_path='',''
          if to:
            to_item=form.db.query(
              query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
              values=[to],
              onerow=1
            )
            if to_item:
              to_path=exists_arg('path',to_item) or ''
            else:
              form.errors.append('в базе отсутствует элемент-приёмник. Возможно, состояние базы было изменено')

          from_item=form.db.query(
            query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
            values=[form.id],
            onerow=1
          )

          if from_item:
            from_path=exists_arg('path',from_item) or ''
          else:
            form.errors.append('в базе отсутствует элемент-источник. Возможно, состояние базы было изменено')

          if not len(form.errors):
            if to: to_path+='/'+to
            else: to='null'

            form.db.query(
                query=f'UPDATE {form.work_table} SET parent_id=%s, path=%s WHERE {form.work_table_id}=%s',
                values=[to,to_path,id]
            );

            childs=form.db.query(
              query=f'SELECT {form.work_table_id} id, path from {form.work_table} WHERE path=%s OR path like %s',
              values=[from_path+'/'+form.id, from_path+'/'+id+'/%']
            )

            for c in childs:
                path=exists_arg('path',c) or ''
                reg1=re.compile('^'+from_path+'$')
                reg2=re.compile('^'+from_path+'/')
                path = re.sub(reg1,to_path,path)
                path = re.sub(reg2,to_path+'/',path)

                form.db.query(
                    query=f'UPDATE {form.work_table} SET path=%s WHERE {form.work_table_id}=%s',
                    values=[path,c['id']]
                )

          return {
            'success':(1,0)[len(form.errors)],
            'errors':form.errors
          }
