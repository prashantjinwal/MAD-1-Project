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

    comp = current_user.company

    # Drives of this company
    drives = comp.drives

    total_drives = len(drives)
    open_drives = len([d for d in drives if d.status == 'open'])

    # Total applications
    total_applications = sum(len(d.applications) for d in drives)

    return render_template(
        'company/c_dashboard.html',
        comp=comp,
        drives=drives,
        total_drives=total_drives,
        open_drives=open_drives,
        total_applications=total_applications
    )