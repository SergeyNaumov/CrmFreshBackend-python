from lib.core import exists_arg
from lib.CRM.form import Form
#from .fields import get_fields

from .code import *
form={
    #'wide_form':True,
    'title':'Совместная работа',
    'work_table':'teamwork_ofp',
    'work_table_id':'teamwork_ofp_id',
    'make_delete':0,
    #'ajax':ajax,
    'is_admin':False,
    'QUERY_SEARCH_TABLES':[
      {'t':'teamwork_ofp','a':'wt'},
      {'t':'user','a':'u','l':'u.id=wt.user_id','lj':1, 'for_fields':['f_city']},
      {'t':'manager','a':'mf','l':'wt.manager_from=mf.id','lj':1, 'for_fields':['manager_from','managers_groups_name']},
      {'t':'manager','a':'mt','l':'wt.manager_to=mt.id','lj':1},
      {'t':'manager','a':'mt2','l':'wt.manager_to2=mt2.id','lj':1,'for_fields':['manager_to2']},
      {'t':'manager','a':'me','l':'wt.exhibitor_id=me.id','lj':1,'for_fields':['exhibitor_id']},
      {'t':'manager','a':'m_oso','l':'wt.manager_oso=m_oso.id','lj':1,'for_fields':['manager_oso']},
      {'t':'manager_group','a':'mfg','l':'mf.group_id=mfg.id','lj':1,'for_fields':['manager_from','managers_groups_name']},
      {'t':'city','a':'city','l':'city.city_id=wt.city_id','lj':1,'for_fields':['city_id']},
      {'t':'teamwork_ofp_memo','a':'memo','l':'memo.teamwork_ofp_id_id=wt.teamwork_ofp_id','for_fields':['comment1']},
      {'t':'manager','a':'m_memo','l':'m_memo.id=memo.manager_id','for_fields':['comment1']},
      #{'t':'users_fs_memo_fp','a':'memo4','l':'memo4.users_fs_id=wt.user_id','for_fields':['comment4']},
      #{'t':'manager','a':'m_memo4','l':'m_memo4.id=memo4.manager_id','for_fields':['comment4']},
    ],

    'filters_groups':[],
    'GROUP_BY':'wt.teamwork_ofp_id',
    'fields':[

        {
            'description':'№',
            'type':'text',
            'name':'teamwork_ofp_id',
            'tab':'ofp',
            'read_only':True,
        },
        {
            'description':'Дата создания',
            'type':'datetime',
            'name':'born',
            #before_code=>sub{
            #  my $e=shift;
            #  if($form->{manager}->{login} eq 'akulov'){
            #    $e->{read_only}=0;
            #  }
            #},
            #after_insert=>sub{
            #  $form->{dbh}->do("UPDATE teamwork_ofp set born=now() where teamwork_ofp_id=$form->{id}");
            #},
            'read_only':True,
        },
        {
            'description':'Дата следующего контакта',
            'type':'datetime',
            'name':'contact_date',
            'tab':'ofp',
        },
        {
            'description':'Наименование компании',
            'type':'text',
            'name':'firm',
            #regexp=>'.+',
        },
        {
            'description':'Карточка продаж',
            'name':'link_to_card',
            'type':'code',
            'code':link_to_card_code
        },
        { # формируем ссылку на реестровый номер (доделать!!!)
          'description':'Реестровый номер',
          'type':'text',
          'name':'regnumber',
          'replace_rules':[
                '/^\s+/', '',
                '/\s+$/', '',
           ]
        },
        {
          'description':'Статус победы',
          'type':'select_values',
          'name':'win_status',
          'values':[
            {'v':1,'d':'Победа','c':'forestgreen'},
            {'v':2,'d':'В работе','c':'yellow'},
            {'v':3,'d':'Поражение','c':'red'},
            {'v':4,'d':'Работа не велась, оплаты не было','c':'blue'},
          ],
        },
        {
          'description':'Дата изменения статуса победы',
          'type':'date',
          'name':'win_status_change_date',
          'read_only':1,
        },
        {
          'description':'Председатель комиссии',
          'type':'text',
          'name':'pred_comm',
          'placeholder':'обязательно укажите председателя комиссии',
        },
        {
          'description':'Статус клиента',
          'name':'client_status',
          'type':'select_values',
          'values':[
            {'v':3,'d':'В работе'},
            {'v':6,'d':'Заявка подана'},
            {'v':2,'d':'Одобрено, получена платежка'},
            {'v':4,'d':'Одобрено, отказ клиента'},
            {'v':1,'d':'Отказ Банка/МФО'},
            {'v':9,'d':'Gередан в гр. Тихонова по регламенту'},
          ],
          'read_only':1,
          'before_code':client_status_before_code
        },
        {
            'description':'ИНН',
            'type':'text',
            'name':'inn',
            'regexp_rules':[
                '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ]
            # code=>sub{
            #   my $e=shift;
            #   $e->{value}=~s{[^\d]}{}g;
            #   #pre();
            #   if($e->{value}=~m{\d+} &&
            #     (
            #       $form->{manager}->{full_path}=~m{\/155($|\/)}
            #         ||
            #       $form->{manager}->{login}=~m{admin1|akulov}
            #     )
            #   ){
                
            #     $e->{field}.=qq{<a href="/moderator/crm_fresh/find_objects.pl?config=sr_ofp_win_card&order_firm=1&order_status=1&inn=$e->{value}&order_inn=2&order_type=3&order_NN=4&order_regnumber=5&order_client_status=6&order_manager_to=7&order_create_date=8&filter_create_date_disabled=1&order_memo=9" target="_blank">поиск дублей</a>}
            #     #$e->{field}.=qq{<a href="./find_objects.pl?config=sr_ofp_win_card&order_firm=1&order_status=2&inn=$e->{value}&order_inn=2&order_type=3&order_regnumber=4&order_manager_to=5&order_create_date=6&filter_create_date_disabled=1&order_memo=7" target="_blank">поиск дублей</a>}
            #   }
            #   return $e->{field}
            # },
        },
        {
            'description':'Вид продукта',
            'name': 'product',
            'before_code': product_before_code,
            'regexp_rules': [
                '/^\d+$/','выберите корректное значение'
            ],
            'multiple':5,
            'values':[
              {'v':3,'d':'Банковская Гарантия (Аукцион выигран с нашей помощью)'},
              {'v':4,'d':'Банковская Гарантия (есть победитель)'},
              {'v':5,'d':'Банковская гарантия, консультация для продажи тарифа (50/50 от оплаченного тарифа)'},
              {'v':10,'d':'Банковская гарантия (консультация на будущее)'},
              {'v':7,'d':'Тендерный займ (нужен под конкретный аукцион)'},
              {'v':8,'d':'Подготовка документации'},
              {'v':9,'d':'Юридические услуги (разное)'},
              {'v':14,'d':'Юридические услуги (ФАС)'},
              {'v':15,'d':'Юридические услуги (Арбитраж)'},
              {'v':11,'d':'Оформление сро, Лицензий, Допусков'},
              {'v':12,'d':'Лизинг'},
              {'v':13,'d':'Факторинг'},


            ],
            'type':'select_values', 
        },
        {
          'description':'Дата и время заседания',
          'type':'datetime',
          'name':'dat_session',
          'before_code':dat_session_before_code,
          'read_only':True,
          
        },
        {
          'description':'Представитель',
          'type':'select_from_table',
          'name':'exhibitor_id',
          'table':'manager',
          'tablename':'me',
          'where':'group_id in (select id from manager_group where parent_id=347 or path regexp "/347/")', # группа 
          'header_field':'name',
          'value_field':'id',
        },
        # !!!!не отображается список, наладить
        {
          'description':'Город заседания',
          'type':'select_from_table',
          'autocomplete':True,
          'name':'city_id',
          'table':'city',
          'tablename':'city',
          'header_field':'name',
          'search_query':"SELECT c.city_id v, concat(r.header,' -> ', c.name ) d FROM city c join region r ON (r.region_id=c.region_id) where c.name like <%v%>",
          'value_field':'city_id',     
        },
       {
          'description':'Время вылета на заседание',
          'name':'date_fly_to',
          'type':'datetime',
          
        },
        {
          'description':'Время возвращения с заседания',
          'name':'date_fly_from',
          'type':'datetime',
          
        },
        {
          'description':'Файл',
          'name':'attach',
          'type':'file',
          'filedir':'./files/teamwork_ofp',
          
          # after_save=>sub{
          #   if($form->{new_values}->{attach}){
          #       send_mes({
          #           from=>'noreply@trade.su',
          #           message=>qq{
          #             $form->{manager}->{name} только что добавил документ в карточку ОФП:
          #             Наименование компании: <a href="http://trade.su/moderator/crm_fresh/edit_form.pl?config=$form->{config}&action=edit&id=$form->{id}">$form->{old_values}->{firm}</a><br>
          #           },
          #           subject=>'Новый документ в карточке  ОФП / '.$form->{old_values}->{firm},
          #           to=>$to
          #       });
          #   }
          # }
        },
        {
            'description':'Контактное лицо',
            'type':'text',
            'name':'contact',
        },
        {
            'description':'Группа менеджеров',
            'type':'filter_extend_select_from_table', # фильтр для сложного запроса
            'table':'manager_group',
            'name':'managers_groups_name',
            'tablename':'mfg',
            'db_name':'id',
            # название таблицы, из которой будет происходить выборка по этому фильтру
            'filter_table': 'manager_group',
            'header_field': 'header',
            'value_field': 'id',
            'tree_use':True
        },
        {
            'description':'Менеджер',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_from',
            'header_field':'name',
            'order':'name',
            'value_field':'id',
            'tablename':'mf',
            'regexp_rules':[
                '/^\d+$/','выберите менеджера'
            ],
            'before_code':manager_from_before_code,            
            'read_only':True
        },
        {
            'description':'Руководитель группы',
            'type':'code',
            'name':'group_owner',
        },
    ]
}

#form['fields']=get_fields()


