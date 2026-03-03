from flask import render_template
from flask_login import login_required, current_user
from app.student import student
from app.models import Student

@student.route('/student/dashboard')
@login_required
def s_student():

     if current_user.role != "student":
        return "Unauthorized", 403
     
     if not current_user.student:
        return "Company profile not found", 404

     stu = current_user.student
     print("Logged user id:", current_user.id)
     print("Student object:", current_user.student)

     return render_template('student/s_dashboard.html', stu=stu)

