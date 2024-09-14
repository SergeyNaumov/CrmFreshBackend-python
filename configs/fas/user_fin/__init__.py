from lib.core import exists_arg
from lib.CRM.form import Form
#from .fields import get_fields
from .ajax import ajax
from .fields import fields

"""
create table user_fin(
id int unsigned primary key auto_increment,
user_id int unsigned,
registered timestamp not null default current_timestamp,
contact_date datetime not null default '0000-00-00 00:00:00' comment 'дата след. контакта',
status tinyint unsigned not null default '0' comment 'статус клиента',
product tinyint unsigned not null default '0' comment 'вид продукта',
manager_id int unsigned not null default '0' comment 'Менеджер ОП',
group_id int unsigned not null default '0' comment 'группа фин. продуктов',
manager_fin int unsigned not null default '0' comment 'Менеджер фин. продуктов',
underwriter int unsigned not null default '0' comment 'Андеррайтер',
rnt varchar(512) not null default ''
constraint foreign key(user_id) references user(id) on update cascade on delete cascade
) engine=innodb default charset=utf8 comment 'СР фин. продуктов';

CREATE TABLE `user_fin_memo` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID комментария',
  `manager_id` int(11) NOT NULL DEFAULT 0 COMMENT 'ID менеджера',
  `comment` varchar(2048) NOT NULL DEFAULT '' COMMENT 'Текст комментария',
  `registered` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Время/дата добавления',
  `user_fin_id` int unsigned,
  PRIMARY KEY (`id`),
  CONSTRAINT FOREIGN KEY (`user_fin_id`) REFERENCES user_fin(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='Комментарии к карточкам СР Фин-продуктов';

CREATE TABLE `user_fin_files` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_fin_id` int unsigned,
  `attach` varchar(255) NOT NULL DEFAULT '',
  `registered` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  CONSTRAINT  FOREIGN KEY (`user_fin_id`) REFERENCES `user_fin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
form={
    'wide_form':True,
    'title':'Совместная работа Фин. услуг', # в карте ОП, увдомления
    'work_table':'user_fin',
    'work_table_id':'id',
    'make_delete':0,
    'read_only':1,
    #'not_create':1,
    #'explain':1,
    'ajax':ajax,
    'is_admin':False,
    'cols':[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},              
            ],
            [
              {'description':'Работа с картой','name':'work','hide':0},
              #{'description':'Платежи','name':'paids','hide':0},
              {'description':'Контакты','name':'contacts','hide':0},
            ]
    ],
    'QUERY_SEARCH_TABLES':[
      {'t':'user_fin','a':'wt'},
      {'t':'user','a':'u','l':'u.id=wt.user_id','lj':1, 'for_fields':['firm', 'inn', 'f_city','manager_id']},
      {'t':'user','a':'s','l':'s.id=wt.supplier_id','lj':1, 'for_fields':['supplier_id']}, # поставщик
      {'t':'manager_group','a':'mg','l':'mg.id=wt.group_id','lj':1, 'for_fields':['group_id']},
      # фильтр для менеджера ОП
      {'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1, 'for_fields':['manager_id']},
      {'t':'manager_group','a':'mfg','l':'m.group_id=mfg.id','lj':1,},
      {'t':'manager','a':'m_fin','l':'wt.manager_fin=m_fin.id','lj':1, 'for_fields':['manager_fin']},
      {'t':'manager','a':'m_un','l':'wt.underwriter=m_un.id','lj':1, 'for_fields':['underwriter']}, # андеррайтер
      #{'t':'manager','a':'mt2','l':'wt.manager_to2=mt2.id','lj':1,'for_fields':['manager_to2']},
      #{'t':'manager','a':'me','l':'wt.exhibitor_id=me.id','lj':1,'for_fields':['exhibitor_id']},
      #{'t':'manager','a':'m_oso','l':'wt.manager_oso=m_oso.id','lj':1,'for_fields':['manager_oso']},
      
      #{'t':'city','a':'city','l':'city.city_id=wt.city_id','lj':1,'for_fields':['city_id']},
      #{'t':'teamwork_ofp_memo','a':'memo','l':'memo.teamwork_ofp_id=wt.teamwork_ofp_id','for_fields':['comment1']},
      #{'t':'manager','a':'m_memo','l':'m_memo.id=memo.manager_id','for_fields':['comment1']},
    ],
    #'explain':1,
    'filters_groups':[],
    'GROUP_BY':'wt.id',
    'fields':fields
}

#form['fields']=get_fields()


