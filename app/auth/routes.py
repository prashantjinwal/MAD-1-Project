from flask import  render_template, url_for, redirect, request, flash, session
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User, Student
from app.auth import auth


@auth.route("/register/student", methods=['GET', 'POST'])
def register_student():
     if request.method == 'POST':
         email = request.form.get("email")
         password = request.form.get("password")
         name = request.form.get("name")
         roll_no = request.form.get('roll_no')

         if User.query.filter_by(email=email).first():
           flash("Already register")
           return redirect(url_for("auth.login_student"))
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
         return redirect(url_for("auth.login_student"))

     return render_template("auth/register.html")


@auth.route("/login/student", methods=['GET','POST'])
def login_student():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("user not found")
            return redirect(url_for('auth.login_student'))
        if user.role != 'student':
            flash("Unauthorized access")
            return redirect(url_for('auth.login_student'))
        if not check_password_hash(user.password, password):
            flash("Incorrect password")
            return redirect(url_for("auth.login_student"))
        
        login_user(user)
        flash('Login sucessfully')
        return redirect(url_for('student.s_dashboard'))
    
    return render_template('auth/login.html')
      


    