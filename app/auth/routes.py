from flask import  render_template, url_for, redirect, request, flash, session
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User, Student, Company
from app.auth import auth


# Register for students
@auth.route("/register/student", methods=['GET', 'POST'])
def register_student():
     if request.method == 'POST':
         email = request.form.get("email")
         password = request.form.get("password")
         name = request.form.get("name")
         roll_no = request.form.get('roll_no')

         if User.query.filter_by(email=email).first():
           flash("Already register")
           return redirect(url_for("auth.login"))
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

     return render_template("auth/register.html")


# Register for company
@auth.route("/register/company", methods=['GET', 'POST'])
def register_company():
     if request.method == 'POST':
         email = request.form.get("email")
         password = request.form.get("password")
         company_name = request.form.get("company_name")

         if User.query.filter_by(email=email).first():
             flash("Company already registerd")
             return redirect(url_for("auth.login"))
         user = User(
             email = email,
             password = generate_password_hash(password),
             role='company'
         )
         db.session.add(user)
         db.session.commit()

         company = Company(
             user_id=user.id,
             company_name = company_name
         )
         db.session.add(company)
         db.session.commit()

         flash("register successfully, Please login.")
         return redirect(url_for("auth.login"))
     
     return render_template("auth/register_company.html")
         

         
# universal login
@auth.route("/login/student", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()


        if not user:
            flash("user not found")
            return redirect(url_for('auth.login'))
        if not check_password_hash(user.password, password):
            flash("Incorrect password")
            return redirect(url_for("auth.login"))
        
        login_user(user)
        flash('Login sucessfully')

        # role based redirect
        if user.role == 'admin':
            return redirect(url_for('admin.a_admin'))
        if user.role == 'student':
            return redirect(url_for('student.s_student'))
        if user.role == 'company':
            return redirect(url_for('company.c_company'))
        
        return redirect(url_for("home.landing_page"))

    return render_template('auth/login.html')
      

    