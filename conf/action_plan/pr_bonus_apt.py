def pr_bonus_apt(form,field):
    # form.id -- action.id
    #form.pre(form.manager['ur_lico_ids'])
    #form.pre(form.manager['apt_list_ids'])
    
    if form.manager['type'] not in [1,2]:
        return
    field['before_html']='<h2 style="margin-top: 20px; margin-bottom: 10px;">Прогнозный бонус по аптекам</h2>'
    # Данное поле только для аптек
    bonus_list=[]
    total_left_to_complete_label='Осталось выполнить в рублях'
    if form.ov['plan']==2:
        total_left_to_complete_label='Осталось выполнить в шт'
    
    

    if 'apt_list_ids' in form.manager and len(form.manager['apt_list_ids']):
            bonus_list=form.db.query(
                query=f"""
                    SELECT
                        pb.*,a.ur_address header, a.id ur_lico_id
                    FROM
                        prognoz_bonus_apteka pb
                        LEFT JOIN apteka a ON a.id=pb.apteka_id
                    WHERE
                        period_id=%s and pb.action_plan_id=%s and pb.apteka_id in ({','.join(form.manager['apt_list_ids'])})
                """,
                values=[form.ov['period']['id'],form.id]
            )
            #form.pre(bonus_list)
            #form.pre([form.ov['period']['id'],form.id])
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

            # параметр "кол-во закупки" нужно поставить после суммы закупки в сип ценах, если план у нас суммовой и перед суммой в сип ценах если план количественный.
            body_text=''
            if form.ov['plan'] in (1,3): # Количественный
                body_text=f'''
                    Кол-во аптек: {b['cnt_apt']}<br>
                    План для аптеки: {b['plan']}<br>
                    сумма закупки в sip-ценах: {b['price']}<br>
                    кол-во закупки: {b['buy_cnt']}<br>
                    процент выполнения: {b['percent_complete']}<br>
                    текущий бонус: {b['current_bonus']}<br>
                    процент выполнения при сохранении темпа закупки: {b['percent_progress']}<br>
                    бонус при сохранении темпа закупки: {b['bonus_progress']}<br>
                    остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {b['other_distrib_sum']}<br>
                    упущенная выгода (общая сумма, сколько недополучили): {b['lost_profit']}<br>
                    осталось выполнить в %: {b['left_to_complete_percent']}<br>
                    {total_left_to_complete_label}: {b['left_to_complete_rub']}<br>
                    
                '''
            elif form.ov['plan']==2: # Суммовой
                body_text=f'''
                    Кол-во аптек: {b['cnt_apt']}<br>
                    План для аптеки: {b['plan']}<br>
                    кол-во закупки: {b['buy_cnt']}<br>
                    сумма закупки в sip-ценах: {b['price']}<br>
                    процент выполнения: {b['percent_complete']}<br>
                    текущий бонус: {b['current_bonus']}<br>
                    процент выполнения при сохранении темпа закупки: {b['percent_progress']}<br>
                    бонус при сохранении темпа закупки: {b['bonus_progress']}<br>
                    остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {b['other_distrib_sum']}<br>
                    упущенная выгода (общая сумма, сколько недополучили): {b['lost_profit']}<br>
                    осталось выполнить в %: {b['left_to_complete_percent']}<br>
                    {total_left_to_complete_label}: {b['left_to_complete_rub']}<br>
                    
                '''
            
            accordion_item={
                'header':b['header'],
                'content':[

                    {
                        'type':'html',
                        'body':f'''
                          <div id="bonus_ur_lico{b['ur_lico_id']}" class="prognoz_bonus_item"> 
                            <div style="padding-left: 20px; margin-bottom: 20px;">
                                {body_text}
                            </div>
                          </div>

                    '''
                    },
                    {
                        'type':'chart',
                        'subtype':'circle',
                        'description':'диаграмма выполнения',
                        'labels':[f"""процент выполнения ({b['percent_complete']})%""",f"""осталось выполнить ({b['left_to_complete_percent']})%"""],
                        'values':[b['percent_complete'],b['left_to_complete_percent']],
                        'width':320,
                        'height':200,
                        #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                    },
                    {
                        'type':'chart',
                        'subtype':'circle',
                        'description':'дистрибьютеры',
                        'labels':[f"""разрешённые дистрибьютеры ({b['price']})""",f"""остальные дистрибьютеры ({b['other_distrib_sum']})"""],
                        'values':[b['price'],b['other_distrib_sum']],
                        'width':320,
                        'height':200,
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
                total_percent_complete = int(100 * (total_price / total_plan))
                

                '''     
                form.ov['period']['querter_begin_days'] -- кол-во дней, прошедших с начала квартала, включая сегодняшний
                form.ov['period']['querter_total_days'] -- кол-во дней в квартале

                Выполнение при сохранении темпа закупки % = 
                сумма закупки (или кол-во закупки)  / кол-во дней с начала квартала, включая день формирования
                    *
                кол-во дней в квартале / план на квартал в рублях или упаковках
                ''' 
                querter_begin_days=int(form.ov['period']['querter_begin_days'])
                querter_total_days=int(form.ov['period']['querter_total_days'])
                
                if form.ov['period']['prev']:
                    querter_begin_days=querter_total_days

                
                if form.ov['plan'] in (1,3): # Суммовой
                    
                    #print('total_plan:',total_plan)
                    #form.pre(f'100*({total_buy_cnt}/{querter_begin_days} * {querter_total_days}/{total_plan})')
                    total_percent_progress=round( 100*(total_price/querter_begin_days * querter_total_days/ int(total_plan) ),2 )
                    
                elif form.ov['plan']==2: # Количественный
                    #form.pre(2)
                    total_percent_progress=round( 100*(total_buy_cnt/querter_begin_days * querter_total_days/int(total_plan)),2 )
                    

                if total_percent_complete<100:
                    total_left_to_complete_percent=100-total_percent_complete


            
            

        
        #form.pre(form.ov['period'])
        #form.pre(form.ov['period']['querter_begin_days'])

        if len(bonus_list) > 1:
            body_text=''
            # параметр "кол-во закупки" нужно поставить после суммы закупки в сип ценах, если план у нас суммовой и перед суммой в сип ценах если план количественный.
            if form.ov['plan'] in (1,3): # Суммовой
                body_text=f'''
                    Кол-во аптек: {total_cnt_apt}<br>
                    План для юридических лиц: {total_plan}<br>
                    Количество закупки: {total_buy_cnt}<br>
                    Сумма закупки в sip-ценах: {total_price}<br>
                    Процент выполнения: {total_percent_complete}<br>
                    Текущий бонус: {total_current_bonus}<br>
                    Процент выполнения при сохранении темпов закупки: {total_percent_progress}<br>
                    Остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {total_other_distrib_sum}<br>
                    Бонус при сохранении темпа закупки: {total_bonus_progress}<br>
                    Осталось выполнить в %: {total_left_to_complete_percent}<br>
                    {total_left_to_complete_label}: {total_left_to_complete_rub}<br>
                    
                '''
            elif form.ov['plan']==2: # Количественный
                body_text=f'''
                    Кол-во аптек: {total_cnt_apt}<br>
                    План для юридических лиц: {total_plan}<br>
                    Сумма закупки в sip-ценах: {total_price}<br>
                    Количество закупки: {total_buy_cnt}<br>
                    Процент выполнения: {total_percent_complete}<br>
                    Текущий бонус: {total_current_bonus}<br>
                    Процент выполнения при сохранении темпов закупки: {total_percent_progress}<br>
                    Остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {total_other_distrib_sum}<br>
                    Бонус при сохранении темпа закупки: {total_bonus_progress}<br>
                    Осталось выполнить в %: {total_left_to_complete_percent}<br>
                    {total_left_to_complete_label}: {total_left_to_complete_rub}<br>
                    
                '''
            # СВОДНЫЕ ДАННЫЕ ПО АПТЕКАМ ПОПРОСИЛИ УБРАТЬ
            # accordion_data.insert(0,
            #     {
            #         'header':'* Сводные данные по всем юридическим лицам',
            #         'content':[

            #             {
            #             'type':'html',
            #             'body':f'''
            #                 <div style="margin-top: 20px; margin-bottom: 20px; border: 1px solid gray; padding: 20px; border-radius: 4px;">
            #                     <h2>Сводные данные по всем юрлицам</h2>
            #                     <br>
            #                     {body_text}
            #                 </div>
            #             ''',
            #         },
            #         {
            #             'type':'chart',
            #             'subtype':'circle',
            #             'description':'диаграмма выполнения',
            #             'labels':[f"""процент выполнения({total_percent_complete})%""",f"""осталось выполнить ({total_left_to_complete_percent})%"""],
            #             'values':[total_percent_complete,total_left_to_complete_percent],
            #             'width':320,
            #             'height':200,
            #             #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

            #         },
            #         {
            #             'type':'chart',
            #             'subtype':'circle',
            #             'description':'дистрибьютеры',
            #             'labels':[f"""разрешённые дистрибьютеры ({total_price})""",f"""остальные дистрибьютеры ({total_other_distrib_sum})"""],
            #             'values':[total_price,total_other_distrib_sum],
            #             'width':320,
            #             'height':200,
            #             #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

            #         }
            #     ]

            # })
        
        field['data']=accordion_data

    else:
        
        period=form.ov['period']
        field['after_html']=f'''
            <p style="color: red;">Информация по прогнозному бонусу за {period['querter']} квартал {period['year']} отсутствует </p>
        '''
        #form.pre(form.ov)