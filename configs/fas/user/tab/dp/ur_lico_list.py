async def ur_lico_list(form,field):

    brand_list=await form.db.query(
        query="SELECT brand_id from manager_email where manager_id=%s",
        values=[form.manager['id']],
        massive=1,
        #debug=1,
        str=1
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
            #debug=1
        )
            #select id v,firm d from ur_lico order by firm')

    else:
        # если нет ни одного бренда -- список юрлиц не возвращаем
        return []