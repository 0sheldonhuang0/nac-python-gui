## https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc
## python 打包 https://www.jianshu.com/p/a944940ae0fc
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(r'fir-rtc-aff50-firebase-adminsdk-4r1i0-f00f6b52fe.json')
#firebase_admin.initialize_app(cred)

db = firestore.client()  # this connects to our Firestore database
collection = db.collection('places')  # opens 'places' collection
doc = collection.document('rome')  # specifies the 'rome' document

res = doc.get().to_dict()
print(res)

docs = collection.get()
print(docs)

res = collection.document('barcelona').set({
    'lat': 41.3851, 'long': 2.1734,
    'weather': 'great',
    'landmarks': [
        'guadí park',
        'gaudí church',
        'gaudí everything'
    ]
})
print(res)