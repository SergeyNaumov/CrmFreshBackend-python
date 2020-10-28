from PIL import Image
import re
from lib.core import exists_arg, get_name_and_ext
from lib.save_base64_file import save_base64_file

def resize_all(**arg):
  field=arg['field']
  value=arg['value']
  v_arr=re.search(r'')
  crops=[]


  filename_without_ext,ext=get_name_and_ext(value)

  if not exists_arg('crops',field):
    field['crops']=0
  
  if not exists_arg('resize',field):
    field['resize']=[]

  if exists_arg('crops',arg) and len(arg['crops']):
    crops=arg['crops']

  if field['crops'] and len(crops):
      for r in field['resize']:
          if not exists_arg('grayscale',arg):
            arg['grayscale']=''
          
          if not exists_arg('composite_file',arg):
            arg['composite_file']=''
          
          if not exists_arg('quality',arg):
            arg['quality']=''

          if not exists_arg('size',r):
            continue

          width,height=r['size'].split("x")

          for c in crops:
              filename=r['file']
              filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
              filename=filename.replace('<%ext%>',ext)

              # save_base64_file(
              #   src=c['data'],
              #   field=field,
              #   filename=filename
              # )

              resize_one(
                fr=field['filedir']+'/'+filename,
                to=field['filedir']+'/'+filename,
                width=width,
                height=height,
                grayscale=arg['grayscale'],
                composite_file=arg['composite_file'],
                quality=arg['quality']
              )



def resize_one(**arg):
  composite_file=''
  grayscale=''
  quality=''
  crop_type='middle'

  width=arg['width']
  height=arg['height']
  fr=arg['fr']
  to=arg['to']

  if exists_arg('crop_type',arg):
    crop_type=arg['crop_type']

  
  

  size=(width,height)
  img = Image.open(fr)
  #w, h = img.size
  print('img.size:',img.size)
  img_ratio = img.size[0] / float(img.size[1])
  ratio = size[0] / float(size[1])

  if ratio > img_ratio:
        img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
                Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
  elif ratio < img_ratio:
        img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
                Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
  else :
        img = img.resize((size[0], size[1]),
                Image.ANTIALIAS)
        # If the scale is the same, we do not need to crop
  
  img.save(to)