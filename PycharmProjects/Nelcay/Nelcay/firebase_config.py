import firebase_admin
from firebase_admin import credentials, firestore
import os


def get_db():
    if not firebase_admin._apps:
        # 1. Point to the EXACT file in the Nelcay folder
        # Ensure 'serviceAccountKey.json' is inside the Nelcay folder (as shown in your screenshot)
        key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'serviceAccountKey.json')

        print(f"DEBUG: Reading credentials from: {key_path}")

        # 2. Initialize with absolute certainty
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        print("DEBUG: Firebase initialized successfully.")

    return firestore.client()


db = get_db()