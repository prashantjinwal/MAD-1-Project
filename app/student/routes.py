from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.student import student
from app.models import Student, PlacementDrive, Application,Company
from app import db
import os
from werkzeug.utils import secure_filename

@student.route('/student/dashboard')
@login_required
def s_student():

    if current_user.role != "student":
        return "Unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()

    if not stu:
        return "Student profile not found", 404

    available_drives = PlacementDrive.query.filter_by(status="open").count()
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
     if current_user.role != "student":
        return "Unauthorized", 403
     
     drive = PlacementDrive.query.get_or_404(drive_id)
     if drive.status != "open":
        return "Drive is not open", 400
     
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
     
     return redirect(url_for('student.s_student'))


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@student.route('/student/stu_profile/<int:id>', methods=['POST','GET'])
@login_required
def stu_profile(id):
    if current_user.role != "student":
        return "Unauthorized", 403
    curr_student = Student.query.get_or_404(id)

    if curr_student.user_id != current_user.id:
        return "Forbidden", 403
    
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
        # resume logic
        file = request.files.get('resume')

        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"resume_{curr_student.id}_{filename}"

                upload_folder = os.path.join('app', 'static', 'uploads')
                file.save(os.path.join(upload_folder, filename))
                curr_student.resume = filename
            else:
                flash("Only PDF, DOC, DOCX allowed!", "danger")
                return redirect(request.url)

        db.session.commit()
        return redirect (url_for("student.s_student"))

    return render_template ("student/profile.html", curr_student=curr_student)


@student.route('/student/stu_history/<int:id>', methods=['GET'])
@login_required
def stu_history(id):
    if current_user.role != "student":
        return "Unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()
    if not stu:                                            
        return "Student profile not found", 404
    
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
    
    # student ne jin drives me apply kiya hai
    applied_apps = Application.query.filter_by(student_id=stu.id).all()

    # un drives ke ids
    applied_drive_ids = [app.drive_id for app in applied_apps]

    # open drives jo student ne apply nahi ki
    available_drives = PlacementDrive.query.filter(
        PlacementDrive.status == "open",
        ~PlacementDrive.id.in_(applied_drive_ids)
    ).all()

    return render_template('student/my_application.html', drives=available_drives)



@student.route('/student/application')
@login_required
def application():
    if current_user.role != 'student':
        return "unauthorized", 403

    stu = Student.query.filter_by(user_id=current_user.id).first()

    search = request.args.get("search")

    if search:
        myapp = Application.query.join(PlacementDrive).filter(
            Application.student_id == stu.id,
            PlacementDrive.job_title.ilike(f"%{search}%")
        ).all()
    else:
        myapp = Application.query.filter_by(student_id=stu.id).all()

    return render_template(
        'student/navigator/application.html',
        myapp=myapp
    )


@student.route('/student/explore')
@login_required
def explore():

    if current_user.role != "student":
        return "Unauthorized", 403
    
    open_drives = PlacementDrive.query.filter_by(status='open').all()
    for drive in open_drives:
        drive.auto_close()
    db.session.commit()
    
    stu = Student.query.filter_by(user_id=current_user.id).first()
    search = request.args.get("search")

    if search:
        available_drives = PlacementDrive.query.join(Company).filter(
            PlacementDrive.status == "open",
            db.or_(
                PlacementDrive.job_title.ilike(f"%{search}%"),
                Company.company_name.ilike(f"%{search}%")
            )
        ).all()

    else:
        available_drives = PlacementDrive.query.filter_by(status="open").all()

    applied_drives = Application.query.filter_by(student_id=stu.id).all()
    applied_drive_ids = [x.drive_id for x in applied_drives] 

    return render_template(
        'student/navigator/exploredrives.html',
        available_drives=available_drives, 
        applied_drive_ids = applied_drive_ids
    )