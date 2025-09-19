from flask import Blueprint,jsonify,request,send_from_directory
from app.models import Member
from app.db import db
import re
import os
from flask_bcrypt  import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
bcrypt=Bcrypt()
#create student bluprint
member_bp=Blueprint("member",__name__)
@member_bp.route("/add", methods=["POST"])
def add_member():
    data=request.get_json()
    name=data.get("name")
    email=data.get("email")
    password=data.get( "password")

    exists = Member.query.filter_by(email=email).first()
    if exists:
        return jsonify({"error": "Email in use"}), 400
    hashed_password=bcrypt.generate_password_hash(password).decode("utf_8")
    new_member=Member(name=name, email=email, password=hashed_password)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({
        "message": "Member added",
        "student": {
            "id": new_member.id,
            "name": new_member.name,
            "email": new_member.email,
            "created_at": new_member.created_at
        }
    }), 201

@member_bp.route("login", methods=["POST"])
def login_member():
    data=request.get_json()

    email=data.get("email")
    password=data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}),400
    
    member=Member.query.filter_by(email=email).first()

    if not member:
        return jsonify({"error": "Member not found"}),401
    
    check_pass=bcrypt.check_password_hash(member.password, password)

    if not check_pass:
        return jsonify({"error": "Invalid email or password"}),401
    access_token=create_access_token(
        identity={"id": member.id, "name":member.name},
        expires_delta=timedelta(seconds=30)
    )
    return jsonify({"token":access_token}),200
    