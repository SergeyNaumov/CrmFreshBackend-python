from lib.engine import s
from lib.core import get_ext
from fastapi.responses import HTMLResponse
#from fpdf import FPDF
import pdfkit
from jinja2 import Template


import base64
def img_to_b64(path):
    ext=get_ext(path)
    type_img='jpeg'
    if ext=='png':
        type_img='png'

    my_string =''
    with open(path,"rb") as img_file:
        my_string=base64.b64encode(img_file.read()).decode('utf-8')
        
    
    return f'data:image/{type_img};base64,{my_string}'
# Формирование сертификата в pdf и его скачивание 
def download_cert(id):
    #pdf = FPDF()
    #pdf.add_page()
    #pdf.set_font("Arial", size=12)
    #pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
    
    #url=f'http://dev-crm.test/backend/anna/download/cert/{id}'
    #pdf=pdfkit.from_url(url, False)


    t=Template(
        open('./routes/anna/download/templates/cert.html').read()
    )
    html_content=t.render(
        id=id,
        fio='Овчинникова Оксана Владимировна',
        compname='BAYER',
        subject='Тема вебинара',
        images={
            #'bg_left':img_to_b64('./files/cert_template/bg_left.jpg'),
            #'bg_right':img_to_b64('./files/cert_template/bg_right.jpg'),
            'bg':img_to_b64('./files/cert_template/bg.jpg'),
            'logo':img_to_b64('./files/cert_template/logo.png'),
            'print':img_to_b64('./files/cert_template/print.png'),
        },
    )

    pdfkit.from_string(html_content, 'cert.pdf')
    return {'ok':1}
    

def html_cert(id):
    t=Template(
        open('./routes/anna/download/templates/cert.html').read()
    )
    logo_img=''
    html_content=t.render(
        id=id,
        fio='Овчинникова Оксана Владимировна',
        compname='BAYER',
        subject='Тема вебинара',
        images={
            'bg':img_to_b64('./files/cert_template/bg.jpg'),
            #'bg_left':img_to_b64('./files/cert_template/bg_left.jpg'),
            #'bg_right':img_to_b64('./files/cert_template/bg_right.jpg'),

            'logo':img_to_b64('./files/cert_template/logo.png'),
            'print':img_to_b64('./files/cert_template/print.png'),
        },
        path='/files/cert_template'
    )
    return HTMLResponse(content=html_content, status_code=200)
    #return {'htmlcert':True}