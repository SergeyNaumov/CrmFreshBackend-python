from lib.core import exists_arg, date_to_rus

async def components_actions(form):
    db=form.db ; R=form.R

    # загрузка статистики в блок "статистика" (выполняется при раскрытии блока)
    if form.id and exists_arg('cgi_params;action',R) == 'load_stat':
        inn=form.ov.get('inn')
        #print('inn:',inn)
        if inn:
            # уклонений
            rejection_list = await db.query(
                query="""
                    select
                        id, reg_number, org_name firm, ts registered
                    from
                        rejection where inn=%s order by ts desc
                """,
                values=[inn]
            )



            # расторжений
            contract_termination_list = await db.query(
                query="""
                    select
                        id, reestr_number reg_number, name_org firm, ts registered
                    from
                        contract_termination where inn=%s order by ts desc
                    """,
                values=[inn]
            )

            # Реестр РПН
            rnp_reestr_from_ftp_list = await db.query(
                query="""
                select
                    id, reestr_number reg_number, registered, client_name firm
                from
                    rnp_reestr_from_FTP where client_inn=%s
                ORDER BY registered desc
                """,
                values=[inn],
            )

            for c in rejection_list:
                c['registered']=date_to_rus(c['registered'])
                c['url']=f'/edit_form/rejection/{c["id"]}'

            for c in contract_termination_list:
                c['registered']=date_to_rus(c['registered'])
                c['url']=f'/edit_form/rejection/{c["id"]}'

            for c in rnp_reestr_from_ftp_list:
                c['registered']=date_to_rus(c['registered'])
                c['url']=f'/edit_form/rnp_reestr_from_FTP/{c["id"]}'


            form.response={
                'success':True,
                'rejection_list':rejection_list, # уклонений
                'contract_termination_list': contract_termination_list, # расторжений
                'rnp_reestr_from_ftp_list':rnp_reestr_from_ftp_list, # реестр РНП
            }
