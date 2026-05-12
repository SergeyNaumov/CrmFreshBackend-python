import os
from lib.core import exists_arg, get_name_and_ext
async def delete_file(form,field,child_field,one_to_m_id):
  form.errors=[]
  query=f"""
        SELECT
            {child_field['name']}
        FROM
            {field['table']}
        WHERE
            {field['foreign_key']}={form.id} and {field['table_id']}={one_to_m_id}
  """
  oldfile=await form.db.query(
    query=f"""
        SELECT
            {child_field['name']}
        FROM
            {field['table']}
        WHERE
            {field['foreign_key']}=%s and {field['table_id']}=%s
    """,
    values=[form.id,one_to_m_id],
    onevalue=1,
    errors=form.errors
  )
  #print('oldfile:',oldfile)
  if oldfile:
    oldfile_arr=oldfile.split(";")
    if len(oldfile_arr) ==2:
        oldfile=oldfile_arr[0]
    fullname=child_field['filedir']+'/'+oldfile
    filename_without_ext,ext=get_name_and_ext(oldfile)
    #print('filename_without_ext:',filename_without_ext,'ext:',ext)
    #print('child_field:',child_field)
    if exists_arg('resize',child_field):
        for r in child_field['resize']:
            
            file=r['file']
            file=file.replace('<%filename_without_ext%>',filename_without_ext)
            file=file.replace('<%ext%>',ext)
            if os.path.exists(child_field['filedir']+'/'+file):
                os.remove(child_field['filedir']+'/'+file)

    if os.path.exists(fullname):
        os.remove(fullname)

    await form.db.query(
        query=f"""
            UPDATE
                {field['table']}
            SET
                {child_field['name']}=''
            WHERE
                {field['foreign_key']}=%s and {field['table_id']}=%s
        """,
        values=[form.id,one_to_m_id]

    )

    return {'success':form.success(),'errors':form.errors}