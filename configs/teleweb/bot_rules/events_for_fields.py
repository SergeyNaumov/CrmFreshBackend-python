def photo_before_code(form,field):
    field['filedir']=f"./files/project_{form.s.shop_id}/bot_rules"

def resize_keyboard_before_code(form,field):
    if form.ov and form.ov.get('keyboard_type')==2:
        field['hide']=False
    else:
        field['hide']=True

def one_time_keyboard_before_code(form,field):
    if form.ov and form.ov.get('keyboard_type')==2:
        field['hide']=False
    else:
        field['hide']=True

events={
    'photo':{
        'before_code':photo_before_code,
        #'after_save_code':photos_after_save_code
    },
    'resize_keyboard': {
        'before_code': resize_keyboard_before_code
    },
    'one_time_keyboard': {
        'before_code': one_time_keyboard_before_code
    }
}