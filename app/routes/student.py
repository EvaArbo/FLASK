from flask import Blueprint,jsonify,request

#create student bluprint
student_bp=Blueprint("student",__name__)


@student_bp.route("/",methods=["GET"])
def single_student():
    print("Single student")
    return "Single student"

#routes and controller logic
@student_bp.route("/add/json",methods=["POST"])
def add_user():
    print("Add user was hit")
    data=request.get_json()
    print ("received data", data)
    return "Adding a student",200

@student_bp.route("/edit",methods=["PUT"])
def edit_student():
    print("Add user was hit")
    return "Edit a student"

@student_bp.route("/list",methods=["GET"])
def list_users():
    print("List Students")
    return "List All students"
