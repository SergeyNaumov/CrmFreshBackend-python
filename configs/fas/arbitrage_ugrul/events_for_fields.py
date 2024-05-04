def case_number_filter_code(form,field,row):
    case_number=row['wt__case_number']
    case_id=row['wt__case_id']
    return f'<a href="https://kad.arbitr.ru/Card/{case_id}" target="_blank">{case_number}</a>'

def phone_filter_code(form,field,row):
    return row['phones']

def email_filter_code(form,field,row):
    #form.pre(row)
    return row['emails']

events={
    'case_number':{
        'filter_code':case_number_filter_code
    },
    'phone':{
        'filter_code':phone_filter_code
    },
    'email':{
        'filter_code':email_filter_code
    },
    #'pl':{ # истец
    #    'filter_code':pl_filter_code
    #}
}