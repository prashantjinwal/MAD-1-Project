from flask import render_template, abort, url_for, redirect, flash, session, request
from flask_login import login_required, current_user
from app.admin import admin
from app.models import Student, Company, PlacementDrive, Application, User
from app import db
from sqlalchemy import or_




@admin.route('/admin/dashboard')
@login_required
def a_admin():
    if current_user.role != "admin":
        abort(403)

    total_student = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    view = request.args.get("view")
    # blacklisted companies
    blacklist_companies = Company.query.filter_by(approval_status='blacklisted').all()
    # pending companies
    pending_companies = Company.query.filter_by(approval_status='pending').all()
    #  reject_companies = Company.query.filter_by(approval_status='rejected').all()
    all_blocked_companies = blacklist_companies 

    #placement drives
    drive_view = request.args.get("drive_view")
    # pending drives
    pending_drives = PlacementDrive.query.filter_by(status='pending').all()
    reject_drives = PlacementDrive.query.filter_by(status='rejected').all()

    # application status counts
    status_applied = Application.query.filter_by(status='applied').count()
    status_shortlisted = Application.query.filter_by(status='shortlisted').count()
    status_selected = Application.query.filter_by(status='selected').count()
    status_rejected = Application.query.filter_by(status='rejected').count()

    # drive status count
    drives_pending = PlacementDrive.query.filter_by(status='pending').count()
    drives_open = PlacementDrive.query.filter_by(status='open').count()
    drives_rejected = PlacementDrive.query.filter_by(status='rejected').count()
    drives_closed = PlacementDrive.query.filter_by(status='closed').count()

    return render_template(
        'admin/dashboard.html',
        total_student=total_student,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications,
        view=view,
        blacklist_companies=blacklist_companies,
        pending_companies=pending_companies,
        all_blocked_companies=all_blocked_companies,
        drive_view=drive_view,
        pending_drives=pending_drives,
        reject_drives=reject_drives,
        status_applied=status_applied,
        status_shortlisted=status_shortlisted,
        status_selected=status_selected,
        status_rejected=status_rejected,
        drives_pending=drives_pending,
        drives_open=drives_open,
        drives_rejected=drives_rejected,
        drives_closed=drives_closed,

    )


@admin.route('/admin/blacklist/<int:id>')
@login_required
def blacklist_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "blacklisted"
     db.session.commit()
     return redirect(request.referrer)

@admin.route('/admin/approve/<int:id>')
@login_required
def approve_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "approved"
     db.session.commit()
     return redirect(request.referrer)

@admin.route('/admin/pending/<int:id>')
@login_required
def pending_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "pending"
     db.session.commit()
     return redirect(request.referrer)

@admin.route('/admin/reject/<int:id>')
@login_required
def reject_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "rejected"
     db.session.commit()
     return redirect(request.referrer)


# drives
@admin.route('/admin/drives_reject/<int:id>')
@login_required
def reject_drives(id):
     if current_user.role != "admin":
        abort(403)
     
     drives = PlacementDrive.query.get_or_404(id)
     drives.status = "rejected"
     db.session.commit()
     return redirect(request.referrer)


@admin.route('/admin/approve_drives/<int:id>')
@login_required
def approve_drives(id):
     if current_user.role != "admin":
        abort(403)
     
     drives = PlacementDrive.query.get_or_404(id)
     drives.status = "open"
     db.session.commit()
     return redirect(request.referrer)

# navigators
@admin.route('/admin/companies')
@login_required
def companies():
     if current_user.role != 'admin':
        abort(403)
     
     # companies = Company.query.all()
     search = request.args.get('search')
     
     if search:
         companies = Company.query.filter(
             Company.company_name.ilike(f"%{search}%")
         ).all()
     else:
         companies = Company.query.all()

     return render_template('admin/navigators/companies.html', companies=companies)

@admin.route('/admin/students')
@login_required
def students():
     if current_user.role != 'admin':
        abort(403)
     search = request.args.get('search')

     if search:
        students = Student.query.filter(
            (Student.name.ilike(f"%{search}%")) |
            (Student.roll_no.ilike(f"%{search}%"))
        ).all()
     else:
        students = Student.query.all()

     return render_template('admin/navigators/students.html', students=students)
     
@admin.route('/admin/deactivate_student/<int:id>')
@login_required
def deactivate_student(id):
     if current_user.role != 'admin':
        abort(403)
     stu = Student.query.get_or_404(id)

     if stu.is_blacklisted == True :
         stu.is_blacklisted = False
     else :
         stu.is_blacklisted = True
     db.session.commit()
     return redirect(request.referrer)


@admin.route('/admin/drives')
@login_required
def drives():
     if current_user.role != 'admin':
        abort(403)

     # drives = PlacementDrive.query.all()
     search = request.args.get("search")
     if search:
         drives = PlacementDrive.query.filter(
             (PlacementDrive.job_title.ilike(f"%{search}%")) |
             ( Company.company_name.ilike(f"%{search}%"))
         ).all()
     else:
         drives = PlacementDrive.query.all()

     return render_template('admin/navigators/drives.html', drives=drives)


@admin.route('/admin/applicants')
@login_required
def applicants():
     if current_user.role != 'admin':
        abort(403)
     search = request.args.get("search", "")

     if search:
        applicants = Application.query.join(Student).join(PlacementDrive).join(Company).filter(
            or_(
                Student.name.like(f"%{search}%"),
                Student.roll_no.like(f"%{search}%"),
                PlacementDrive.job_title.like(f"%{search}%"),
                Company.company_name.like(f"%{search}%")
            )
        ).all()
     else:
        applicants = Application.query.all()


     return render_template('admin/navigators/applications.html',applicants=applicants)

