def permissions(form):
    db=form.db
    form.fields=[]

    form.fields=db.query(
        query='''
            SELECT
                 description, header name,type
            FROM
                template_const
            WHERE
                template_id=%s
            ORDER BY sort
        ''',
        #debug=1,
        errors=form.errors,
        values=[form.s.template_id]

    )
    form.filedir=f"./files/project_{form.s.project_id}"
    form.filedir_http=f"/files/project_{form.s.project_id}"
    
    form.foreign_key='project_id'
    form.foreign_key_value=form.s.project_id

    #print('CONST_LIST:', form.fields)
    
    
events={
    'permissions':permissions
}