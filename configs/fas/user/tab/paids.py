def paids_forere_code(form,field):
    if not(form.id):
        return ''

    # Счета
    _list=form.db.query(query="""
        SELECT
            b.id, b.docpack_id, b.number,  DATE_FORMAT(b.paid_date,%s) paid_date, b.paid_summ summ,
            m.name manager, t.header tarif, ul.firm ur_lico, b.paid_type
        FROM
            docpack dp
            join bill b ON b.docpack_id=dp.id
            LEFT join manager m ON b.manager_id=m.id
            LEFT JOIN tarif t ON t.id=dp.tarif_id
            LEFT JOIN ur_lico ul ON dp.ur_lico_id = ul.id
        WHERE
            dp.user_id=%s and b.paid=1""",

        values=['%d.%m.%Y', form.id],
        #errors=form.errors
    )
    #form.pre(_list)
    if len(_list):
        field['after_html']=form.template(
                #'confFas/win_our_clients/template/table.html',
                f"./{form.s.config['config_folder']}/{form.config}/templates/paids.html",
                list=_list,
        )
    else:
        field['after_html']='<p align="center">Оплаченных счетов нет</p>'

    # Акты:
    _list=form.db.query(
        query="""
            select
                a.id, a.ur_lico_id, a.number,
                DATE_FORMAT(a.dat,%s) dat, a.summa,
                 ul.firm ur_lico
            from
                act2 a
                join docpack dp ON dp.id=a.docpack_id
                join ur_lico ul ON ul.id=dp.ur_lico_id
            WHERE
                dp.user_id=%s
        """,
        values=['%d.%m.%Y',form.id]
    )
    if len(_list):
        field['after_html']+=form.template(
            f"./{form.s.config['config_folder']}/{form.config}/templates/acts.html",
            list=_list,
            backend_base=form.s.config.get('bakend_base','/backend')
        )
    #form.pre(_list)


fields=[{
  'type':'code',
  'name':'paids',
  'tab':'paids',
  'before_code':paids_forere_code
}]