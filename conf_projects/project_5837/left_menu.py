# Левое меню бэкендера для проекта 5837 (CMS-конструктор t1).
# Если файла нет — меню собирается из стандартных сервисов (struct_public):
# Promo, Статичные текстовые страницы, Верхнее меню, Константы шаблона.
left_menu = [
    {
        "header": "Характеристики товаров",
        "value": "admin-tree",
        "type": "vue",
        "icon": "fa fa-list",
        "child": [
            {
                "header": "Справочник параметров",
                "value": "admin-tree",
                "type": "vue",
                "child": [],
                "params": {"config": "params"},
            },
            {
                "header": "Параметры рубрик",
                "value": "admin-tree",
                "type": "vue",
                "child": [],
                "params": {"config": "params_catalog"},
            },
            {
                "header": "Значения по товарам",
                "value": "admin-tree",
                "type": "vue",
                "child": [],
                "params": {"config": "params_good"},
            },
        ],
    },
]