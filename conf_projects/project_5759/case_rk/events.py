def ajax_tbl1_load_template(form,values):
    return [
        'tbl',{'value':'''
                <table class="table table_3">
                <tbody>
                <tr>
                <td>Регион</td>
                <td>Республика Адыгея, г. Майкоп</td>
                </tr>
                <tr>
                <td>Старт работы</td>
                <td>Февраль 2015</td>
                </tr>
                <tr>
                <td>Результат на</td>
                <td>Июнь 2015</td>
                </tr>
                <tr>
                <td>Ктегория</td>
                <td>Вывод в ТОП</td>
                </tr>
                <tr>
                <td>Адрес проекта URL</td>
                <td>bochkadub.com</td>
                </tr>
                </tbody>
                </table>
        '''}
    ]
    

def ajax_tbl2_load_template(form,values):
    return [
        'tbl2',{'value':'''
                <table class="table table_4">
                <tbody>
                <tr>
                <td>Запросы</td>
                <td>Частота запроса</td>
                <td>Место в ТОП 24.11.2022</td>
                <td>Место в ТОП 01.09.2022</td>
                </tr>
                <tr>
                <td>Нашивки на заказ</td>
                <td>912</td>
                <td>30</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Шеврон на заказ</td>
                <td>496</td>
                <td>54</td>
                <td>6 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивка на одежду на заказ</td>
                <td>301</td>
                <td>34</td>
                <td>7 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивка на заказ</td>
                <td>654</td>
                <td>36</td>
                <td>3 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивки на одежду на заказ</td>
                <td>301</td>
                <td>36</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Изготовление нашивок</td>
                <td>345</td>
                <td>38</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Заказать нашивку</td>
                <td>458</td>
                <td>25</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивки на заказ Москва</td>
                <td>139</td>
                <td>35</td>
                <td>5 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивка на одежду на заказ Москва</td>
                <td>93</td>
                <td>34</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Сделать нашивку</td>
                <td>-</td>
                <td>36</td>
                <td>7 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Заказать нашивки</td>
                <td>367</td>
                <td>41</td>
                <td>5 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивки на заказ</td>
                <td>912</td>
                <td>30</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Шеврон на заказ</td>
                <td>496</td>
                <td>54</td>
                <td>6 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивка на одежду на заказ</td>
                <td>301</td>
                <td>34</td>
                <td>7 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивка на заказ</td>
                <td>654</td>
                <td>36</td>
                <td>3 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                <tr>
                <td>Нашивки на одежду на заказ</td>
                <td>301</td>
                <td>36</td>
                <td>4 <span class="triangle"><img class="img" src="/templates/2023/digitalstrateg.ru/images/triangle_table_4.svg" alt="" title="" /></span></td>
                </tr>
                </tbody>
                </table>
        '''}
    ]
    

def permissions(form):
    pass
    form.ajax={
        'tbl1_load_template':ajax_tbl1_load_template,
        'tbl2_load_template':ajax_tbl2_load_template
    }
    
    #if 'cgi_params' in form.R:
    #    cgi_params = form.R['cgi_params']
    #    if 'load_template' in cgi_params:

events={
    'permissions':permissions
}