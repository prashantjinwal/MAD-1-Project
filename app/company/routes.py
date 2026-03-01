from flask import render_template
from flask_login import login_required, current_user
from app.company import company

@company.route('/company/dashboard')
@login_required
def c_company():
     
     return render_template('company/c_dashboard.html')

