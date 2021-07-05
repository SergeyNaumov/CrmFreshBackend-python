def pr_bonus(form,field):
    # form.id -- action.id
    #form.pre(form.manager['ur_lico_ids'])
    #form.pre(form.manager['apt_list_ids'])
    bonus_list=[]

    if form.id and form.manager['type']==2:
        if len(form.manager['ur_lico_ids']):
            bonus_list=form.db.query(
                query=f"""
                    SELECT
                        pb.*,u.header
                    FROM
                        prognoz_bonus pb
                        LEFT JOIN ur_lico u ON u.id=pb.ur_lico_id
                    WHERE
                        pb.action_plan_id=%s and pb.ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})
                """,
                values=[form.id]
            )
            #form.pre(bonus_list)
    else:
        return
    if len(bonus_list):
        # field['after_html']=form.template(
        #   './conf/action/templates/prognoz_bonus.html',
        #   bonus_list=bonus_list
        # )
        #form.tabs.append({'description':'<span style="color: red;">Прогнозный бонус</span>','name':'pr_bonus','tab_style':'color: red;'})

        # Переделываем в аккордеон
        field['type']='accordion'
        #form.pre(bonus_list)
        accordion_data=[]
        
        total_cnt_apt=0
        total_plan=0
        total_price=0
        total_current_bonus=0
        total_bonus_progress=0
        total_other_distrib_sum=0
        total_left_to_complete_rub=0
        total_buy_cnt=0
        total_percent_complete=0
        total_left_to_complete_percent=0
        total_percent_progress=0

        for b in bonus_list:
            #form.pre(b)
            accordion_item={
                'header':b['header'],
                'content':[

                    {
                        'type':'html',
                        'body':f'''
                          <div id="bonus_ur_lico{b['ur_lico_id']}" class="prognoz_bonus_item"> 
                            <!--<div><b>{b['header']}</b></div>-->
                            <div style="padding-left: 20px; margin-bottom: 20px;">
                                Кол-во аптек: {b['cnt_apt']}<br>
                                План для юридического лица: {b['plan']}<br>
                                сумма закупки в sip-ценах: {b['price']}<br>
                                процент выполнения: {b['percent_complete']}<br>
                                текущий бонус: {b['current_bonus']}<br>
                                процент выполнения при сохранении темпа закупки: {b['percent_progress']}<br>
                                бонус при сохранении темпа закупки: {b['bonus_progress']}<br>
                                остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {b['other_distrib_sum']}<br>
                                упущенная выгода (общая сумма, сколько недополучили): {b['lost_profit']}<br>
                                осталось выполнить в %: {b['left_to_complete_percent']}<br>
                                осталось выполнить в рублях: {b['left_to_complete_rub']}<br>
                                кол-во закупки: {b['buy_cnt']}<br>

                            </div>
                          </div>

                    '''
                    },
                    {
                        'type':'chart',
                        'subtype':'circle',
                        'description':'диаграмма выполнения',
                        'labels':[f"""процент выполнения({b['percent_complete']})%""",f"""осталось выполнить ({b['left_to_complete_percent']})%"""],
                        'values':[b['percent_complete'],b['left_to_complete_percent']],
                        'width':320,
                        'height':250,
                        #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                    },
                    {
                        'type':'chart',
                        'subtype':'circle',
                        'description':'дистрибьютеры',
                        'labels':[f"""разрешённые дистрибьютеры ({b['price']})""",f"""остальные дистрибьютеры ({b['other_distrib_sum']})"""],
                        'values':[b['price'],b['other_distrib_sum']],
                        'width':320,
                        'height':250,
                        #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                    },
                ]

            }
            accordion_data.append(accordion_item)

            # вычисления для сводных данных
            total_cnt_apt+=b['cnt_apt']
            total_plan+=b['plan']
            total_price+=b['price']
            total_current_bonus+=b['current_bonus']
            total_bonus_progress+=b['bonus_progress']
            total_other_distrib_sum+=b['other_distrib_sum']
            total_buy_cnt+=b['buy_cnt']
            total_left_to_complete_rub+=b['left_to_complete_rub']
            
            # Процент выполнения = сумма закупки в сип-ценах / план
            if total_plan:
                total_percent_complete = round(100 * (total_price / total_plan),2)
                total_percent_progress=round( 100*(total_price/90 * 91/total_plan),2 )
                if total_percent_complete<100:
                    total_left_to_complete_percent=100-total_percent_complete


            
            

        

        if len(bonus_list) > 1:

            #field['before_html']=
            accordion_data.insert(0,
                {
                    'header':'* Сводные данные по всем юридическим лицам',
                    'content':[

                        {
                        'type':'html',
                        'body':f'''
                            <div style="margin-top: 20px; margin-bottom: 20px; border: 1px solid gray; padding: 20px; border-radius: 4px;">
                                <h2>Сводные данные по всем юрлицам</h2>
                                <br>
                                Кол-во аптек: {total_cnt_apt}<br>
                                План для юридических лиц: {total_plan}<br>
                                Сумма закупки в sip-ценах: {total_price}<br>
                                Процент выполнения: {total_percent_complete}<br>
                                Текущий бонус: {total_current_bonus}<br>
                                Процент выполнения при сохранении темпов закупки: {total_percent_progress}<br>
                                Остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {total_other_distrib_sum}<br>
                                Бонус при сохранении темпа закупки: {total_bonus_progress}<br>
                                Осталось выполнить в %: {total_left_to_complete_percent}<br>
                                Осталось выполнить в рублях: {total_left_to_complete_rub}<br>
                                Количество закупки: {total_buy_cnt}<br>
                            </div>
                        ''',
                    },
                    # {
                    #     'type':'chart',
                    #     'subtype':'circle',
                    #     'description':'диаграмма выполнения',
                    #     'labels':[f"""процент выполнения({b['percent_complete']})%""",f"""осталось выполнить ({b['left_to_complete_percent']})%"""],
                    #     'values':[b['percent_complete'],b['left_to_complete_percent']],
                    #     'width':320,
                    #     'height':250,
                    #     #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                    # },
                    {
                        'type':'chart',
                        'subtype':'circle',
                        'description':'дистрибьютеры',
                        'labels':[f"""разрешённые дистрибьютеры ({b['price']})""",f"""остальные дистрибьютеры ({b['other_distrib_sum']})"""],
                        'values':[total_price,total_other_distrib_sum],
                        'width':320,
                        'height':250,
                        #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                    }
                ]

            })
        
        field['data']=accordion_data

    #else:
    #    form.pre('нет прогнозного бонуса')
    #form.pre(form.ov)