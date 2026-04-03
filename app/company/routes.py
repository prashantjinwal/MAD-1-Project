from datetime import datetime
from flask import render_template, abort, url_for, redirect, flash, session, request
from flask_login import login_required, current_user
from app.company import company
from app.models import  Company,  PlacementDrive, Application, Student
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

    for drive in comp.drives:
        drive.auto_close()
    db.session.commit()

    return render_template(
        'company/c_dashboard.html',
        comp=comp,
        drives=drives,
        total_drives=total_drives,
        open_drives=open_drives,
        total_applications=total_applications
    )

# placement drive
@company.route('/company/placementdrive')
@login_required
def placement_drive():

    if current_user.role != "company":
        return "Unauthorized", 403

    if not current_user.company:
        return "Company profile not found", 404

    comp = current_user.company

    # Drives of this company
    drives = comp.drives

    return render_template(
        'company/placement_drives.html',
        comp=comp,
        drives=drives,
        
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
    if drive.company_id != current_user.company.id:
        abort(403)

    Application.query.filter_by(drive_id=drive.id).delete()

    db.session.delete(drive)
    db.session.commit()
    return redirect(url_for("company.c_company"))


# edit drives
@company.route('/company/edit-drive/<int:id>', methods=['POST','GET'])
@login_required
def edit_drive(id):
    curr_drive = PlacementDrive.query.get_or_404(id)
    if curr_drive.company_id != current_user.company.id:
        abort(403)

    if request.method == "POST":
        curr_drive.job_title = request.form.get("job_title")
        curr_drive.description = request.form.get("description")
        curr_drive.eligibility = request.form.get("eligibility")

        deadline = request.form.get("deadline")
        if deadline:
            curr_drive.deadline = datetime.fromisoformat(deadline)

        db.session.commit()
        flash("Drive Updated Successfully!", "success")
        return redirect(url_for("company.c_company"))

    return render_template("company/edit_drive.html", curr_drive=curr_drive)


@company.route('/company/view/<int:id>')
@login_required
def view_application(id):
    drive = PlacementDrive.query.get_or_404(id)
    return render_template("company/view.html", drive=drive)

@company.route("/company/application/<int:app_id>")
@login_required
def application_detail(app_id):

    application = Application.query.get_or_404(app_id)

    return render_template(
        "company/application_detail.html",
        application=application
    )

@company.route("/company/update-status/<int:app_id>/<string:status>", methods=["POST"])
@login_required
def update_application_status(app_id, status):

    application = Application.query.get_or_404(app_id)

    if current_user.role != "company":
        abort(403)

    valid_status = ["shortlisted", "selected", "rejected"]

    if status not in valid_status:
        abort(400)

    application.status = status
    db.session.commit()

    flash(f"Application marked as {status}", "success")

    return redirect(url_for("company.application_detail", app_id=app_id))


# @company.route('/update_status/<int:app_id>', methods=['POST'])
# @login_required
# def update_status(app_id):
#     application = Application.query.get_or_404(app_id)

#     application.status = request.form.get("status")

#     db.session.commit()

#     return redirect(request.referrer)

@company.route('/company/com_profile/<int:id>', methods=['POST','GET'])
@login_required
def com_profile(id):
    curr_company = Company.query.get_or_404(id)
    if curr_company.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        curr_company.company_name = request.form.get("company_name")
        curr_company.hr_name  = request.form.get("hr_name")
        curr_company.website  = request.form.get("website")
        curr_company.approval_status  = request.form.get("approval_status")
        # curr_company.email  = request.form.get("email")


        email = request.form.get("email")
        if email:
            curr_company.user.email = email

        db.session.commit()
        return redirect (url_for("company.c_company"))

    return render_template ("company/profile.html", curr_company=curr_company)
