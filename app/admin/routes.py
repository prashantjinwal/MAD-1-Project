from flask import render_template, abort, url_for, redirect, flash, session, request
from flask_login import login_required, current_user
from app.admin import admin
from app.models import Student, Company, PlacementDrive, Application,User
from app import db

@admin.route('/admin/dashboard')
@login_required
def a_admin():
     if current_user.role != "admin":
          abort(403)
     # count
     total_student = Student.query.count()
     total_companies = Company.query.count()
     total_drives = PlacementDrive.query.count()
     total_applications = Application.query.count()

     
     view = request.args.get("view")
     # blacklisted companies
     blacklist_companies = Company.query.filter_by(approval_status='blacklisted').all()
     # pending companies
     pending_companies = Company.query.filter_by(approval_status='pending').all()
     reject_companies = Company.query.filter_by(approval_status='rejected').all()
     all_blocked_companies = blacklist_companies + reject_companies

# 

     #placement drives
     drive_view = request.args.get("drive_view")
     # pending drives
     pending_drives = PlacementDrive.query.filter_by(status='pending').all()
     reject_drives = PlacementDrive.query.filter_by(status='rejected').all()

     # placement_drive = PlacementDrive.query.all()
    
     return render_template('admin/a_dashboard.html',drive_view=drive_view, pending_drives=pending_drives, reject_drives=reject_drives, view=view, reject_companies=reject_companies, all_blocked_companies=all_blocked_companies, total_student=total_student, total_companies=total_companies,total_drives=total_drives,total_applications=total_applications,pending_companies=pending_companies, blacklist_companies=blacklist_companies)


@admin.route('/admin/approve/<int:id>')
@login_required
def approve_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "approved"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))


@admin.route('/admin/reject/<int:id>')
@login_required
def reject_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "rejected"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))

@admin.route('/admin/blacklist/<int:id>')
@login_required
def blacklist_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "blacklisted"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))


@admin.route('/admin/pending/<int:id>')
@login_required
def pending_company(id):
     if current_user.role != "admin":
        abort(403)
     
     company = Company.query.get_or_404(id)
     company.approval_status = "pending"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))

# drives
@admin.route('/admin/drives_reject/<int:id>')
@login_required
def reject_drives(id):
     if current_user.role != "admin":
        abort(403)
     
     drives = PlacementDrive.query.get_or_404(id)
     drives.status = "rejected"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))


@admin.route('/admin/approve_drives/<int:id>')
@login_required
def approve_drives(id):
     if current_user.role != "admin":
        abort(403)
     
     drives = PlacementDrive.query.get_or_404(id)
     drives.status = "open"
     db.session.commit()
     return redirect(url_for('admin.a_admin'))
