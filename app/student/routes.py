from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from app.student import student
from app.models import Student, PlacementDrive, Application
from app import db


@student.route('/student/dashboard')
@login_required
def s_student():

    if current_user.role != "student":
        return "Unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()

    if not stu:
        return "Student profile not found", 404

    available_drives = PlacementDrive.query.filter_by(status="open").all()
    applications = Application.query.filter_by(student_id=stu.id).all()
    total_applied = len(applications)
    total_shortlist_dives = Application.query.filter_by(status="shortlisted",student_id=stu.id).count()
    total_selected_dives = Application.query.filter_by(status="selected",student_id=stu.id).count()
    
    return render_template(
        'student/s_dashboard.html',
        stu=stu,
        available_drives=available_drives,
        applications=applications,
        total_applied=total_applied,
        total_shortlist_dives=total_shortlist_dives,
        total_selected_dives=total_selected_dives
    )


@student.route('/student/apply/<int:drive_id>')
@login_required
def apply_drive(drive_id):

     stu = Student.query.filter_by(user_id=current_user.id).first()
     existing = Application.query.filter_by(
         student_id = stu.id,
         drive_id = drive_id
     ).first()

     if existing : 
          return "Already Applied"

     new_app = Application(
         student_id = stu.id,
         drive_id = drive_id
     )

     db.session.add(new_app)
     db.session.commit()

     return redirect('/student/dashboard')


@student.route('/student/stu_profile/<int:id>', methods=['POST','GET'])
@login_required
def stu_profile(id):
    curr_student = Student.query.get_or_404(id)
    if request.method == "POST":
        curr_student.name = request.form.get("name")
        curr_student.roll_no  = request.form.get("roll_no")
        curr_student.branch  = request.form.get("branch")
        curr_student.phone  = request.form.get("phone")
        curr_student.cgpa  = request.form.get("cgpa")
        # curr_student.user.email  = request.form.get("email")

        email = request.form.get("email")
        if email:
            curr_student.user.email = email

        db.session.commit()
        return redirect (url_for("student.s_student"))

    return render_template ("student/profile.html", curr_student=curr_student)


@student.route('/student/stu_history/<int:id>', methods=['POST','GET'])
@login_required
def stu_history(id):
    if current_user.role != "student":
        return "Unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()
    applications = Application.query.filter_by(student_id=stu.id).all()
    return render_template("student/history.html",applications=applications)


@student.route('/student/my_application')
@login_required
def my_application():

    if current_user.role != "student":
        return "Unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()

    if not stu:
        return "Student profile not found", 404

    return render_template('student/my_application.html')
