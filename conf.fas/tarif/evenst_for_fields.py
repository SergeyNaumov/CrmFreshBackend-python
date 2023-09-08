def header_filter_code(form,field,row):
    return f"<span style="color: red;">{row['wt__header']}</span>"

def blank_bill_id_before_code(form,field)
  return f'<br><a href="/files/blank_document/{form.ov['blank_attach']}" target="_blank">скачать бланк</a>'
  
events={
  'header':{
    'filter_code':header_filter_code
  },
  'blank_bill_id':{
    'before_code':blank_bill_id_before_code
  }
}