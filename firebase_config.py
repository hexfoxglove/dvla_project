import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key
cred = credentials.Certificate("/content/drive/MyDrive/dvla_project/firebase_key.json")

# Initialize Firebase app (only once)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
