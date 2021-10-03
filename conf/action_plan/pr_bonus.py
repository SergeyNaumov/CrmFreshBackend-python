def pr_bonus(form,field):

    # form.id -- action.id
    #form.pre(form.manager['ur_lico_ids'])
    #form.pre(form.manager['apt_list_ids'])
    bonus_list=[]

    #form.pre({'total_good_price':total_good_price})

    total_left_to_complete_label='осталось выполнить в рублях'
    if len(form.errors):
      return 
    if form.ov['plan']==2:
        total_left_to_complete_label='осталось выполнить в шт'
    label_plan='план для юридического лица'
    set1=1
    set2=1
    if form.manager['type']==3:
        set1=form.manager['apteka_settings']['set1']
        set2=form.manager['apteka_settings']['set2']
        
      
    if form.id and form.manager['type'] in [1,2]:

        field['before_html']='<h2 style="margin-top: 20px; margin-bottom: 10px;">Прогнозный бонус по юридическим лицам</h2>'
        if len(form.manager['ur_lico_ids']):
            bonus_list=form.db.query(
                query=f"""
                    SELECT
                        pb.*,u.header
                    FROM
                        prognoz_bonus pb
                        LEFT JOIN ur_lico u ON u.id=pb.ur_lico_id
                    WHERE
                        period_id=%s and pb.action_plan_id=%s and pb.ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})
                """,
                values=[form.ov['period']['id'],form.id],
            
            )

    elif form.id and form.manager['type']==3:
        label_plan='План для аптеки'
        if len(form.manager['apt_list_ids']):
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
        total={
            'cnt_apt':0,
            'plan':0,
            'price':0,
            'current_bonus':0,
            'bonus_progress':0,
            'other_distrib_sum':0,
            'left_to_complete_rub':0,
            'buy_cnt':0,
            'percent_complete':0,
            'left_to_complete_percent':0,
            'percent_progress':0,
            'lost_profit':0,
            'earned_bonus':0
        }
        
        # total_plan=0
        # total_price=0
        # total_current_bonus=0
        # total_bonus_progress=0
        # total_other_distrib_sum=0
        # total_left_to_complete_rub=0
        # total_buy_cnt=0
        # total_percent_complete=0
        # total_left_to_complete_percent=0
        # total_percent_progress=0
        # total_lost_profit=0
        # total_earned_bonus=0

        for b in bonus_list:
            # параметр "кол-во закупки" нужно поставить после суммы закупки в сип ценах, если план у нас суммовой и перед суммой в сип ценах если план количественный.
            if form.manager['type']==3 and form.manager['apteka_settings']['set1']==0:
                    accordion_data.append({
                        'header':b['header'],
                        'content':[
                            {
                                'type':'html',
                                'body':f'''
                                  <div class="prognoz_bonus_item"> 
                                    <div style="padding-left: 20px; margin-bottom: 20px;">
                                        Доступ к информации о прогнозном бонусе закрыт
                                    </div>
                                  </div>

                            '''
                            },
                        ]
                    })
            else:
                    body_text=form.template(
                        './conf/action_plan/templates/pr_bonus.html',
                        ov=form.ov,
                        manager=form.manager,
                        label_plan=label_plan,
                        total_left_to_complete_label=total_left_to_complete_label,
                        #total_good_price=total_good_price,
                        b=b,
                        set1=set1,
                        set2=set2
                    )
        #            if form.manager['type'] !=3:
        #                body_text=f'Кол-во аптек: {b["cnt_apt"]}<br>'

                    # if form.ov['plan'] in (1,3): # Суммовой
                    #     body_text=f'''
                    #         {label_plan}: {b['plan']}<br>
                    #         сумма закупки в sip-ценах: {b['price']}<br>
                    #         кол-во закупки: {b['buy_cnt']}<br>
                    #         процент выполнения: {b['percent_complete']}<br>
                    #         текущий бонус: {b['current_bonus']}<br>
                    #         процент выполнения при сохранении темпа закупки: {b['percent_progress']}<br>
                    #         бонус при сохранении темпа закупки: {b['bonus_progress']}<br>
                    #         остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {b['other_distrib_sum']}<br>
                    #         упущенная выгода (общая сумма, сколько недополучили): {b['lost_profit']}<br>
                    #         осталось выполнить в %: {b['left_to_complete_percent']}<br>
                    #         заработанный бонус: {b['earned_bonus']}<br>

                    #     '''
                    # elif form.ov['plan']==2: # Количественный
                    #     body_text=f'''
                            
                    #         {label_plan}: {b['plan']}<br>
                    #         кол-во закупки: {b['buy_cnt']}<br>
                    #         сумма закупки в sip-ценах: {b['price']}<br>
                    #         процент выполнения: {b['percent_complete']}<br>
                    #         текущий бонус: {b['current_bonus']}<br>
                    #         процент выполнения при сохранении темпа закупки: {b['percent_progress']}<br>
                    #         бонус при сохранении темпа закупки: {b['bonus_progress']}<br>
                    #         остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {b['other_distrib_sum']}<br>
                    #         упущенная выгода (общая сумма, сколько недополучили): {b['lost_profit']}<br>
                    #         осталось выполнить в %: {b['left_to_complete_percent']}<br>
                    #         заработанный бонус: {b['earned_bonus']}<br>
                    #     '''

                    #if b['left_to_complete_percent']>0:
                    #    body_text+=f'''{total_left_to_complete_label}: {b['left_to_complete_rub']}<br>'''

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

                        ]

                    }

                    # диаграммы добавляем только к планам, отличным от "% за любые закупки"

                    if form.ov['plan']!=3:

                        accordion_item['content'].append(
                            {
                                'type':'chart',
                                'subtype':'circle',
                                'description':'диаграмма выполнения',
                                'labels':[f"""процент выполнения ({b['percent_complete']})%""",f"""осталось выполнить ({b['left_to_complete_percent']})%"""],
                                'values':[b['percent_complete'],b['left_to_complete_percent']],
                                'width':320,
                                'height':200,
                                #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                            }
                        )

                        accordion_item['content'].append(
                            {
                                'type':'chart',
                                'subtype':'circle',
                                'description':'дистрибьютеры',
                                'labels':[f"""разрешённые дистрибьютеры ({b['price']})""",f"""остальные дистрибьютеры ({b['other_distrib_sum']})"""],
                                'values':[b['price'],b['other_distrib_sum']],
                                'width':320,
                                'height':200,
                                #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                            }
                        )
                    
                    accordion_data.append(accordion_item)

            # вычисления для сводных данных
            total['cnt_apt']+=b['cnt_apt']
            total['plan']+=b['plan']
            total['price']+=b['price']
            total['current_bonus']+=b['current_bonus']
            total['bonus_progress']+=b['bonus_progress']
            total['other_distrib_sum']+=b['other_distrib_sum']
            total['buy_cnt']+=b['buy_cnt']
            total['left_to_complete_rub']+=b['left_to_complete_rub']
            total['lost_profit']+=b['lost_profit']
            total['earned_bonus']+=b['earned_bonus']
            # Процент выполнения = сумма закупки в сип-ценах / план
            if total['plan']:
                total['percent_complete'] = round(100 * (total['price'] / total['plan']),2)
                
                #form.pre(f'''100 * ({total['price']} / {total['plan']} )''')
                '''     
                form.ov['period']['querter_begin_days'] -- кол-во дней, прошедших с начала квартала, включая сегодняшний
                form.ov['period']['querter_total_days'] -- кол-во дней в квартале

                Выполнение при сохранении темпа закупки % = 
                сумма закупки (или кол-во закупки)  / кол-во дней с начала квартала, включая день формирования
                    *
                кол-во дней в квартале / план на квартал в рублях или упаковках
                ''' 
                querter_begin_days=int(form.ov['period']['querter_begin_days'])
                querter_total_days=int(form.ov['period']['querter_total_days'])+1
                #form.pre(form.ov['period'])
                if form.ov['period']['prev']:
                    querter_begin_days=querter_total_days

                
                if form.ov['plan'] in (1,3): # Суммовой
                    
                    #print('total_plan:',total_plan)
                    #form.pre(f'''100*({total['price']}/{querter_begin_days} * {querter_total_days}/{total['plan']})''')
                    total['percent_progress']=round( 100*(total['price']/querter_begin_days * querter_total_days/ int(total['plan']) ),2 )
                    
                elif form.ov['plan']==2: # Количественный
                    #form.pre(2)
                    total['percent_progress']=round( 100*(total['buy_cnt']/querter_begin_days * querter_total_days/int(total['plan'])),2 )
                    

                if total['percent_complete']<100:
                    total['left_to_complete_percent']=100-total['percent_complete']


            
            

        
        #form.pre(form.ov['period'])
        #form.pre(form.ov['period']['querter_begin_days'])

        if len(bonus_list) > 1:
            body_text=''
            total['bonus']=0
            '''
                - если процент выполнения<99, то выводим значение 0 
                - процент выполнения  или > или =99, то выводим  данные из строки "текущий бонус" 
                это мы можем сейчас сделать?
            '''
            if total['percent_progress']>=99:
                total['bonus']=total['current_bonus']
            
            if form.ov['plan']==1:
                pass
                #form.pre(str(total['plan'])+'-'+str(total['price']) )
                #total['current_bonus']=total['plan']-total['price']
            else:
                total['current_bonus']=total['plan']-total['buy_cnt']

            #form.pre(form.ov)
            body_text=form.template(
                './conf/action_plan/templates/pr_bonus.html',
                ov=form.ov,
                manager=form.manager,
                label_plan=label_plan,
                total_left_to_complete_label=total_left_to_complete_label,
                multi=1,
                b=total
            )
            # # параметр "кол-во закупки" нужно поставить после суммы закупки в сип ценах, если план у нас суммовой и перед суммой в сип ценах если план количественный.
            # if form.ov['plan'] in (1,3): # Суммовой
            #     body_text=f'''
            #         кол-во аптек: {total_cnt_apt}<br>
            #         план для юридических лиц: {total_plan}<br>
            #         сумма закупки в sip-ценах: {total_price}<br>
            #         количество закупки: {total_buy_cnt}<br>
            #         процент выполнения: {total_percent_complete}<br>
            #         текущий бонус: {total_current_bonus}<br>
            #         итоговой бонус: {total_bonus}<br>
            #         процент выполнения при сохранении темпов закупки: {total_percent_progress}<br>
            #         бонус при сохранении темпа закупки: {total_bonus_progress}<br>
            #         остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {total_other_distrib_sum}<br>
                    
            #         упущенная выгода (общая сумма, сколько недополучили): {total_lost_profit}<br>
            #         осталось выполнить в %: {total_left_to_complete_percent}<br>
            #         заработанный бонус: {total_earned_bonus}<br>
            #     '''
            # elif form.ov['plan']==2: # Количественный
            #     body_text=f'''
            #         кол-во аптек: {total_cnt_apt}<br>
            #         сумма закупки в sip-ценах: {total_price}<br>
            #         план для юридических лиц: {total_plan}<br>
            #         количество закупки: {total_buy_cnt}<br>
            #         процент выполнения: {total_percent_complete}<br>
            #         текущий бонус: {total_current_bonus}<br>
            #         итоговой бонус: {total_bonus}<br>
            #         процент выполнения при сохранении темпов закупки: {total_percent_progress}<br>
            #         бонус при сохранении темпа закупки: {total_bonus_progress}<br>
            #         остальные дистрибьютеры (сумма закупленного товара у всех неразрешённых поставщиков): {total_other_distrib_sum}<br>
                    
            #         упущенная выгода (общая сумма, сколько недополучили): {total_lost_profit}<br>
            #         осталось выполнить в %: {total_left_to_complete_percent}<br>
            #         заработанный бонус: {total_earned_bonus}<br>
            #     '''

            # if total['left_to_complete_percent']>0:
                
            #     body_text+=f"""{total_left_to_complete_label}: {total_left_to_complete_rub}<br>"""
            
            header_total='* Сводные данные по всем юридическим лицам'
            if form.manager['type']==3:
                header_total='* Сводные данные по всем аптекам!!'
            
            if form.manager['type']!=3: # для аптек просили убрать прогнозный бонус по всем аптекам
                accordion_data.insert(0,
                    {
                        'header':header_total,
                        'content':[

                            {
                            'type':'html',
                            'body':f'''
                                <div style="margin-top: 20px; margin-bottom: 20px; border: 1px solid gray; padding: 20px; border-radius: 4px;">
                                    <h2>Сводные данные по всем юрлицам</h2>
                                    <br>
                                    {body_text}
                                </div>
                            ''',
                        },


                    ]

                })

                if form.ov['plan']!=3:
                    accordion_data[0]['content'].append(
                        {
                            'type':'chart',
                            'subtype':'circle',
                            'description':'диаграмма выполнения',
                            'labels':[f"""процент выполнения({total['percent_complete']})%""",f"""осталось выполнить ({total['left_to_complete_percent']})%"""],
                            'values':[total['percent_complete'],total['left_to_complete_percent']],
                            'width':320,
                            'height':200,
                            #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                        },
                    )

                    accordion_data[0]['content'].append(
                        {
                            'type':'chart',
                            'subtype':'circle',
                            'description':'дистрибьютеры',
                            'labels':[f"""разрешённые дистрибьютеры ({total['price']})""",f"""остальные дистрибьютеры ({total['other_distrib_sum']})"""],
                            'values':[total['price'],total['other_distrib_sum']],
                            'width':320,
                            'height':200,
                            #'style':'display: inline-block; max-width: 100%; width: 50%; border: 1px solid gray;'

                        }
                    )
        #form.pre(accordion_data)
        field['data']=accordion_data

    else:
        
        period=form.ov['period']
        field['after_html']=f'''
            <p style="color: red;">Информация по прогнозному бонусу за {period['querter']} квартал {period['year']} отсутствует </p>
        '''
        #form.pre(form.ov)