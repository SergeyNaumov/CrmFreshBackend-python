"""
CREATE TABLE `test_dep` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dep1` varchar(20) DEFAULT NULL,
  `dep2` varchar(20) DEFAULT NULL,
  `dep3` tinyint(1) NOT NULL DEFAULT '0',
  `dep4` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
dep1_js=''
with open('./configs/test/dependences/js/dep1.js','r',encoding='utf-8') as file:
    dep1_js=file.read()

form={
    'work_table':'test',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Зависимые поля',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[

    ],
    'cols':[
        [
            {'description':'Блок1','name':'dep1'},
            {'description':'Блок2','name':'dep2'},
        ],
        [

            {'description':'Блок3','name':'dep3'},
            {'description':'Блок4','name':'dep4'},
        ]
    ],
    'fields': [ 

        {
            'description':'Поле, от которого зависят другие поля',
            'type':'select_values',
            'name':'dep1',
            'values':[
                {'v':1,'d':'скрыть dep2, dep3 и dep4'},
                {'v':2,'d':'показать второй select'},
                {'v':3,'d':'показать второй select, а также текстовые поля'},
                {'v':4,'d':'заполнить рандомно текстовые поля'},
                {'v':5,'d':'скрыть все вкладки кроме этой'},
                {'v':6,'d':'показать описание'},
            ],

            'frontend':{
                'fields_dependence':dep1_js, # изменяем поведение других полей
                'tabs_dependence':'' # изменяем поведение табов
            },
            'before_html':'''
                <div id="dep1_before_html" style="display: none;">
                    <p>Иногда требуется сделать так, чтобы в зависимости от выбранного значения в одном поле, изменялось поведение других полей.</p>
                    <p>Например, если это опросник, при выборе отсутствие подходящего варианта, можно предложить указать свой (сделать так, чтобы появилось некое поле для ввода текста).</p>
                    <p>Могут понадобится варианты посложнее</p>
                </div>
            ''',
            'tab':'dep1'
        },
        {
            'description':'dep2',
            'name':'dep2',
            'type':'select_values',
            'values':[
                {'v':1,'d':'Значение1'},
                {'v':2,'d':'Значение2'},
                {'v':3,'d':'Значение3'},
            ],
            'tab':'dep2'

        },
        {
            'description':'Текстовое поле!',
            'tab':'dependences',
            'type':'textarea',
            'name':'dep3',
            'tab':'dep3',
            'frontend':{
                'after_buttons':[
                    {'description':'кнопка1','js':''},
                    {'description':'кнопка2','js':''},
                    {'description':'кнопка3','js':''},
                ]
            },
        },
        {
            'description':'Текстовое поле1',
            'tab':'dependences',
            'type':'textarea',
            'name':'dep4',
            'tab':'dep4'
        },

  ]  
    
}
      


