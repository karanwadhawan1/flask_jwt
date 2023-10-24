import jwt 
from app import app
from flask import request
from functools import wraps
from app.auth.model import User
from datetime import datetime, timedelta




def encode_token(user_id):
    payload ={
        'exp': datetime.utcnow() + timedelta(days=1, seconds=5 ),
        'iat' :datetime.utcnow(),
        'sub':user_id
        
    }
    access_token = jwt.encode(payload,app.config['SECRET_KEY_ACCESS_TOKEN'],algorithm= 'HS256')
    refresh_payload = {
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    refresh_token = jwt.encode(refresh_payload, app.config['SECRET_KEY_REFRESH_TOKEN'], algorithm='HS256')

   
    return access_token, refresh_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print(token)
        if not token:
            return {
                "message": "Authentication Token is missing",
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, app.config["SECRET_KEY_ACCESS_TOKEN"], algorithms=["HS256"])
            current_user=User.query.filter_by(id=data['sub']).first()
            if current_user is None:
                return {
                "message": "Invalid Authentication token",
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "An error Occured",
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated