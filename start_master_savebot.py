
def get_list_zakaz (message_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')    
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,info,data_id from users where name = 'Заказ'"
    cursor.execute(sql)
    data = cursor.fetchall()
    list = []
    for rec in data: 
        id,name,info,data_id = rec.values()
        data_info = {'id_name':data_id}
        name_user_id = get_user_id (message_info,data_info)['user_id']
        data_info  = {'Заказ':id,'Список замены':['Биржа','Основная валюта','Второстепенная валюта'],'Список значения':['Объем валюты']} 
        data_zakaz = get_data_zakaz (message_info,data_info)
        data_zakaz['user_id'] = name_user_id
        if data_zakaz.setdefault('user_id','') != ''  and data_zakaz.setdefault('Биржа','') != '' and data_zakaz.setdefault('Основная валюта','') != '' and data_zakaz.setdefault('Второстепенная валюта','') != '' and data_zakaz.setdefault('Объем валюты','') != '':
            list.append ([data_zakaz.setdefault('user_id',''),data_zakaz.setdefault('Биржа',''),data_zakaz.setdefault('Основная валюта',''),data_zakaz.setdefault('Второстепенная валюта',''),data_zakaz['Объем валюты'][0]])
    return list

def get_user_id (message_info,data_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    id_name = data_info.setdefault('id_name','')    
    data_answer = {}    
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,info,data_id from users where id = {} limit 1".format (id_name)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,info,data_id = rec.values()        
        data_answer = {'user_id':info}    
    return data_answer

def message_send_list (message_info,data_info):  #### Печатаем список
    import iz_bot
    text       = data_info.setdefault('Текст','')
    key_array  = data_info.setdefault('Кнопки','')
    message_id = data_info.setdefault('Номер Сообшения',0)    
    if message_id == 0:
        send_data = {"Text":text,'Кнопки':key_array,'Тип кнопки':'Сообщение'} 
        iz_bot.send_message (message_info,send_data) 
    else:   
        send_data = {"Text":text,'Кнопки':key_array,'Тип кнопки':'Сообщение','Метод':'editMessageText'}     
        iz_bot.send_message (message_info,send_data) 

def messaage_in_list (message_info,data_info):   #### Выводит сообщение с кнопками
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    kolon      = data_info.setdefault('Колличество колонок',3) 
    
    ### Номер заказа который выбираем  
    zakaz      = data_info.setdefault('Заказ','')   
        
    ### Команда выполнения
    prit       = data_info.setdefault('Прификс','')
    param      = data_info.setdefault('Значение',0)    
        
    ### Запрос у базе
    sql        = data_info.setdefault('sql_main','')

    step_left = data_info.setdefault('Шаг влево',0) 
    step_prav = data_info.setdefault('Шаг вправо',0) 

    key_array = []
    
    print ('-----------------------------------------------------')
    print ('[sql]',sql)   
    
    db,cursor = iz_bot.connect (namebot)   
    cursor.execute(sql)
    results = cursor.fetchall()    
    polka = 0    
    list = [] 
     
    for row in results:
        id,info,reting,change = row.values()         
        list.append ([id,info,reting,change])
        
        if change != None:
            name = change
        else:
            name = info        
        
        
        if kolon == 1:
            key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            key1      = [key11,['',''],['','']]
            key_array.append(key1)
        if kolon == 2:    
            polka = polka + 1
            if polka == 1:
                key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            if polka == 2:    
                key12     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
                key1      = [key11,key12,['','']]
                key_array.append(key1)
                polka = 0                
        if kolon == 3:    
            polka = polka + 1
            if polka == 1:
                key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            if polka == 2:
                key12     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]                
            if polka == 3:    
                key13     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
                key1      = [key11,key12,key13]
                key_array.append(key1)
                polka = 0  

    if kolon == 3: 

        if polka == 1:  
            key1 = [key11,['',''],['','']]
            key_array.append(key1)            
        if polka == 2:  
            key1 = [key11,key12,['','']]        
            key_array.append(key1)
            
    key11     = ['Назад',iz_bot.build_jsom({"o":prit+'_left',"p":param,"z":zakaz,"s":step_left})]
    key12     = ['Цент',iz_bot.build_jsom( {"o":'ex_cent',"p":param,"z":zakaz, "s":0  })]
    key13     = ['Право',iz_bot.build_jsom({"o":prit+'_prav',"p":param,"z":zakaz, "s":step_prav})]
    
    key1      = [key11,key12,key13]
    key_array.append(key1)
            
                
            
            
    data_info['Кнопки'] = key_array       
    message_send_list (message_info,data_info)     
   
def input_message (message_info,data_info): 
    import iz_bot
    namebot    = message_info.setdefault('namebot','')      
    text       = data_info.setdefault('Текст','')
    message_id = data_info.setdefault('Номер Сообшения',0)  
    prit       = data_info.setdefault('Прификс','')    
    ask        = data_info.setdefault('Вопрос','') 
    zakaz      = data_info.setdefault('Заказ','')
    zamena    = data_info ['Замена']
    if ask == 'Да':
        send_data = {"Text":text} 
        iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',prit],['Номер заказа',zakaz]]
        iz_bot.user_save_data (message_info,save_data)
    else:
        send_data = {"Text":text,'Замена':zamena} 
        iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',''],['Номер заказа','']]
        iz_bot.user_save_data (message_info,save_data)    

def save_info_zakaz (message_info,data_info):
    import iz_bot
    namebot     = message_info.setdefault('namebot','') 
    name_z      = data_info.setdefault('Имя','')
    user_id     = message_info.setdefault('user_id','')
    id_z        = data_info.setdefault('Статус','')
    param_z     = data_info.setdefault('Значение','')
    
    lastid = 0
    if data_info.setdefault('Статус','')  == 'Новый':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,info from users where name = 'user_id' and info = '"+str(user_id)+"' limit 1"
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,name,info = rec.values()
            sql = "INSERT INTO users (`name`,`info`,`data_id`) VALUES ('Заказ','"+str(name_z)+"','"+str(id)+"')"
            cursor.execute(sql)
            db.commit()            
        db.close
        lastid = cursor.lastrowid
    else:
        db,cursor = iz_bot.connect (namebot)
        sql = "INSERT INTO users (`name`,`info`,`data_id`) VALUES ('"+str(name_z)+"','"+str(param_z)+"','"+str(id_z)+"')"
        cursor.execute(sql)
        db.commit()            
        db.close
    return lastid   
              
def get_data_zakaz (message_info,data_info):        
    import iz_bot
    namebot = message_info['namebot']
    user_id = message_info['user_id']
    data_id   = data_info ['Заказ']
    data_list = data_info ['Список замены']
    data_parm = data_info ['Список значения']
    db,cursor = iz_bot.connect (namebot)
    data_answer = {}   
    sql = "select id,name,info from users where data_id = '{}' ;".format (data_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row1 in results:
        id1,name1,info1 = row1.values()         
        data_answer[name1] = info1
    data_answer2 = {}
    
    print ('data_answer',data_answer)
    
    for line in data_list:
        data =  data_answer.setdefault(line,'')         
        sql = "select id,name,info from service where id = '{}' ;".format (data)
        cursor.execute(sql)
        results = cursor.fetchall()    
        id2 = 0
        for row2 in results:
            id2,name2,info2 = row2.values()
            data_answer2[line] = [info2,data]
        #if id2 == 0   
        #   data_answer[name1] = ['Сумма',info1]
    for line in data_parm:    
        data =  data_answer.setdefault(line,'')  
        data_answer2[line] = [data]                
    return data_answer2    

def set_name_key (message_info,namekey):
    import iz_bot
    info_data = {'Имя':namekey}
    info    = iz_bot.get_message(message_info,info_data)
    return_key = info.setdefault('Текст',info_data.setdefault('Имя',''))
    return return_key

def get_data_in_base (message_info,data_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    sql        = data_info.setdefault('sql','')
    nomer      = data_info.setdefault('nomer','')
    go         = data_info.setdefault('go','id')
    info = ''
    data = ''
    name = ''
    if go == 'prev':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,data,`text` from name_file where id < {} and status <> 'delete'  ORDER BY id DESC limit 1".format(nomer)
        print ('[sql 1]:',sql)
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,data,text = row.values() 
            if text == '':
                text = name
        info = data+name
    if go == 'next' or go == 'new':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,data,`text` from name_file where id > {}  and status <> 'delete'  ORDER BY id limit 1".format(nomer)   
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,data,text = row.values() 
            if text == '':
                text = name
        info = data+name           
    get_data_in_info = {'picture':info,'id':id,'text':text}    
    return get_data_in_info
            
def get_name_message (message_info,name_message): ##'Запрос геолокации
    import iz_bot
    info_data = {'Имя':name_message,'Сохранить':'Да'}
    data_message = iz_bot.get_message (message_info,info_data)
    print ('[data_message]',data_message)
    message_out    = data_message.setdefault ('Текст',name_message)
    return message_out
     
def foto_presentation (message_info,data_info):
    import iz_bot
    message_id = message_info.setdefault('message_id','')
    key_array = []
    picture_send_info = get_data_in_base (message_info,data_info)
    nomer     = picture_send_info['id']
    name1     = set_name_key (message_info,'Кнопка лево')
    name2     = set_name_key (message_info,'Кнопка право')    
    key11     = [name1,iz_bot.build_jsom({"o":'pict_l',"p":nomer})]
    key12     = [name2,iz_bot.build_jsom({"o":'pict_p',"p":nomer})]
    key1 = [key11,['',''],key12]
    key_array.append(key1)    
    key_array = []
    picture_send_info = get_data_in_base (message_info,data_info)
    nomer     = picture_send_info['id']
    name1     = set_name_key (message_info,'Кнопка лево')
    name2     = set_name_key (message_info,'Кнопка право')    
    key11     = [name1,iz_bot.build_jsom({"o":'pict_l',"p":nomer})]
    key12     = [name2,iz_bot.build_jsom({"o":'pict_p',"p":nomer})]
    key1 = [key11,['',''],key12]
    key_array.append(key1)    
    if data_info.setdefault('go','new') == 'new':
        send_data = {"Text":picture_send_info['text'],'Метод':'sendPhoto','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение'}
        answer = iz_bot.send_message (message_info,send_data)
    else:    
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageCaption','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageMedia','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageCaption','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
               
def delete_message (message_info,data_info): 
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    name = data_info['name']
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,message_id from message_log where name = '{}' and user_id = '{}' and status <> 'delete'".format (name,user_id,)
    cursor.execute(sql)
    data = cursor.fetchall()    
    for rec in data:
        id,message_id_del = rec.values()
        iz_bot.deleteMessage (message_info,message_id_del) 

    sql = "UPDATE message_log SET status = 'delete' WHERE name = '{}' and user_id = '{}' and status <> 'delete'".format (name,user_id,)
    cursor.execute(sql)
    db.commit()
        
def save_sql (message_info,sql_param,param):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "INSERT INTO data_sql (name,data) VALUES (%s,%s)".format ()
    sql_save = (sql_param,str(param))
    result = cursor.execute(sql,sql_save)
    db.commit()    
    lastid = cursor.lastrowid
    return lastid
    
def get_sql (message_info,param):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,data from data_sql where id = {}".format(param)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,param = rec.values() 
    return name,param  
       
       
def list_key (message_info,id_code,metka):
    import iz_bot
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = iz_bot.connect (namebot)
    sql,param_string    = get_sql (message_info,id_code)            
    param_string        = param_string.replace("'",'"')
    param               = json.loads(param_string)
    limit               = str(param.setdefault('limit',20))
    offet               = str(param.setdefault('offset',20))
    sql                 = sql.replace("#limit#",limit)
    sql                 = sql.replace("#offset#",offet)
    cursor.execute(sql)
    data = cursor.fetchall()
    print (data)
    key_array = []
    for rec in data: 
        id,info = rec.values()  
        info_exchange = info
        command =  iz_bot.build_jsom ({'o':metka,'s':id})
        key_array.append ([[info_exchange,command],['',''],['','']])  
    command =  iz_bot.build_jsom ({'o':'next','s':id_code})
    name_key     = set_name_key (message_info,'Кнопка далее')        
    key_array.append ([[name_key,command],['',''],['','']])         
    return key_array        
       
   
   
def get_data_id (message_info,namebase,nomer):
    import iz_bot
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = iz_bot.connect (namebot)
    element = {}
    sql = "select id,name,info,data_id from {} where data_id = {}".format(namebase,nomer)
    
    print ('[sql]',sql)
    
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,info,data_id = rec.values()
        element[name] = id
    return element    
     
def key_to_menu (element,metka):
    import iz_bot
    key_array = []
    for line in element:
        print ('[+] line:',line)        
        info_exchange = line + ' '+str(element[line])
        command =  iz_bot.build_jsom ({'o':metka,'s':str(element[line])})
        key_array.append ([[info_exchange,command],['',''],['','']])  
    return key_array       




   
def list_music (message_info,id_code,command):
    namebot    = message_info.setdefault('namebot','')
    import iz_bot
    import json
    db,cursor = iz_bot.connect (namebot)
    sql,param_string = get_sql (message_info,id_code)            
    param_string = param_string.replace("'",'"')
    print ('[+] param_string',param_string)
    param = json.loads(param_string)
    limit = str(param.setdefault('limit',20))
    offet = str(param.setdefault('offset',20))
    if command == 'next':
        offet = str(int(offet) + int(limit))
        param = {'limit':int(limit),'offset':int(offet)}
        id_code = save_sql (message_info,sql,param)
    sql = sql.replace("#limit#",limit)
    sql = sql.replace("#offset#",offet)
    cursor.execute(sql)
    data = cursor.fetchall()
    key_array = []
    for rec in data: 
        id,info = rec.values()  
        info_exchange = info
        print ('[Композиция]',info)
        command =  iz_bot.build_jsom ({'o':'list','s':id})
        key_array.append ([[info_exchange,command],['',''],['','']])  
    command =  iz_bot.build_jsom ({'o':'next','s':id_code})
    name_key     = set_name_key (message_info,'Кнопка далее')        
    key_array.append ([[name_key,command],['',''],['','']])         
    return key_array       
   
def get_info_bot_in_token (token):
    import requests
    import json        
    import time
    
    url = 'https://api.telegram.org/bot'+str(token)+'/getMe'
    answer = requests.get(url) 
    #print ('    [answer]',answer.text)
    parsed_string = json.loads(answer.text)
    print ('    [+] parsed_string',parsed_string)   
    return parsed_string
   
def install_web_hook (token,namebot): 
    import iz_bot    
    import requests
    import json
    setting = iz_bot.get_setting_prog ('main314_bot')
    #db,cursor = iz_bot.connect (namebot)
    #sql_main = "select id,name,info from setting where name = '{}' ".format ('nerok')
    #cursor_main.execute(sql_main)
    #data_main = cursor_main.fetchall()
    nerok = setting['nerok']
    #for rec_main in data_main: 
    #    id,info,nerok = rec_main.values()
    #nerok  = "https://5060-46-191-186-3.ngrok-free.app"
    url = 'https://api.telegram.org/bot'+str(token)+'/setWebhook?url='+nerok+'/telegram/3141/'+namebot+'/'
    answer = requests.get(url)                                
    print ('    [+] Постановка Webhook: ',answer.text)   
    print ('    [+] Постановка url: ',url)        
    parsed_string = json.loads(answer.text)
    description = ''
    ok = ''
    try:
        ok                          =  (parsed_string['ok'])
        result                      =  (parsed_string['result'])
        description                 =  (parsed_string['description'])
    except Exception as e:
        pass 
    
    return ok    
   
def save_name_bot (token,username,user_id):
    import iz_bot
    db,cursor = iz_bot.connect_postgres () 
    sql = "select id,name from main314_bot_bots where name = '{}' limit 1".format (username)
    cursor.execute(sql)
    data = cursor.fetchall()    
    id = 0
    for rec in data: 
        id,name = rec
        print ('    [+] Токен обнаружен в базе данных',id,name)        
    if  id == 0:
        print ('    [+] Бот в базе данных не обнаружен. Записываем')
        sql = "INSERT INTO main314_bot_bots (name,status,token,user_id) VALUES ('{}','','{}','{}')".format (username,token,user_id)
        cursor.execute(sql)
        db.commit()    
   
def create_base (username):
    #import iz_bot
    
    import pymysql
    db_main = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database='bot_main',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cursor_main = db_main.cursor() 
    if 1==1:
        if 1==1:
            sql_main = 'CREATE DATABASE '+str(username)
            try:
                cursor_main.execute(sql_main)
            except Exception as e:
                print ('    [+] Ошибка создания базы данных:',e)    
            print ('    [+] Создаем таблицу')            
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql_main = "select id,name,`sql` from create_base where `type` = 'telegram' ".format ()
            cursor_main.execute(sql_main)
            data_main = cursor_main.fetchall()            
            for rec_main in data_main: 
                id,name,sql = rec_main.values()
                print ('    [+] Создаем таблицы:',id,name)
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print ('    [+] Ошибка создания Таблицы:',e)  
   
def start_prog (message_info):
    import iz_bot
    #### Загрузка всех необходимых данных
    message_in = message_info.setdefault('message_in','')
    message_id = message_info.setdefault('message_id','')
    callback   = message_info.setdefault('callback','')
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    photo      = message_info.setdefault('photo','')
    document  = message_info.setdefault('document','')
    get_data = {}
    status_input = iz_bot.user_get_data (message_info,get_data)    ### Получение информации по пользователю
    setting_bot  = iz_bot.get_setting (message_info)               ### Получение информации по боту
    for line in status_input:
        print ('        [+]',line,'-',status_input[line])
    status     = status_input.setdefault('status','')        
    if document != '':
        print ('[+] Получен документ через бота')
        setting = iz_bot.get_setting (message_info)
        token    = setting.setdefault ('Токен','')
        from telebot import TeleBot 
        bot = TeleBot(token)            
        fileID = document['file_id']    
        file_info = bot.get_file(fileID)
        print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = "/home/main314_bot/Main/Server/files/main314_bot/"+str(document['file_name'])
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
            name = file_info.file_path
        print ('[+] Получена новая файл') 
        send_data = {'Text':'Файл сохранен на компьютере'}
        iz_bot.send_message (message_info,send_data)
        doc = open(filename, 'rb')
        bot.send_document(user_id, doc)
        send_data = {'Text':'Файл Всем отправлен'}
        iz_bot.send_message (message_info,send_data)
        #binaryData = ''
        #with open(filename, 'rb') as file:
        #    binaryData = file.read()
        #db,cursor = iz_bot.connect (namebot)
        #sql_insert_blob_query = "INSERT INTO files (name, photo) VALUES (%s,%s)".format ( )
        #insert_blob_tuple = (filename,binaryData)
        #result = cursor.execute(sql_insert_blob_query,insert_blob_tuple)
        #db.commit()
    
    
    if message_in   == '/message':
        param = {'limit':10,'offset':0}
        sql = "select id,info from message where name = 'Имя' limit #offset#,#limit#"
        id_code = save_sql (message_info,sql,param)
        key_array = list_key (message_info,id_code,'message')
        send_data = {"Text":'Список выходных сообщений','Кнопки':key_array,'Тип кнопки':'Сообщение'}
        answer = iz_bot.send_message (message_info,send_data)     
    
    
    ### Процедура загрузки фотографии в базу данных
    if photo != '':
        for line in photo:
            print ('[+] Присланная фотография:',line)
            from telebot import TeleBot 
            token    = setting_bot.setdefault ('Токен','')
            #bot = TeleBot("5713227819:AAGE5XdsgHs_YHNaOpwcxHXLT9pL9Hkpvok")
            bot = TeleBot(token)            
            fileID = line['file_id']    
            file_info = bot.get_file(fileID)
            print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = "/var/www/html/pict_bot/pict_"+str(fileID)+".jpg"
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
            name = file_info.file_path
        print ('[+] Получена новая фотография')               
        binaryData = ''
        with open(filename, 'rb') as file:
            binaryData = file.read()
        db,cursor = iz_bot.connect (namebot)
        sql_insert_blob_query = "INSERT INTO files (name, photo) VALUES (%s,%s)".format ( )
        insert_blob_tuple = (filename,binaryData)
        result = cursor.execute(sql_insert_blob_query,insert_blob_tuple)
        db.commit()  

##################################  начало 93472672893 Вставка администратора ##################################
    if callback.find ('ig_') != -1: 
        print ('[+] Модуль обработки ответа администратора')
        word = callback.replace("ig_","")  
        save_data = [['Игнор',"Да"]]
        message_info['user_id'] = word
        iz_bot.user_save_data (message_info,save_data) 
        print ('    [+] Сохранение информации в базе:',save_data,message_info)    
        message_info['user_id'] = user_id
        send_data = {"Text":'Замена сообщения администратора','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data) 
        
    if callback.find ('za_') != -1: 
        print ('[+] Модуль обработки ответа администратора')
        word = callback.replace("za_","")  
        save_data = [['Заказ',"Да"]]
        message_info['user_id'] = word
        iz_bot.user_save_data (message_info,save_data)        
        message_info['user_id'] = user_id
        send_data = {"Text":'Замена сообщения менаджера','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)    

    if callback.find ('del_') != -1: 
        print ('[+] Модуль обработки ответа администратора')
        word = callback.replace("del_","")

        db,cursor = iz_bot.connect (namebot)
        sql = "select id,message_id from message_id where status = '' and name = 'Информирование' and data_id = '{}' and user_id = '{}' ".format(word,user_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,message_id = rec.values()  
            iz_bot.deleteMessage (message_info,message_id)
            sql = "UPDATE message_id SET status = '{}' WHERE id = {}".format('delete',id)
            cursor.execute(sql)
            db.commit()

    if message_in == '/intel':
        import random
        import time
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name01,name02,name03,name04 from intell where 1=1 ".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        lb01 = []
        lb02 = []
        lb03 = []
        lb04 = []
        for rec in data: 
            id,name01,name02,name03,name04 = rec.values()  
            lb01.append (name01)
            lb02.append (name02)
            lb03.append (name03)
            lb04.append (name04)
        random.shuffle(lb02)    
        random.shuffle(lb03)    
        random.shuffle(lb04)    
        if 1==1:
            slpv1 =  lb01[0] +' '+ lb02[0] +' '+ lb03[0] +' '+ lb04[0]
            slpv2 =  lb01[1] +' '+ lb02[1] +' '+ lb03[1] +' '+ lb04[1]        
            slpv3 =  lb01[2] +' '+ lb02[2] +' '+ lb03[2] +' '+ lb04[2]        
            slpv4 =  lb01[3] +' '+ lb02[3] +' '+ lb03[3] +' '+ lb04[3]        
        send_data = {"Text":'##Text##','Замена':[['##Text##',str(slpv1)]]}
        answer = iz_bot.send_message (message_info,send_data)        
        time.sleep (1)    
        send_data = {"Text":'##Text##','Замена':[['##Text##',str(slpv2)]]}
        answer = iz_bot.send_message (message_info,send_data)        
        time.sleep (1)    
        send_data = {"Text":'##Text##','Замена':[['##Text##',str(slpv3)]]}
        answer = iz_bot.send_message (message_info,send_data)        
        time.sleep (1)    
        send_data = {"Text":'##Text##','Замена':[['##Text##',str(slpv4)]]}
        answer = iz_bot.send_message (message_info,send_data)        
        
##################################  конец 93472672893 Вставка администратора ##################################) 

    if message_in == 'Coin Farmer' or message_in == '/Farmer':
        label_send = True
        import iz_game
        iz_game.game_farmer (message_info,"start",'')
        message_in = ''
        callback   = ''

    if callback.find ('game_farmer_') != -1:
        label_send = True
        import iz_game
        iz_game.game_farmer (message_info,callback,'')
        message_in = ''
        callback   = ''
        
    if message_in   == '/test2':    
        data_info = {'nomer':0,'go':'new'}
        foto_presentation (message_info,data_info)    
        
    if message_in.find ('/start') != -1 or message_in == '/help' or  message_in == 'Вопрос':
        status = ''
        if setting_bot.setdefault('Вывод начальной картинки','') == 'Да':
            send_data = {"Text":'Идет загрузка'}
            answer = iz_bot.send_message (message_info,send_data)
            message_del_id   = answer['result']['message_id']

        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)  
        send_data = {"Text":'/start'}
        answer = iz_bot.send_message (message_info,send_data)
        if setting_bot.setdefault('Вывод начальной картинки','') == 'Да':
            iz_bot.deleteMessage (message_info,message_del_id)    

        if message_in.find ('/start ') != -1:
            word = message_in.replace("/start ","")
            if word.find ('site') != -1:
                print ('[+] Переход по реферальной ссылке с сайта')
                word = word.replace("site","")
                db,cursor = iz_bot.connect (namebot)
                send_data = {"Text":'Переход по реферальной ссылки сайта'}
                answer = iz_bot.send_message (message_info,send_data)  
                sql = "INSERT INTO site_task (name,info,user_id,data_id) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Новый клиент',str(word),user_id,0)
                cursor.execute(sql,sql_save)
                db.commit()
            else:
                db,cursor = iz_bot.connect (namebot)
                sql = "select id,`info` from `order` where id = {}".format(word)
                cursor.execute(sql)
                data = cursor.fetchall()
                for rec in data:
                    id,name = rec.values()
                    send_data = {"Text":name}
                    answer = iz_bot.send_message (message_info,send_data)

    if message_in   == '/test':    
        param = {'limit':10,'offset':0}
        sql = "select id,info from service where name = 'Имя' ORDER BY id DESC limit #offset#,#limit#"
        id_code = save_sql (message_info,sql,param)
        key_array = list_music (message_info,id_code,'new')
        send_data = {"Text":'Список команд бота','Кнопки':key_array,'Тип кнопки':'Сообщение'}
        answer = iz_bot.send_message (message_info,send_data)  
        
    if callback.find ('i_') != -1:
        import json
        import requests
        import datetime
        json_string  = iz_bot.change_back(callback.replace('i_',''))
        data_json = json.loads(json_string)
        operation = data_json.setdefault('o','')
        #nomer     = data_json.setdefault('p','')        
        nomer     = data_json.setdefault('s','') 
        print ('    [+] operation:',operation)    
        print ('    [+] nomer    :',nomer)     
        date      = data_json.setdefault('d','') 
        now = datetime.datetime.now()
        current_date_string = now.strftime('%d.%m.%y') 
        print ('    [+] current_date :',current_date_string)         
    
    
    
        if operation == 'message':  ## Основное
            element   = get_data_id (message_info,'message',nomer)
            key_array = key_to_menu (element,'message2')
            print ('key_array',key_array)
            send_data = {"Text":'Показать элементы','Кнопки':key_array,'Тип кнопки':'Сообщение'}
            answer = iz_bot.send_message (message_info,send_data)
            
        if operation == 'message2':  ## Основное    %%Ответ%%
            
            db,cursor = iz_bot.connect (namebot)
            
            sql = "select id,name,info from message where id = {}".format (nomer)
            cursor.execute(sql)
            data = cursor.fetchall()    
            id_s = 0
            text       = ''
            for rec in data: 
                id,name,info = rec.values()
                text = info
            

            zamena     = [['%%Ответ%%',text]]
            send_data = {"Text":'Изменить элемент сообщение','Замена':zamena}
            answer = iz_bot.send_message (message_info,send_data)
            save_data = [['Номер параметра замены',str(nomer)],['status','Ввод нового параметра сообщения']]
            iz_bot.user_save_data (message_info,save_data) 
    
    
    
    
        if operation == 'pict_l': 
            data_info = {'nomer':nomer,'go':'prev'}
            foto_presentation (message_info,data_info)
            
        if operation == 'pict_p':            
            data_info = {'nomer':nomer,'go':'next'}
            foto_presentation (message_info,data_info)
   

        if operation == 'next':    
            id_code = nomer
            key_array = list_music (message_info,id_code,'next')
            send_data = {"Text":'Список песен 2','Кнопки':key_array,'Тип кнопки':'Сообщение','Метод':'editMessageText','message_id':message_id}
            answer = iz_bot.send_message (message_info,send_data)  
            
        if operation == 'list':
            send_data = {'Text':'Отправка файлов'}
            iz_bot.send_message (message_info,send_data)               




    if status == 'Ввод нового параметра сообщения': 
        save_data = [['Номер параметра замены',''],['status','']]
        iz_bot.user_save_data (message_info,save_data) 
        id_message = status_input['Номер параметра замены']
        send_data = {"Text":'Замена в параметре сообщения'}
        answer = iz_bot.send_message (message_info,send_data)
        
        db,cursor = iz_bot.connect (namebot)
        sql = "UPDATE message SET info = %s WHERE id = %s ".format ()
        sql_save = (message_in,status_input['Номер параметра замены'])
        cursor.execute(sql,sql_save)        
        db.commit()






    if message_in == '/location':
        from telebot import TeleBot
        from telebot import types
        #bot = TeleBot("469097102:AAEdz6SX6OkdGjufUBri0BSQmr4bBEh7Vrk")        
        setting = iz_bot.get_setting (message_info)
        token    = setting.setdefault ('Токен','')
        bot = TeleBot(token)
        name_key1 = get_name_message (message_info,'Отправить номер телефона')
        name_key2 = get_name_message (message_info,'Отправить местоположение')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text=name_key1, request_contact=True)
        button_geo = types.KeyboardButton(text=name_key2, request_location=True)
        keyboard.add(button_phone, button_geo)
        message_out = get_name_message (message_info,'Запрос геолокации')
        bot.send_message(user_id,message_out, reply_markup=keyboard)   
            
    if message_in == '/time_zona':
        user_id    = message_info.setdefault('user_id','') 
        namebot    = message_info.setdefault('namebot','')    
        send_data = {"Text":'Укажите Ваш город'}        
        answer = iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',"Ввод города"],['Город','']]
        iz_bot.user_save_data (message_info,save_data)  
        status = ''

    if status_input.setdefault('Статус ввода','') == 'Ввод города':
        import iz_bot        
        import geopy
        from tzwhere import tzwhere
        import datetime
        import pytz      
 
    if callback == 'save_message':
        send_data = {"Text":'Введите текст сообщения','Метод':'editMessageText'}        
        answer = iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',"Создание нового сообшения"]]
        iz_bot.user_save_data (message_info,save_data)        

    if status_input.setdefault('Статус ввода','') == 'Создание нового сообшения':
        send_data = {"Text":'Сообшение создано'}        
        answer = iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)  
        db,cursor = iz_bot.connect (namebot)
        sql = "INSERT INTO message (`data_id`,`data_name`,`info`,`name`) VALUES (0,'','"+str(status_input['Новое сообшение'])+"','Имя')"
        cursor.execute(sql)
        db.commit()    
        lastid = cursor.lastrowid        
        sql = "INSERT INTO message (`data_id`,`data_name`,`info`,`name`) VALUES ({},'','{}','Текст')".format (lastid,message_in)
        cursor.execute(sql)
        db.commit()    
        lastid = cursor.lastrowid        
        
    global_prif = "ex_"
    if message_in == '/status_2' or callback.find ('ex_') != -1 or status_input.setdefault('Статус ввода','').find (global_prif) != -1:  
        import code_shkepeerbot
        if message_in == '/status_2':
            message_info['message_in'] = '➕ Добавить'
        code_shkepeerbot.code03 (message_info,status_input,global_prif)       
        
    if message_in.find ('/edit_message_nomer_') != -1:
        import re        
        #word = re.sub('/edit_message_nomer_', '',message_in)
        #message_in = '/edit_message_nomer_75'
        word = re.sub('/edit_message_nomer_', '', message_in)
        send_data = {"Text":"Редактирование сообщения","Замена":[['%id%',word],['%info%',"---------"]]}        
        iz_bot.send_message (message_info,send_data)   
        save_data = [['Статус ввода',"Ввод нового сообщения"],['Номер заменяемого сообщения',word]]
        iz_bot.user_save_data (message_info,save_data)         

    if message_in == '/newbot' and 1==2:
        key_array = [[['Ввести токен','Ввести токен'],['',''],['','']],[['Выбрать шаблон','Выбрать шаблон'],['',''],['','']]]
        send_data = {"Text":'Создать телеграмм бота','Кнопки':key_array,'Тип кнопки':'Сообщение'}
        answer = iz_bot.send_message (message_info,send_data)   

    if message_in == 'Ваш ID код':
        import code_main314_bot
        code_main314_bot.send_user_id  (message_info)

    if message_in == 'Получить пароль':
        import code_main314_bot    
        code_main314_bot.get_password (message_info)
 
    if status_input.setdefault('Статус ввода','')  == 'Ввод нового сообщения':
        db,cursor = iz_bot.connect (namebot)
        save_data = [['Статус ввода',''],['Номер заменяемого сообщения','']]
        iz_bot.user_save_data (message_info,save_data)
        nomer_id = status_input.setdefault('Номер заменяемого сообщения','')
        sql = "UPDATE message SET info = '"+message_in+"' WHERE id = "+str(nomer_id)+""
        cursor.execute(sql)
        db.commit()
        send_data = {"Text":"Редактирование сообщения завершено"}        
        iz_bot.send_message (message_info,send_data) 

    if status_input.setdefault('Статус ввода','')  == 'Ввод куска текста':
        send_data = {"Text":'Поиск текста'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Текст поиска',message_in]]
        iz_bot.user_save_data (message_info,save_data)
        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)        
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,info,data_id from message where name = 'Текст' and info like '%"+str(message_in)+"%' limit 5"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name,info,data_id = rec.values()
            sql = "select id,name,info from message where name = 'Имя' and id = '"+str(data_id)+"' limit 1"
            cursor.execute(sql)
            data = cursor.fetchall()
            info_v = ''
            for rec_v in data: 
                id_v,name_v,info_v = rec_v.values()
            send_data = {"Text":"Номер сообшения","Замена":[['%id%',id],['%name%',info_v]]}        
            iz_bot.send_message (message_info,send_data)          
            send_data = {"Text":info,'Запись в базу':'Не записывать'}        
            iz_bot.send_message (message_info,send_data)
        
    if status_input.setdefault('Статус ввода','') == 'Ввод сообщения':
        send_data = {"Text":'Сообщение сохранено'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Сообщение для отправки',message_in]]
        iz_bot.user_save_data (message_info,save_data)
        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)

    if message_in.find ('/editmessage') != -1:
        send_data = {"Text":'Кусок текста бота'}        
        iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',"Ввод куска текста"]]
        iz_bot.user_save_data (message_info,save_data)

    if callback.find ('info') != -1:
        import json
        json_string  = iz_bot.change_back(callback.replace('info_',''))
        data_json = json.loads(json_string)
        operation = data_json.setdefault('o','')
        param     = data_json.setdefault('p','')        
        print ('    [+] operation:',operation)    
        print ('    [+] param    :',param)
        if operation == 'task':    
            db,cursor = iz_bot.connect (namebot)
            sql = "select id,info from users where name = 'user_id' "
            cursor.execute(sql)
            results = cursor.fetchall()  
            nomer = 0 
            for row in results:
                nomer = nomer + 1
                id,info = row.values() 
                send_data = {'Text':'Сообщение отправляется'}
                iz_bot.send_message (message_info,send_data)
                send_data = {'Text':status_input.setdefault('Сообщение для отправки',''),'Запись в базу':'Не записывать','user_id':info}        
                iz_bot.send_message (message_info,send_data) 
                save_data = {'id_task':1,'Параметр':[['Всего',str(nomer)],['Удачных',str(nomer)]]}
                iz_bot.task_save_data (message_info,save_data)

    if message_in == '/sendmessage':
        nomer = 0
        key_array = []
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,info from task where name = 'Имя' "
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            nomer = nomer + 1
            id,name,info = row.values() 
            key11     = [info,iz_bot.build_jsom({"o":"task","p":id})]                      #### 
            key1      = [key11,['',''],['','']]
            key_array.append(key1) 
        send_data = {"Text":'Подготовка к отправке','Кнопки':key_array,'Тип кнопки':'Сообщение'} 
        iz_bot.send_message (message_info,send_data)         

    if message_in == '/report_messsge':   
        get_data = {'id_task':"1"} 
        data_answer = iz_bot.task_get_data (message_info,get_data)
        print ('data_answer',data_answer)
        send_data = {"Text":'Отчет отправленных сообщений','Замена':[['%Всего%',data_answer['Всего']],['%Удачных%',data_answer['Удачных']]]}        
        iz_bot.send_message (message_info,send_data)         

    if message_in == '/in_message':        
        send_data = {"Text":'Введите сообщение для отправки'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Статус ввода',"Ввод сообщения"]]
        iz_bot.user_save_data (message_info,save_data)

    if message_in == '/status':
        send_data = {"Text":'Статус телеграмм бота'}        
        iz_bot.send_message (message_info,send_data) 

    if message_in == '/send':
        send_data = {"Text":'Отправить сообшение'}        
        iz_bot.send_message (message_info,send_data) 
    
    if message_in == '/stop':
        send_data = {"Text":'Админка отключна'}        
        iz_bot.send_message (message_info,send_data) 
        
    if message_in == '/stat':
        send_data = {"Text":'Статистика бота'}        
        iz_bot.send_message (message_info,send_data)     
        
    if message_in == '/server':
        send_data = {"Text":'Информация о работе сервера'}        
        iz_bot.send_message (message_info,send_data)     
     
    if message_in == '/help':
        send_data = {"Text":'Помощь'}        
        iz_bot.send_message (message_info,send_data)      

    if message_in == '/trafic':  
        import code_main314_bot   
        code_main314_bot.trafic (message_info)

    if 1==1:
        import code_main314_bot   
        code_main314_bot.nomer_avto (message_info)

    if message_in == '/memory': 
        import psutil
        hdd = psutil.disk_usage('/')
        total   = hdd.total   #)      #/ (2**30))
        used    = hdd.used    #)      #/ (2**30))
        free    = hdd.free    #)      #/ (2**30))
        percent = hdd.percent #)      #/ (2**30))
        send_data = {"Text":'Информация о системе','Замена':[['%percent%',percent]]}
        iz_bot.send_message (message_info,send_data)      

    if message_in == '/add_info_1': 
        ### Переносим настройки     
        import pymysql
        username = status_input.setdefault('namebot','')  
        token    = status_input.setdefault('Токен','')    
        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username.replace("@","") ,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()      
        sql = "INSERT INTO setting (`name`,`info`,`data_id`,status) VALUES ( '{}', '{}',{},'')".format ('Токен',token,0)
        cursor.execute(sql)
        db.commit()   
        lastid = cursor.lastrowid   
    
        ### Переносим настройки     
        import pymysql 
        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = 'bot_main',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()      
        sql = "INSERT INTO users (`name`,`namebot`,`password`,status) VALUES ( '{}', '{}',{},'')".format (user_id,str(username),'1111','')
        cursor.execute(sql)
        db.commit()   
        lastid = cursor.lastrowid   
    

        print ('[+] Приступаем к заполнению данных')     
        print ('    [+] Пользователи')
        print ('    [+] Сообщения')
        import pymysql
        username1 = 'main314_bot'   
        print ('[+] Создаем таблицу') 
        username2 = username.replace("@","") 
        print ('username2',username2)

        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username2,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()  
        import pymysql
        
        
        db1 = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username1,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor1 = db1.cursor()  
        sql = "select id,name,info,data_id,status from message where data_id = 22".format ()
        print ('sql',sql)
        cursor1.execute(sql)
        data1 = cursor1.fetchall()    
        id = 0
        for rec1 in data1: 
            id,name,info,data_id,status = rec1.values()
            print ('[+]',id,name,info,data_id,status)   
            sql = "INSERT INTO message (`id`,`name`,`info`,`data_id`,`status`) VALUES ( {}, '{}','{}',{},'{}')".format (id,name,info,data_id,status)
            cursor.execute(sql)
            db.commit()   
            lastid = cursor.lastrowid   
        import pymysql
        username1 = 'main314_bot'     
        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username2,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()  
        import pymysql
        db1 = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = username1,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor1 = db1.cursor()  
        sql = "select id,name,info,data_id,status from menu where data_id = 4".format ()
        print ('sql',sql)
        cursor1.execute(sql)
        data1 = cursor1.fetchall()    
        id = 0
        for rec1 in data1: 
            id,name,info,data_id,status = rec1.values()
            print ('[+]',id,name,info,data_id,status)   
            sql = "INSERT INTO menu (`id`,`name`,`info`,`data_id`,`status`) VALUES ( {}, '{}','{}',{},'{}')".format (id,name,info,data_id,status)
            print ('sql',sql)
            cursor.execute(sql)
            db.commit()   
            lastid = cursor.lastrowid   

    if message_in == '/token' or message_in == '/newbot' :
        status    = ''
        send_data = {"Text":'Введите Ваш токен'}        
        iz_bot.send_message (message_info,send_data) 
        save_data = [['status',"Ввод токена"]]
        iz_bot.user_save_data (message_info,save_data)
        iz_bot.deleteMessage (message_info,message_id)
        delete_message (message_info,{'name':'Проверка токена'}) 
        delete_message (message_info,{'name':'Токен не прошел проверку'}) 
        
    if status == 'Ввод токена':   
        send_data = {"Text":'Проверка токена'}        
        iz_bot.send_message (message_info,send_data) 
        iz_bot.deleteMessage (message_info,message_id)
        delete_message (message_info,{'name':'Регистрация нового бота по токену'}) 
        import pymysql
        db_main = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database='bot_main',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cursor_main = db_main.cursor() 
        save_data = [['Статус ввода',""],['Токен',message_in]]
        iz_bot.user_save_data (message_info,save_data)
        token =  message_in
        
        #token = message_in
        parsed_string = get_info_bot_in_token (token)
        
       
        if parsed_string['ok'] == False:
            send_data = {"Text":'Токен не прошел проверку'}        
            iz_bot.send_message (message_info,send_data) 
            delete_message (message_info,{'name':'Проверка токена'})
            save_data = [['status',""]]
            iz_bot.user_save_data (message_info,save_data)
            status    = ''
        
        if parsed_string['ok'] == True:
            first_name = parsed_string['result']['first_name']
            username   = parsed_string['result']['username']
            namebot    = '@'+username
            save_data = [['namebot','@'+username]]
            iz_bot.user_save_data (message_info,save_data)
            send_data = {"Text":'Результат проверки','Замена':[['%first_name%',first_name],['%username%',username]]}        
            iz_bot.send_message (message_info,send_data)
            delete_message (message_info,{'name':'Проверка токена'})
            install_web_hook (token,namebot)
            save_name_bot (token,username,user_id)
            print ('    [+] Прописываеи нового пользователя ')   
            print ('    [+] Копируем файлы')
            print ('    [+] Создаем базу')        
            






            create_base (username)












                    
            print ('    [+] Приступаем к заполнению данных: Message')  
            sql_main = "select id,data_id,info,name,status from message where `type` = 'Main telegram' ".format ()    
            cursor_main.execute(sql_main)
            data_main = cursor_main.fetchall()    
            for rec_main in data_main: 
                id,data_id,info,name,status = rec_main.values()
                db,cursor = iz_bot.connect (namebot)
                sql = "INSERT INTO message (id,data_id,info,name,status) VALUES (%s,%s,%s,%s,%s)"
                sql_save = (id,data_id,info,name,status)
                try:
                    cursor.execute(sql,sql_save)
                except Exception as e:
                    print ('    [+] Ошибка записи информации message:',e)                 
                db.commit() 
            print ('    [+] Приступаем к заполнению данных: Menu')          
            sql_main = "select id,data_id,info,name,status from menu where `type` = 'Main telegram' ".format ()    
            cursor_main.execute(sql_main)
            data_main = cursor_main.fetchall()    
            for rec_main in data_main: 
                id,data_id,info,name,status = rec_main.values()
                db,cursor = iz_bot.connect (namebot)
                sql = "INSERT INTO menu (id,data_id,info,name,status) VALUES (%s,%s,%s,%s,%s)"
                sql_save = (id,data_id,info,name,status)
                try:
                    cursor.execute(sql,sql_save)
                except Exception as e:
                    print ('    [+] Ошибка записи информации menu:',e)      
                db.commit()     
            print ('    [+] Приступаем к заполнению данных: файлов')          
            sql_main = "select id,data,name,status,`text` from name_file where `type` = 'Main telegram' ".format ()    
            cursor_main.execute(sql_main)
            data_main = cursor_main.fetchall()    
            for rec_main in data_main: 
                id,data,name,status,text = rec_main.values()
                db,cursor = iz_bot.connect (namebot)
                sql = "INSERT INTO name_file (id,data,name,status,`text`) VALUES (%s,%s,%s,%s,%s)"
                sql_save = (id,data,name,status,text)
                try:
                    cursor.execute(sql,sql_save)
                except Exception as e:
                    print ('    [+] Ошибка записи информации menu:',e)      
                db.commit()     
                
            print ('    [+] Приступаем к заполнению данных: настроек')  
            db,cursor = iz_bot.connect (namebot)            
            sql = "INSERT INTO setting (`name`,`info`,`data_id`,status) VALUES ( '{}', '{}',{},'')".format ('Токен',token,0)
            cursor.execute(sql)
            db.commit()   
            lastid = cursor.lastrowid                  

            print ('[+] Прописываем нового пользователя ')     ####   !!!!!!!!!!!!!!!!!!!!!!!!
            print ('[+] Копируем файл бота')     ####   !!!!!!!!!!!!!!!!!!!!!!!!
            import shutil
            shutil.copyfile('start_main314_bot.py', 'start_'+username+'.py')

            send_data = {"Text":'Телеграмм бот создан','Замена':[['#Имябота#','@'+username]]}        
            iz_bot.send_message (message_info,send_data)
            
            delete_message (message_info,{'name':'Подключени к серверу'})
            
            save_data = [['status',""]]
            iz_bot.user_save_data (message_info,save_data)
