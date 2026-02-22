from flask import render_template
from flask_login import login_required, current_user
from app.admin import admin

@admin.route('/admin/dashboard')
@login_required
def a_admin():
     return render_template('admin/a_dashboard.html')
