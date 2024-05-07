async def get_values(form):
	return await form.db.query(
            query=f'''
                SELECT
                    wt.*,
                    b.id bill_id,
                    b.number bill_number,
                    b.registered bill_registered,
                    dp.id docpack_id,
                    u.firm, u.id user_id,
                    d.registered dogovor_registered, d.number dogovor_number,
                    t.header tarif_header
                FROM
                    act wt
                    LEFT JOIN bill b ON b.id=wt.bill_id
                    LEFT JOIN docpack dp ON dp.id=b.docpack_id
                    LEFT JOIN tarif t ON t.id=dp.tarif_id
                    LEFT JOIN dogovor d ON d.docpack_id=dp.id
                    LEFT JOIN user u ON u.id=dp.user_id
                WHERE wt.id=%s GROUP BY wt.id
            ''',
            errors=form.errors,
            values=[form.id],onerow=1,

        )
