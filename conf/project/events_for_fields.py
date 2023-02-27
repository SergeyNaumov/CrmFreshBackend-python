def header_code(form,field):
    if form.id:
        field['before_html']=f'Проект №{form.id}'

events={
    'header':{
        'before_code':header_code
    }
}