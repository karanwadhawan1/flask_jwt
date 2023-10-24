import jwt 
from app import app
from app.db import db
from flask import Blueprint
from app.auth.model import User
from datetime import datetime, timedelta
from flask import request,jsonify,make_response
from app.utils import encode_token,token_required
from werkzeug.security import generate_password_hash,check_password_hash


auth_bp = Blueprint('auth', __name__,)



@auth_bp.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    user = User.query.filter_by(email = user_data['email']).first()
    if not user:
        try: 

            hashed_password = generate_password_hash(user_data['password'])
            user = User(email =user_data['email'], password =hashed_password)
            db.session.add(user)
            db.session.commit()
            resp = {
                "status":"success",
                "message":"User successfully registered",
            }
            return make_response(jsonify(resp)),201

        except Exception as e:
            print(e)
            resp = {
                "status" :"Error",
                "message" :" Error occured, user registration failed"
            }
            return make_response(jsonify(resp)),401
    else:
        resp = {
            "status":"error",
            "message":"User already exists"
        }
        return make_response(jsonify(resp)),202


@auth_bp.route('/login',methods = ['POST'])
def post():
    user_data = request.get_json()
    try:

        user = User.query.filter_by(email = user_data['email']).first()
        
        if user and check_password_hash(user.password,user_data['password'])==True:
            
            access_token,refresh_token = encode_token(user.id)
            
            resp = {

                "status":"succes",
                "message" :"Successfully logged in",
                'access_token':access_token,
                'refresh_token':refresh_token
            }
            return make_response(jsonify(resp)),200
        else:
            resp ={
                "status":"Error",
                "message":"User does not exist"
            }
            return make_response(jsonify(resp)), 404

    except Exception as e:
        print(e)
        resp = {
            "Status":"error",
                "Message":"User login failed"
        }
        return make_response(jsonify(resp)), 404
    


@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    resp={}
    try:
        refresh_token = request.json['refresh_token']
        payload = jwt.decode(refresh_token, app.config["SECRET_KEY_REFRESH_TOKEN"], algorithms=['HS256'])
        user_id = payload['sub']
        payload ={
        'exp': datetime.utcnow() + timedelta(days=1, seconds=5 ),
        'iat' :datetime.utcnow(),
        'sub':user_id
        }
        access_token = jwt.encode(payload,app.config['SECRET_KEY_ACCESS_TOKEN'],algorithm= 'HS256')
        return {'access_token': access_token},200
    except jwt.ExpiredSignatureError:
        resp['message']= 'Expired refresh token'
        return make_response(jsonify(resp)), 401
    except jwt.InvalidTokenError:
        resp['message']= 'Invalid refresh token'
        return make_response(jsonify(resp)), 401

@auth_bp.route('/')
@token_required
def hello_world(current_user):
    return f'Welcome to JWT Tokens user id :{current_user.id},user email:{current_user.email}'
        
