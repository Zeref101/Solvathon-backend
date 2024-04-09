from firebase_admin import auth, firestore


def get_db():
    return firestore.client()
