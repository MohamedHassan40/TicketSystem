from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import  User
from . import db
from flask_login import login_user, login_required,logout_user, current_user
auth = Blueprint('auth',__name__)
from werkzeug.security import generate_password_hash,check_password_hash


SESSION_SQLALCHEMY = db

@auth.route('/login',methods=['GET','POST'])
def login():
   if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # print(user)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.user_type=="admin":
                    return redirect(url_for('views.admin'))
                else:
                            
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')


   return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/home')
def home():
    return render_template('home.html')




@auth.route('/signup',methods=['GET','POST'])
# @login_required

def sign_up():

    if request.method=='POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type= request.form.get('user_type')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 7 characters.', category='error')
        elif len(user_type)<1:
            flash('User type must be selected',category='error')
        else:
             new_user = User(email=email, first_name=first_name,user_type=user_type, password=generate_password_hash(
                password1, method='sha256'))
             db.session.add(new_user)
             db.session.commit()
             flash('Account created!', category='success')


            #  login_user(user, remember=True)



    return render_template('sign_up.html',user=current_user)


# auth.py.

@auth.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', category='error')
        return redirect(url_for('auth.users'))

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')

        # Update the user details
        user.email = email
        user.first_name = first_name

        if password:
            # Hash the new password
            hashed_password = generate_password_hash(password, method='sha256')
            user.password = hashed_password

        db.session.commit()

        flash('User details updated successfully!', category='success')
        return redirect(url_for('auth.users'))

    return render_template('edit_user.html', user=user)



@auth.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', category='error')
        return redirect(url_for('auth.users'))

    if request.method == 'POST':
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        flash('User deleted successfully!', category='success')
        return redirect(url_for('auth.users'))

    return render_template('delete_user.html', user=user)
