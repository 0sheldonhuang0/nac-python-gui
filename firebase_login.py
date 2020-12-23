import pyrebase

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

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password("sheldonhuang1994@gmail.com", "g3g4x5122")

print(user)
# # Get a reference to the database service
# db = firebase.database()

# # data to save
# data = {
#     "name": "Mortimer 'Morty' Smith"
# }

# # Pass the user's idToken to the push method
# results = db.child("users").push(data, user['idToken'])