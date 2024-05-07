async def get_values(form):
	return await form.db.query(
            query=f'''
                SELECT
                    wt.*
                FROM
                    act2 wt

                WHERE wt.id=%s GROUP BY wt.id
            ''',
            errors=form.errors,
            values=[form.id],onerow=1,

        )
