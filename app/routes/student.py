from flask import Blueprint, jsonify, request, send_from_directory
from app.models import Student
from app.db import db
import re
import os


#create student blueprint
student_bp = Blueprint("student", __name__)

UPLOAD_FOLDER = "uploads"

# -------------------------------
# Get a single student
# -------------------------------
@student_bp.route("/single/<int:student_id>", methods=["GET"])
def get_single_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": f"student with id {student_id} does not exist"}), 404
    
    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "created_at": student.created_at
    }), 200


# -------------------------------
# Edit single student
# -------------------------------
@student_bp.route("/edit/<int:student_id>", methods=["PUT"])
def edit_single_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": f"student with id {student_id} does not exist"}), 404

    data = request.get_json(force=True)  # force=True fixes 415 if header missing

    if "name" in data:
        student.name = data["name"]
    if "email" in data:
        student.email = data["email"]

    db.session.commit()

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "created_at": student.created_at
    }), 200


# Delete single student

@student_bp.route("/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": f"student with id {student_id} does not exist"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": f"Student with id {student_id} has been deleted successfully."
    }), 200




# Add student (JSON)

@student_bp.route("/add/json", methods=["POST"])
def add_student_json():
    data = request.get_json(force=True)

    name = data.get("name")
    email = data.get("email")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email address"}), 400

    # Existing student
    exists = Student.query.filter_by(email=email).first()
    if exists:
        return jsonify({"error": "Email in use"}), 400

    new_student = Student(name=name, email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Student added",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "created_at": new_student.created_at
        }
    }), 201


# -------------------------------
# Add student (Form)
# -------------------------------
@student_bp.route("/add/form", methods=["POST"])
def add_student_form():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email address"}), 400

    exists = Student.query.filter_by(email=email).first()
    if exists:
        return jsonify({"error": "Email in use"}), 400

    new_student = Student(name=name, email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Student added",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "created_at": new_student.created_at
        }
    }), 201


# -------------------------------
# Upload picture
# -------------------------------
@student_bp.route("/picture", methods=["POST"])
def add_student_picture():
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if "pic" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["pic"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename
    ext = filename.rsplit(".", 1)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Invalid file type"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "path": filepath
    }), 201



# Serve uploaded file

@student_bp.route("/picture/<filename>", methods=["GET"])
def serve_file(filename):
    cwd = os.path.dirname(__file__)
    uploads = os.path.join(cwd, "../../uploads")
    return send_from_directory(uploads, filename)



# List all students

@student_bp.route("/list", methods=["GET"])
def list_users():
    students = Student.query.all()
    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "created_at": student.created_at
        })

    return jsonify({
        "students": student_list,
        "count": len(student_list)
    }), 200
