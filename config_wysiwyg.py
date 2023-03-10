
def get_options():

    return {
            #'selector':f'#{name}.mce',
            'content_css': 'https://newds.digitalstrateg.ru/templates/2023/digitalstrateg.ru/css/styles.css',
            'browser_spellcheck': True,
            'relative_urls' : False,

            'plugins': [
                "advlist autolink autosave link image lists charmap print preview hr anchor pagebreak ", # spellchecker
                "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
                "table  directionality emoticons template  paste  textpattern"
            ], 
            'menubar': False,
            'toolbar1': "formatselect fontselect fontsizeselect | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify ", # styleselect
            'toolbar2': "cut copy paste |  bullist numlist | outdent indent blockquote | undo redo | link unlink anchor image media code |  forecolor backcolor", # searchreplace insertdatetime preview |
            'toolbar3': "table | hr removeformat | subscript superscript | charmap emoticons | print fullscreen | visualchars visualblocks nonbreaking  pagebreak", #  ltr rtl | spellchecker |  restoredraft
            'language': 'ru',
            'advlist_number_styles': "lower-alpha",
            'height': 500,
            
            'paste_data_images': True,
            'image_advtab': True,
            'extended_valid_elements': '@[itemscope|itemprop|itemtype|itemref|content],img[*],time[*],div[*|class|data-resultsUrl|data-newWindow|data-queryParameterName],span[*],strong[*],td[*],tr[*],p[*],small[*],a[*|download],ul[*],li[*],em[*],script[type|src],article[*],header[*],meta[itemprop|itemtype|itemref|itemscope|content],iframe[src|style|width|height|scrolling|marginwidth|marginheight|frameborder|allowfullscreen],object[width|height|classid|codebase|embed|param],param[name|value],embed[param|src|type|width|height|flashvars|wmode],a[*]',
            'valid_children': '+a[div|p|img|span  ]'
    }

# модификация опций в случае необходимости (например для определённого поля или определённого проекта)
def options_modify(form,field_name):
    options=get_options()

    
    templates=form.db.query(
      query=f'''SELECT title, description, concat("/wysiwyg/load-template/",%s,"/",%s,"/",id) url FROM wysiwyg_template WHERE project_id=%s order by sort''',
      values=[form.config,field_name, form.s.project_id],
    )

    if len(templates):
      options['templates']=templates
      # добавляем в визивиг кнопку "шаблоны"
      options['toolbar2']+='| template '
    
    return options

# выводим шаблон
def out_template(form,field_name,template_id):
   return form.db.query(
       query="SELECT body FROM wysiwyg_template WHERE project_id=%s and id=%s",
       values=[form.s.project_id,template_id],
       onevalue=1
   )
   

config_wysiwyg={
    'get_options':get_options,
    'options_modify':options_modify,
    'out_template':out_template,
}