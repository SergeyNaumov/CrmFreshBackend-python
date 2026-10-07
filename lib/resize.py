from PIL import Image, ImageOps
#import re, 
import os
from lib.core import exists_arg, get_name_and_ext
#from lib.save_base64_file import save_base64_file


def out_ext_for(field, ext):
  """Расширение мини-файла: 'webp', если у поля to_webp, иначе как у base."""
  if exists_arg('to_webp', field):
    return 'webp'
  return ext


def _flatten_rgb(img):
  """RGBA/LA/P с прозрачностью -> RGB на белом фоне (для JPEG)."""
  if img.mode == 'RGBA':
    bg = Image.new('RGB', img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[-1])
    return bg
  if img.mode == 'LA':
    return img.convert('RGB')
  return img if img.mode == 'RGB' else img.convert('RGB')


def _save_image(img, to, quality=None, optimize=None):
  """Сохраняет по расширению to; quality применяется для JPEG/WEBP."""
  ext = os.path.splitext(to)[1].lower()
  fmt = {'.webp': 'WEBP', '.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG'}.get(ext)
  kwargs = {}
  if fmt == 'JPEG':
    img = _flatten_rgb(img)
  if quality and fmt in ('JPEG', 'WEBP'):
    try:
      kwargs['quality'] = int(quality)
    except (TypeError, ValueError):
      pass
  if fmt == 'PNG':
    kwargs['optimize'] = True
  if optimize and fmt in ('JPEG', 'WEBP'):
    kwargs['optimize'] = True
  if fmt:
    img.save(to, fmt, **kwargs)
  else:
    img.save(to, **kwargs)


RASTER_EXTS = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tif', 'tiff'}


def is_raster_ext(ext):
  return (ext or '').lower().lstrip('.') in RASTER_EXTS


def convert_to_webp(src, dst, quality=None):
  """Пересохраняет файл в webp, сохраняя прозрачность (для to_webp base)."""
  if not os.path.isfile(src):
    return False
  try:
    img = Image.open(src)
  except Exception:
    # SVG и прочая векторная графика — не конвертируем.
    return False
  if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
    img = img.convert('RGBA')
  else:
    img = img.convert('RGB')
  _save_image(img, dst, quality=quality or 85)
  return True


def resize_field(field,value,debug=0):
  if not(exists_arg('resize',field)) or not(value):
    return False
  
  for r in field['resize']:
    
    if not exists_arg('grayscale',r): r['grayscale']=''
    
    if not exists_arg('composite_file',r): r['composite_file']=''
    
    if not exists_arg('quality',r): r['quality']=''

    if not exists_arg('size',r): continue

    width,height=r['size'].split("x")

    filename_without_ext,ext=get_name_and_ext(value)  
    out_ext=out_ext_for(field, ext)
    filename=r['file'].replace('<%filename_without_ext%>',filename_without_ext).replace('<%ext%>',out_ext)
    resize_one(
      fr=field['filedir']+'/'+value,
      to=field['filedir']+'/'+filename,
      width=width,
      height=height,
      grayscale=r['grayscale'],
      composite_file=r['composite_file'],
      quality=r['quality'],
      to_webp=exists_arg('to_webp',field),
      debug=debug
    )


def resize_all(**arg):
  field=arg['field']
  value=arg['value']
  #v_arr=re.search(r'')
  crops=[]


  filename_without_ext,ext=get_name_and_ext(value)

  if not exists_arg('crops',field):
    field['crops']=0
  
  if not exists_arg('resize',field):
    field['resize']=[]

  if exists_arg('crops',arg) and len(arg['crops']):
    crops=arg['crops']

  if len(crops): # field['crops'] and 
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
          out_ext=out_ext_for(field, ext)

          for c in crops:
              filename=r['file']
              filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
              filename=filename.replace('<%ext%>',out_ext)

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


def crop(img,crop_type,width,height):
  min_x,min_y=0,0
  max_x,max_y=img.size[0],img.size[1]

  if crop_type == 'middle':

    min_x = (img.size[0] - width) / 2
    min_y = (img.size[1] - height) / 2
    
    max_x=min_x+width
    max_y=min_y+height

    box = (min_x, min_y, max_x, max_y)
  else:
    box = (0, 0, img.size[0], img.size[1])
  return img.crop(box)

def resize_one(**arg):
  composite_file=''
  grayscale=''
  quality=None
  crop_type='middle'
  #crop_type=''
  optimize=0
  to_webp=False
  width=int(arg['width'])
  height=int(arg['height'])
  fr=arg['fr']
  to=arg['to']
  ny=0
  nx=0



  if exists_arg('grayscale',arg): grayscale=arg['grayscale']
  if exists_arg('crop_type',arg): crop_type=arg['crop_type']
  if exists_arg('quality',arg): quality=arg['quality']
  if exists_arg('composite_file',arg): composite_file=arg['composite_file']
  if 'optimize' in arg: optimize=arg['optimize']
  if exists_arg('to_webp',arg): to_webp=arg['to_webp']

  if to_webp:
    to=os.path.splitext(to)[0]+'.webp'
  
  
  #size=(width,height)
  if not(os.path.isfile(fr)):
    return 
  #print('fr:',fr)
  try:
    img = Image.open(fr)
  except Exception:
    # SVG/битый файл — ресайз не делаем.
    return
  if img.mode in ('RGBA','LA') or (img.mode=='P' and 'transparency' in img.info):
    img = img.convert('RGBA')
  else:
    img = img.convert('RGB')
  ox, oy = img.size
  k=nx=ny=0

  # Wx0 / 0xH — пропорциональный ресайз (height/width == 0 = авто).
  if width>0 or height>0:
      if height==0:
        if width > ox:
          _save_image(img, to, quality=quality, optimize=optimize)
          return

        k = oy / ox
        height = int(width * k)

      elif width==0:
        k = ox / oy
        width = int(height * k)

      elif width==height:
        nx=ny=width
        k=1

      else:
        ny= int( (oy / ox) * width)
        nx= int( (ox / oy) * height)

      if width == height:
        # Квадратная цель: центр-кроп до квадрата и приведение к точному
        # размеру (раньше квадратный исходник не масштабировался вовсе).
        if ox != oy:
          min_len=min(ox,oy)
          img=crop(img,crop_type,min_len,min_len)
        img=img.resize((width,height), resample=Image.BICUBIC)

      elif nx >= width: # горизонтально ориентированная

        #$image->Resize(geometry=>'geometry', width=>$nx, height=>$opt->{height});

        #img=img.resize( (nx,height), Image.ANTIALIAS)
        print('img:',img)
        #img=img.resize( (nx,height), Image.Resampling.LANCZOS)
        img=img.resize( (nx,height), resample=Image.BICUBIC)

        if ny>height:

          #$image->Crop(geometry=>$opt->{width}.'x'.$opt->{height}, gravity=>'center')
          img=crop(img,crop_type,width,height)




        if nx >width:
          img=crop(img,crop_type,width,height)

          #nnx = int( (nx - width) / 2 )


      else: # вертикально ориентированная

        if ny < height:
          ny = height
        #img=img.resize( (width,ny), Image.ANTIALIAS )

        #img=img.resize( (width,ny), Image.Resampling.LANCZOS )
        img=img.resize( (width,ny), resample=Image.BICUBIC )
        if ny > height or nx > width:
          img=crop(img,crop_type,width,height)

  if composite_file:
    composite_gravity=exists_arg('composite_gravity',arg)

    if not (width+height):
      # Можно указать размер 0x0, чтобы был watermark без ресайза
      # в этом случае, берём реальные размеры фото
      width,height=img.size[0],img.size[1]
    
    if not composite_gravity:
      composite_gravity='center'

    composite_image = Image.open(composite_file)
    wm_position_x=0
    wm_position_y=0

    if composite_gravity=='center':
      wm_position_x = int( ( width - composite_image.size[0] ) / 2  )
      wm_position_y = int( ( height - composite_image.size[1] ) / 2 )
    
    elif composite_gravity=='left,top':
      wm_position_x = 0
      wm_position_y = 0
    
    elif composite_gravity=='center,top':
      wm_position_x = int( ( width - composite_image.size[0] ) / 2  )
      wm_position_y = 0
    
    elif composite_gravity=='right,top':
      wm_position_x = width - composite_image.size[0]
      wm_position_y = 0
    
    elif composite_gravity=='left,center':
      wm_position_x = 0
      wm_position_y = int( ( height - composite_image.size[1] ) / 2 )
    
    elif composite_gravity=='right,center':
      wm_position_x = width - composite_image.size[0]
      wm_position_y = int( ( height - composite_image.size[1] ) / 2 )

    elif composite_gravity=='left,bottom':
      wm_position_x = 0
      wm_position_y = int(  height - composite_image.size[1] )

    elif composite_gravity=='center,bottom':
      wm_position_x = int( ( width - composite_image.size[0] ) / 2  )
      wm_position_y = int(  height - composite_image.size[1] )

    elif composite_gravity=='right,bottom':
      wm_position_x = width - composite_image.size[0]
      wm_position_y = int(  height - composite_image.size[1] ) 
    
    img.paste(composite_image, (wm_position_x, wm_position_y) ,composite_image)



  if grayscale:
    img = ImageOps.grayscale(img)
  
  if exists_arg('debug',arg):
    print("size: ",img.size,"\nsave:",to,"\n")
  
  _save_image(img, to, quality=quality, optimize=optimize)

