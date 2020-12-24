# 只有以下的 pyrebase4 的库可以正常运作
# https://github.com/nhorvath/Pyrebase4
import pyrebase 
import PySimpleGUI as sg
import binascii

def userSignIn():
    # config = {
    #   "apiKey": "apiKey",
    #   "authDomain": "projectId.firebaseapp.com",
    #   "databaseURL": "https://fir-rtc-aff50-default-rtdb.firebaseio.com/",
    #   "storageBucket": "projectId.appspot.com"
    # }
    
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
    	exit()
    
    UserEmail = values['_USER_EMAIL_']
    UserPassword = values['_USER_PASSWORD_']
    args = values
    
    win.Close()
     
    # Get a reference to the auth service
    auth = firebase.auth()
    
    try:
        # Log the user in
        user = auth.sign_in_with_email_and_password(UserEmail, UserPassword)
        sg.popup('登录成功！欢迎', UserEmail)
    except:
        sg.popup('发生了一些错误，可能是用户名/密码错误！')
    
    str_16 = binascii.b2a_hex(UserEmail.encode('utf-8'))
    print(str_16)
        
    ## 测试设计数据结构（未完成）
    ## https://firebase.google.com/docs/database/web/structure-data?authuser=0
    # Get a reference to the database service
    db = firebase.database()
    
    # data to save
    data = {
        "name": "Mortimer 'Morty' Smith"
    }
    
    # Pass the user's idToken to the push method
    results = db.child("users").push(data, user['idToken'])