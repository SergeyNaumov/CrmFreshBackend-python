"""
DROP TABLE tarif_manager;
CREATE TABLE `tarif_manager` (
  id int unsigned primary key auto_increment,
  `tarif_id` int unsigned NOT NULL,
  `manager_id` int unsigned NOT NULL,
  `percent` tinyint unsigned NOT NULL DEFAULT '0',
  UNIQUE KEY (`tarif_id`,`manager_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT FOREIGN KEY (`tarif_id`) REFERENCES `tarif` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""
async def bank_before_code(form,field):
    if form.id and form.ov:
        if not form.ov['position']:
            field['read_only'] = 1
        field['relation_table_where']=f"position={form.ov['position']} and position <> 0"
    else:
        field['read_only']=1
        field['after_html']='Выберите должность данного сотрудника, чтобы указать процент начислений'
        #form.remove_field(field['name'])

fields=[
    {
      'before_code': bank_before_code,
      'description':'Процент менеджера по тарифам',
      'type':'multiconnect',
      'tree_table':'permissions',
      'name':'bank_percent',
      'subtype':'table',
      'fields':[
        {
            'description':'Процент',
            'type':'text',
            'name':'percent',
            'subtype':'percent'
        },
      ],
      'tablename':'pos',
      'relation_table':'tarif',
      'relation_save_table':'tarif_manager',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'manager_id',
      'relation_save_table_id_relation':'tarif_id',
      'tab':'bank',
    },
    {
      'before_code': bank_before_code,
      'description':'Процент менеджера по услугам',
      'type':'multiconnect',
      'tree_table':'permissions',
      'name':'bank_percent2',
      'subtype':'table',
      'fields':[
        {
            'description':'Процент',
            'type':'text',
            'name':'percent',
            'subtype':'percent'
        },
      ],
      'tablename':'pos',
      'relation_table':'service',
      'relation_save_table':'service_manager',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'manager_id',
      'relation_save_table_id_relation':'service_id',
      'tab':'bank',
    },
]