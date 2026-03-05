from flask import render_template, redirect
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
    total_shortlist_dives = Application.query.filter_by(status="shortlisted").count()
    
    return render_template(
        'student/s_dashboard.html',
        stu=stu,
        available_drives=available_drives,
        applications=applications,
        total_applied=total_applied,
        total_shortlist_dives=total_shortlist_dives
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