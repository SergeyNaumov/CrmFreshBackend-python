import random, time
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from subprocess import PIPE, run

blank_dir='blank'

result_dir='./tmp/result'
tmp_dir='./tmp/docpack'

def gen_tmpl_prefix():
    now=str(int(time.time()))
    return str(int(time.time())) + \
    '_' +  ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV0123456780') for i in range(5))

def response_doc(template_file, output_filename, format, data, replace_images=[]): # images_list=None
    #print('template_file:',template_file)
    doc=DocxTemplate(template_file)

    if replace_images:
        for i in replace_images:
            doc.replace_pic(i[0],i[1])
   

    doc.render(data)

    file_prefix=gen_tmpl_prefix()

    docx_file=f'{tmp_dir}/{file_prefix}.docx'
    
    try:
        doc.save(docx_file)
    except Exception as e:
        return f'Внутренняя ошибка генерации документа: {e}'

    output_filename=f'{output_filename}.{format}'
    try:
        if format=='pdf':
            pdf_file=f'{tmp_dir}/{file_prefix}.pdf'
            
            convert_command=f"soffice --convert-to pdf {docx_file} --outdir {tmp_dir} --headless"
            
            run(convert_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

            #docx = aw.Document(docx_file)
            #saveOptions = aw.saving.PdfSaveOptions()
            #saveOptions.page_set = aw.saving.PageSet([0, 1])
            #doc.save(pdf_file, saveOptions)

            return FileResponse(path = pdf_file, filename=output_filename)
            #remove(pdf_file)
        else:
            print('response')
            return FileResponse(path = docx_file, filename=output_filename)
    except Exception:
        return "error!"
    
    