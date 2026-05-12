import random, time
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from subprocess import PIPE, run
import os

blank_dir='blank'

result_dir='./tmp/result'
tmp_dir='./tmp/docpack'

def gen_tmpl_prefix():
    now=str(int(time.time()))
    return str(int(time.time())) + \
    '_' +  ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV0123456780') for i in range(5))

def response_doc(template_file, output_filename, format, data, replace_images=[]):
    print('replace_images: ',replace_images)
    try:
        # 1. Проверка существования шаблона
        if not os.path.exists(template_file):
            return {'error': f'Шаблон документа не найден: {template_file}'}

        # 2. Загрузка шаблона
        try:
            doc = DocxTemplate(template_file)
        except Exception as e:
            return {'error': f'Ошибка загрузки шаблона: {str(e)}'}

        # 3. Замена изображений
        if replace_images:
            for i in replace_images:
                try:
                    doc.replace_pic(i[0], i[1])
                except Exception as e:
                    # Логируем, но продолжаем
                    print(f'Ошибка замены изображения {i[0]}: {e}')
                    #print('i: ',i)

        # 4. Рендер данных
        try:
            doc.render(data)
        except Exception as e:
            return {'error': f'Ошибка рендеринга документа: {str(e)}'}

        # 5. Сохранение DOCX
        file_prefix = gen_tmpl_prefix()
        docx_file = f'{tmp_dir}/{file_prefix}.docx'

        # Проверка/создание директории
        os.makedirs(tmp_dir, exist_ok=True)

        try:
            doc.save(docx_file)
        except Exception as e:
            return {'error': f'Ошибка сохранения DOCX: {str(e)}'}

        # 6. Конвертация в PDF если нужно
        output_filename_full = f'{output_filename}.{format}'

        if format == 'pdf':
            pdf_file = f'{tmp_dir}/{file_prefix}.pdf'

            # Проверяем, существует ли soffice
            convert_command = f"soffice --convert-to pdf {docx_file} --outdir {tmp_dir} --headless"
            print(f'convert_command={convert_command}')

            try:
                result = run(convert_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True, timeout=30)

                # Проверяем результат
                if result.returncode != 0:
                    return {
                        'error': f'Ошибка конвертации в PDF (код {result.returncode}):\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}'
                    }

                # Проверяем, создался ли файл
                if not os.path.exists(pdf_file):
                    return {
                        'error': f'PDF файл не создался после конвертации. Ожидался: {pdf_file}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}'
                    }

                # Проверяем, не пустой ли файл
                if os.path.getsize(pdf_file) == 0:
                    return {'error': f'PDF файл создался, но имеет нулевой размер: {pdf_file}'}

                return FileResponse(path=pdf_file, filename=output_filename_full)

            except Exception as e:
                return {'error': f'Исключение при конвертации в PDF: {str(e)}'}

        elif format == 'docx' or format=='doc':
            # Просто отдаем DOCX
            return FileResponse(path=docx_file, filename=output_filename_full)

        else:
            return {'error': f'Неподдерживаемый формат: {format}. Доступны: pdf, docx'}

    except Exception as e:
        return {'error': f'Общая ошибка генерации документа: {str(e)}'}
