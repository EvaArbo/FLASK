from flask import Blueprint,jsonify,request,send_from_directory
from app.models import Member
from app.db import db
import re
import os

from flask_bcrypt  import Bcrypt
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
        "message": "Student added",
        "student": {
            "id": new_member.id,
            "name": new_member.name,
            "email": new_member.email,
            "created_at": new_member.created_at
        }
    }), 201


