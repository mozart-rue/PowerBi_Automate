import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./config/serviceAccountKey.json")
firebase_admin.initiliaze_app(cred)

