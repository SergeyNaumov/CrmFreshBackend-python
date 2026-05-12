from jinja2 import Template

def template(form,filename,**values):
  html = open(filename).read()
  try:
    t=Template(html)
    return t.render(**values)
  except Exception as e:
    print(f"exception in template {filename} {e}")
    form.errors.append(e)
    return ''
  # try:
  #   return t.render(**values)
  # except TemplateSyntaxErrorr as e:
  #   form.errors.append(
  #       f"Jinja2 template syntax error during render: {e.filename}:{e.lineno} error: {e.message}"
  #   )
  # raise form.errors.append(f'ошиибка в form.template {filename}')
  # return ''
  