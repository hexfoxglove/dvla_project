from firebase_config import db

def get_user_role(uid: str) -> str:
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        return doc.to_dict().get("role", "customer")
    return "customer"

def set_user_role(uid: str, email: str, role: str):
    db.collection("users").document(uid).set({
        "email": email,
        "role": role
    }, merge=True)
