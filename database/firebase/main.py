import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./config/serviceAccountKey.json")
firebase_admin.initiliaze_app(cred)

db = firestore.client()
