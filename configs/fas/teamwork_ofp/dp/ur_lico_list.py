async def ur_lico_list(form,field):

    # brand_list=await form.db.query(
    #     query="SELECT brand_id from manager_email where manager_id=%s",
    #     values=[form.manager['id']],
    #     massive=1,
    #     #debug=1,
    #     str=1
    # )
    perm=form.manager['permissions']
    brand_list=await form.db.query(query="select brand_id from manager_brand where manager_id=%s",values=[form.manager['id']], str=1,massive=1)
    if form.manager['group_id']:
        if brand_id:= await form.db.query(query="select brand_id from manager_group where id=%s",values=[form.manager['group_id']],onevalue=1):
            brand_list.append(str(brand_id))
    
    

    #print('brand_list:',brand_list)
    perm=form.manager['permissions']
    if perm['admin_paids']:
        return await form.db.query(
            query=f"""
            SELECT
                ul.id v,ul.firm d
            FROM
                ur_lico ul
            GROUP BY ul.id ORDER BY ul.firm
            """,

        )
    
    if len(brand_list):
        return await form.db.query(
            query=f"""
            SELECT
                ul.id v,ul.firm d
            FROM
                ur_lico ul
                JOIN ur_lico_brand lb ON lb.ur_lico_id=ul.id
            WHERE
                lb.brand_id in ({",".join(brand_list)})
            GROUP BY ul.id ORDER BY ul.firm
            """,

        )
        #select id v,firm d from ur_lico order by firm')

    else:
        # если нет ни одного бренда -- список юрлиц не возвращаем
        return []