from lib.resize import resize_one

# field={
#   'type':'file',
#   'name':'file',
#   'filedir':'./files/test',
#   'resize':[
#       {
#         'description':'Горизонтальное фото',
#         'file':'<%filename_without_ext%>_mini2.<%ext%>',
#         'size':'1004x490',
#         'quality':'90'
#       },
#       {
#         'description':'Вертикальное фото',
#         'file':'<%filename_without_ext%>_mini1.<%ext%>',
#         'size':'488x1008',
#         'quality':'95'
#       },
#       {
#         'description':'Квадратное фото',
#         'file':'<%filename_without_ext%>_mini3.<%ext%>',
#         'size':'500x500',
#         'quality':'95'
#       },
#       {
#         'description':'Фото для страницы статьи',
#         'file':'<%filename_without_ext%>_mini4.<%ext%>',
#         'size':'1165x672',
#         'quality':'90'
#       },
#   ]
# }


# resize_one(
#   fr='./files/test/FORESTER.jpg',
#   to='./files/test/FORESTER_resize.jpg',
#   width=500,
#   height=0
# )

resize_one(
  fr='./files/test/FORESTER.jpg',
  to='./files/test/FORESTER_resize.jpg',
  quality=70,
  width=0,
  optimize=0,
  composite_file='./files/composite/composite.png',
  composite_gravity='right,bottom',
  height=500
)
# resize_one(
#   fr='./files/test/FORESTER.jpg',
#   to='./files/test/FORESTER_resize2.jpg',
#   width=0,
#   height=500,
#   quality=70,
#   optimize=1
# )