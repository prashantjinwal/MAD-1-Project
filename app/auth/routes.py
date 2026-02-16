from flask import  render_template, url_for, redirect, request, flash, session
from werkzeug.security import generate_password_hash
from app import db


@auth.route("/register/student", method=['GET', 'POST'])
def register_student():
     if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        roll_no = request.form.get('roll_no')

        if User.query.filter_by(email=email).first():
          flash("Already register")
          return redirect(url_for("auth.register_student"))
        user  = User(
          email = email,
          password= generate_password_hash(password),
          role="student"
        )
        db.session.add(user)
        db.session.commit()

        student = Student(
          user_id=user.id,
          name=name,
          roll_no=roll_no
        )
        db.session.add(student)
        db.session.commit()

        flash("register successfully, Please login.")
        return redirect(url_for("auth.login"))

     return render_template("register_student.html")
