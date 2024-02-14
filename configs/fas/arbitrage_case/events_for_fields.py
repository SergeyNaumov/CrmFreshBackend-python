def case_number_filter_code(form,field,row):
    case_number=row['wt__case_number']
    case_id=row['wt__case_id']
    return f'<a href="https://kad.arbitr.ru/Card/{case_id}" target="_blank">{case_number}</a>'


events={
    'case_number':{
        'filter_code':case_number_filter_code
    },


}