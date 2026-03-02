from flask import render_template
from flask_login import login_required, current_user
from app.company import company
from app.models import  Company

@company.route('/company/dashboard')
@login_required
def c_company():

     if current_user.role != "company":
          return "Unauthorized", 403

     if not current_user.company:
          return "Company profile not found", 404

     return render_template(
          'company/c_dashboard.html',
          comp=current_user.company
     )