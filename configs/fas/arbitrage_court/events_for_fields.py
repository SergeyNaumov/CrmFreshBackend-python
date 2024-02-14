def firm_filter_code(form,field,row):
    backend_base=form.s.config.get('bakend_base')
    #form.pre(form.s.config)
    if not(row['u__firm']):
        return '-'
    else:
        result=f"<a href='/edit_form/user/{row['u__id']}'>{row['u__firm']}</a>"

    return f"""
        <div style="font-size: 10pt;">
            {result}
            <br>Скачать
                <div style="margin-left: 10px;">
                    с печатями:
                        <a href='{backend_base}/fas/download-act/{row['wt__ur_lico_id']}/{row['wt__id']}/doc/1'>doc</a> |
                        <a href='{backend_base}/fas/download-act/{row['wt__ur_lico_id']}/{row['wt__id']}/pdf/1'>pdf</a>
                    <br>
                    без печатей:
                        <a href='{backend_base}/fas/download-act/{row['wt__ur_lico_id']}/{row['wt__id']}/doc/0'>doc</a> |
                        <a href='{backend_base}/fas/download-act/{row['wt__ur_lico_id']}/{row['wt__id']}/pdf/0'>pdf</a>
                </div
        </div>
    """
    #


events={
    'firm':{
        'filter_code':firm_filter_code
    }
}