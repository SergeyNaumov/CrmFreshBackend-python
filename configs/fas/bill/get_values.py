async def get_values(form):
	return await form.db.query(
            query=f'''
                    SELECT
                        wt.*,u.firm, u.id user_id,
                        t.header tarif, t.id tarif_id,
                        ul.with_nds,
                        ul.without_nds_dat, dp.ur_lico_id, ul.firm ur_lico,
                        m.id m_id, me.email m_email, m.group_id m_group_id, mg.path m_group_path,mg.owner_id mg_owner_id,
                        d.number d_number,
                        af.number avance_fact_number
                    FROM
                        bill wt
                        left join manager m ON (m.id=wt.manager_id)
                        left join manager_email me on me.manager_id=m.id and me.main=1
                        left join manager_group mg ON (m.group_id=mg.id)
                        join docpack dp ON (wt.docpack_id=dp.id)
                        join dogovor d on d.docpack_id=dp.id
                        LEFT JOIN ur_lico ul ON (dp.ur_lico_id=ul.id)
                        LEFT JOIN tarif t ON (dp.tarif_id=t.id)
                        JOIN user u ON (u.id=dp.user_id)
                        LEFT JOIN avance_fact af ON (af.bill_id=wt.id)
                    WHERE wt.id=%s GROUP BY wt.id order by me.main
            ''',
            values=[form.id],onerow=1,

        )
