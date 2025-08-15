import json
import pyrebase4 as pyrebase
from typing import Optional, Tuple

with open("firebase_client_config.json", "r") as f:
    client_cfg = json.load(f)

firebase = pyrebase.initialize_app(client_cfg)
auth = firebase.auth()

def sign_in(email: str, password: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user["idToken"], user.get("refreshToken"), user["localId"]
    except Exception:
        return None, None, None

def sign_up(email: str, password: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user["idToken"], user.get("refreshToken"), user["localId"]
    except Exception:
        return None, None, None
