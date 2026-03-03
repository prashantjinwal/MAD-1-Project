from datetime import datetime
from flask import render_template, abort, url_for, redirect, flash, session, request
from flask_login import login_required, current_user
from app.company import company
from app.models import  Company,  PlacementDrive
from app import db


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


# drive logic
@company.route('/company/create-drive', methods=['GET','POST'])
@login_required
def create_drive():
    if current_user.role != 'company':
        abort(403)
    
    comp = current_user.company
    if not comp:
        abort(404)
    
    if comp.approval_status != 'approved' :
        flash('Your account is not approved yet.')
        return redirect(url_for("company.c_company"))

    if request.method == 'POST' :
        job_title = request.form.get("job_title")
        description = request.form.get("description")
        eligibility = request.form.get("eligibility")
        deadline = request.form.get("deadline")

        # save data in new_drive
        new_drive = PlacementDrive(
            company_id=comp.id,
            job_title=job_title,
            description=description,
            eligibility=eligibility,
            deadline=datetime.strptime(deadline, "%Y-%m-%d"),
            status="pending"
        )

        db.session.add(new_drive)
        db.session.commit()

        # if dirve sucessfully created
        flash("Placement Drive Created Successfully!", "success")
        return redirect(url_for("company.c_company"))
    

    return render_template("company/drive_popup.html", comp=comp)


@company.route('/company/delete-drive/<int:id>',methods=['POST'])
@login_required
def delete_drive(id):
    drive= PlacementDrive.query.get_or_404(id)
    db.session.delete(drive)
    db.session.commit()
    return redirect(url_for("company.c_company"))