from flask import Flask, request
import pymongo
from pymongo import MongoClient
from flask import jsonify
app = Flask(__name__)
from flask_cors import CORS
import bcrypt
import re


cors = CORS(app, resources={r"/*": {"origins": "*"}})
client = MongoClient("mongodb://localhost:27017")
db = client["enolity"]
collection = db['useres']

@app.route("/login", methods=['POST'])
def login():
    input_data = request.get_json()
    email = input_data['email']
    password = input_data['password']
    user = db.useres.find_one({'email':email,'password':password})
    if user and '_id' in user:
        return{
            'status':1,
            'msg':"user exits",
            'classs':"success"
        }
    else:
        return{
            'status':0,
            'msg':"user not exits",
            'classs':"danger"
        }
    
# @app.route("/register", methods=['POST'])
# def register():
#     input_data = request.get_json()
    
#     name = input_data.get('fullName')
#     email = input_data.get('email')
#     phonenumber = input_data.get('phonenumber')
#     password = input_data.get('password')

#     if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$", password):
#         return jsonify({
#             'status': 0,
#             'msg': "Password must be 8-16 characters long, include uppercase, lowercase, a number, and a special character.",
#             'class': "error"
#         })

#     if "gmail" in password.lower():
#         return jsonify({
#             'status': 0,
#             'msg': "Password should not contain 'gmail'.",
#             'class': "error"
#         })

#     user = db.useres.find_one({'email': email})
#     if user:
#         return jsonify({
#             'status': 0,
#             'msg': "User already exists",
#             'class': "error"
#         })

#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     count = db.useres.count_documents({})
#     new_user = {
#         "_id": count + 1,
#         "fullName": name,
#         "email": email,
#         "phonenumber": phonenumber,
#         "password": hashed_password.decode('utf-8')
#     }

#     db.useres.insert_one(new_user)
    
#     return jsonify({
#         'status': 1,
#         'msg': "User registered successfully",
#         'class': "success"
#     })

@app.route("/register", methods=['POST'])
def register():
    input_data = request.get_json()
    
    name = input_data.get('fullName')
    email = input_data.get('email')
    phonenumber = input_data.get('phonenumber')
    password = input_data.get('password')

    # Validate phone number (10-digit numeric)
    if not re.fullmatch(r"\d{10}", phonenumber):
        return jsonify({
            'status': 0,
            'msg': "Phone number must be exactly 10 digits.",
            'class': "error"
        })

    # Validate password strength
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$", password):
        return jsonify({
            'status': 0,
            'msg': "Password must be 8-16 characters long, include uppercase, lowercase, a number, and a special character.",
            'class': "error"
        })

    if "gmail" in password.lower():
        return jsonify({
            'status': 0,
            'msg': "Password should not contain 'gmail'.",
            'class': "error"
        })

    # Check if the email is already registered
    existing_user = db.useres.find_one({'email': email})
    if existing_user:
        return jsonify({
            'status': 0,
            'msg': "User with this email already exists.",
            'class': "error"
        })

    # Check the number of registrations for this phone number (limit to 3 emails per number)
    email_count = db.useres.count_documents({'phonenumber': phonenumber})
    if email_count >= 3:
        return jsonify({
            'status': 0,
            'msg': "A maximum of 3 email addresses can be registered with this phone number.",
            'class': "error"
        })

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Assign a unique ID
    count = db.useres.count_documents({})
    new_user = {
        "_id": count + 1,
        "fullName": name,
        "email": email,
        "phonenumber": phonenumber,
        "password": hashed_password.decode('utf-8')
    }

    db.useres.insert_one(new_user)
    
    return jsonify({
        'status': 1,
        'msg': "User registered successfully",
        'class': "success"
    })