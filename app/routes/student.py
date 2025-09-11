from flask import Blueprint, jsonify,request
#create student blueprint
student_bp=Blueprint("student", __name__,)


@student_bp.route("/", methods=["GET"])
def home():
    return """
<!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    HELLO ,GOODmorning
</body>
</html>
"""
#routes and controler logic
@student_bp.route("/add", methods=["POST"])
def add_user():
    print("Add user was hit")
    return"Adding a user"

@student_bp.route("/list", methods=["GET"])
def list_user():
    print("List Students")

    return"List all students"