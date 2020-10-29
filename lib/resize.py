from PIL import Image, ImageOps
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


def crop(img,crop_type,width,height):
  min_x,min_y=0,0
  max_x,max_y=img.size[0],img.size[1]

  if crop_type == 'middle':

    min_x = (img.size[0] - width) / 2
    min_y = (img.size[1] - height) / 2
    max_x=min_x+width
    max_y=min_y+height

    box = (min_x, min_y, max_x, max_y)
    print('size:',img.size, 'width:',width,'height:',height, 'crop_box:',box)
  return img.crop(box)

def resize_one(**arg):
  composite_file=''
  grayscale=''
  quality=100
  crop_type='middle'
  optimize=1
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
  
  
  #print(f'width: {width}, height: {height}')
  size=(width,height)
  print('size:',size)
  img = Image.open(fr)
  ox, oy = img.size
  k=1
  if not height:
    if width > ox:
      img.save(to)
      return

    k = oy / ox
    height = int(width * k)
    

  elif not width:
    k = ox / oy
    width = int(height * k)
  
  else:
    ny= int( (oy / ox) * width)
    nx= int( (ox / oy) * height)
  #print('nx: ',nx,'ny:',ny)
  if width == height:
    if ox != oy:
      min_len=min(ox,oy)
      img=crop(img,crop_type,min_len,min_len)
    
    img=img.resize((width,height),  Image.ANTIALIAS)
    
  elif nx >= width: # горизонтально ориентированная
    img=img.resize( (nx,height), Image.ANTIALIAS)
    if nx >width:
      crop(img,crop_type,width,height)
      
      #nnx = int( (nx - width) / 2 )


  else: # вертикально ориентированная
    if ny < height:
      ny = height
    img=img.resize( (width,ny), Image.ANTIALIAS ) 

    if ny > height:
      crop(img,crop_type,width,height)

  if composite_file:
    composite_gravity=exists_arg('composite_gravity',arg)
    
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

    print('img_size:', wm_position_x, wm_position_y)
    
    
    img.paste(composite_image, (wm_position_x, wm_position_y) ,composite_image)


    #print('водяные знаки не реализованы')

  #print('optimize:',optimize)
  if grayscale:
    img = ImageOps.grayscale(img)
  #print('save:',to,'size: ',img.size)
  img.save(to,quality=quality,optimize=optimize)

