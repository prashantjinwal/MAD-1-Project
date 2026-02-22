from flask import render_template, abort
from flask_login import login_required, current_user
from app.admin import admin
from app.models import Student, Company, PlacementDrive, Application

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

     return render_template('admin/a_dashboard.html', total_student=total_student, total_companies=total_companies,total_drives=total_drives,total_applications=total_applications)
