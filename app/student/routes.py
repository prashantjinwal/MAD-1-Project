from flask import render_template
from flask_login import login_required, current_user
from app.student import student

@student.route('/dashboard')
@login_required
def s_student():
     return render_template('student/s_dashboard.html')

