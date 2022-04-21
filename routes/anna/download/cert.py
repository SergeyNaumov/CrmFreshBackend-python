from lib.engine import s
from lib.core import get_ext, date_to_rus
from fastapi.responses import HTMLResponse, FileResponse
#from fpdf import FPDF
import pdfkit
from jinja2 import Template
import tempfile
import base64
from pyvirtualdisplay import Display
import pdfkit


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
    conference=s.db.query(
        query="""
            SELECT
                c.*, date(c.start) date
            FROM
                conference c
                join conference_stat cs ON cs.conference_id=c.id and cs.manager_id=%s
            WHERE c.id=%s
        """,
        debug=1,
        values=[s.manager['id'],id],
        onerow=1
    )
    if not(conference) or not(conference['id']):
        return HTMLResponse(content='Сертификат не найден', status_code=404)
    date=date_to_rus(conference['date'])
    fio=s.manager['name']
    t=Template(
        open('./routes/anna/download/templates/cert.html').read()
    )
    html_content=t.render(
        id=id,
        fio=fio,
        compname=conference['comp_name'],
        subject=conference['header'],
        date=date,
        images={
            #'bg_left':img_to_b64('./files/cert_template/bg_left.jpg'),
            #'bg_right':img_to_b64('./files/cert_template/bg_right.jpg'),
            'bg':img_to_b64('./files/cert_template/bg.jpg'),
            'logo':img_to_b64('./files/cert_template/logo.png'),
            'print':img_to_b64('./files/cert_template/print.png'),
        },
    )
    with Display():
        pdf=pdfkit.from_string(html_content, False) # 'cert.pdf'
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as TPDF:
            TPDF.write(pdf)
            return FileResponse(
                TPDF.name,
                media_type="application/pdf",
                filename=f"Cертификат: {conference['header']}.pdf")

def html_cert(id):
    t=Template(
        open('./routes/anna/download/templates/cert.html').read()
    )
    logo_img=''
    fio=s.manager['name']
    
    conference=s.db.query(
        query="""
            SELECT
                c.*, date(min(cs.ts)) date
            FROM
                conference c
                join conference_stat cs ON cs.conference_id=c.id and cs.manager_id=%s
            WHERE c.id=%s
        """,
        debug=1,
        values=[s.manager['id'],id],
        onerow=1
    )
    if not(conference) or not(conference['id']):
        return HTMLResponse(content='Сертификат не найден', status_code=404)
    date=date_to_rus(conference['date'])
    html_content=t.render(
        id=id,
        fio=fio,
        compname=conference['comp_name'],
        subject=conference['header'],
        date=date,
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