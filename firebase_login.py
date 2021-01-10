# -*- coding: utf-8 -*-
# Seule le bibliothèque pyrebase4 suivante
# peut fonctionner
# 只有以下的 pyrebase4 的库可以正常运作
# https://github.com/nhorvath/Pyrebase4
# pip install pyrebase4
import pyrebase 
import PySimpleGUI as sg
import binascii
import pickle
import sys
import time

# config = {
#   "apiKey": "apiKey",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://fir-rtc-aff50-default-rtdb.firebaseio.com/",
#   "storageBucket": "projectId.appspot.com"
# }

def firebaseLogin():
    firebaseConfig = {
      "apiKey": "AIzaSyB4KpNt_TjCoaDx4iA4KP80Ompm4cc1ymk",
      "authDomain": "fir-rtc-aff50.firebaseapp.com",
      "databaseURL": "https://fir-rtc-aff50-default-rtdb.firebaseio.com/",
      "projectId": "fir-rtc-aff50",
      "storageBucket": "fir-rtc-aff50.appspot.com",
      "messagingSenderId": "900710198529",
      "appId": "1:900710198529:web:0ec5f5be44756ef2e9ff00",
      "measurementId": "G-267VZRPMW4"
    };
    firebase = pyrebase.initialize_app(firebaseConfig)
    # enregistrer des données 保存数据
    pickle.dump(firebase,open('firebase_info.txt','wb'))
    
    sg.ChangeLookAndFeel('Reddit')
    layout = 	[
    		[sg.Text('Connectez-vous à votre compte', size=(30,1), font=('Helvetica',12),text_color='#1c86ee' ,justification='left'),\
                 sg.Image(r'images\nac-logo.png',key = "_WEATHER_IMG_",size=(100, 50))],
    		[sg.Text('Email'), sg.In(size=(40,1), key='_USER_EMAIL_')],
    		[sg.Text('Password'), sg.In(size=(40,1), key='_USER_PASSWORD_')],
    		[sg.OK(), sg.Cancel()]
    			]
    win = sg.Window('Test vidéo pour YOLOv4 - NAC',
    				default_element_size=(21,1),
    				text_justification='left',
    				auto_size_text=False).Layout(layout)
    event, values = win.Read()
    if event is None or event =='Cancel':
    	sys.exit()
    
    UserEmail = values['_USER_EMAIL_']
    UserPassword = values['_USER_PASSWORD_']
    
    # Obtenir une référence au service d'auth
    # 获取对用户验证的引用
    auth = firebase.auth()
    
    try:
        # Connexion 登录
        user = auth.sign_in_with_email_and_password(UserEmail, UserPassword)
        sg.popup('登录成功！欢迎', UserEmail)
        pickle.dump(user,open('user_info.txt','wb'))
        userUniqueId = UserEmail.replace("@","__").replace(".","_")
        pickle.dump(userUniqueId,open('user_id.txt','wb'))        
    except:
        sg.popup('发生了一些错误，可能是用户名/密码错误！')
    
    str_16 = binascii.b2a_hex(UserEmail.encode('utf-8'))
    print(str_16)
    
    win.Close()
    

def firebaseUploadData(targetPositionObject,timeStamp):
    # Lire des données 读取数据
    firebase = pickle.load(open('firebase_info.txt','rb'))
    user = pickle.load(open('user_info.txt','rb'))
    # 测试设计数据结构（未完成）
    # https://firebase.google.com/docs/database/web/structure-data?authuser=0
    # Obtenir une référence au service de base de données
    # 获取对数据库服务的引用
    db = firebase.database()
    storage = firebase.storage()
    
    # Exemple de données 数据样例
    userUniqueId = pickle.load(open('user_id.txt','rb'))
    dataCible = {
            "timeStamp":timeStamp,
            "targetPosition": str(targetPositionObject)
            }
    
    dataUser = {
        "setup":{"time_update":300},
        "zone_name":["manger","libre","manger","libre",
                      "manger","libre","manger","libre"],
    }
    
    # Utiliser ID Tocken d'utilisateur pour télécharger des données json
    # 使用用户的 ID Tocken 上传 json 数据
    db.child("cibles").child(userUniqueId).push(dataCible, user['idToken'])
    db.child("users").child(userUniqueId).set(dataUser, user['idToken'])
    
    storage.child(userUniqueId + "/" + str(timeStamp)).put('image_raw/'+ str(timeStamp) + '.jpg', user['idToken'])