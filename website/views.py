from flask import Blueprint, render_template,request,flash,redirect,url_for,send_file,Response
from flask_login import login_required, current_user, login_user, logout_user
from .models import Comment, Tickets,User
from . import db
views = Blueprint('views',__name__)
from datetime import datetime
from io import BytesIO
import pandas as pd
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

@views.route('/admin')
@login_required
def admin():
    if not (current_user.user_type == 'admin'):
        flash("You do not have permission to view this page.", 'error')
        return redirect(url_for('views.home'))
    return render_template('admin.html',user=current_user,tickets = Tickets.query.all()
)


@views.route('/tickets')
@login_required
def tickets():
    return render_template('tickets.html',user=current_user,tickets = Tickets.query.all()
)

@views.route('/new_ticket')
@login_required
def new_ticket():
    return render_template('new_ticket.html',user=current_user,tickets = Tickets.query.all()
)



@views.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('views.login'))  # Redirect to login page if not logged in

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'ticket':
            handle_ticket_form(request)

        return redirect(url_for('views.home'))

    return render_template('base.html', user=current_user)

import random
import string

# Global variables to store the last generated IDs
last_ticket_id = -1
last_comment_id = -1

def generate_random_Ticket_id():
    global last_ticket_id
    last_ticket_id += 1
    return f"T-{last_ticket_id:04}"

def generate_random_Comment_id():
    global last_comment_id
    last_comment_id += 1
    return f"Comment - {last_comment_id:04}"


def handle_ticket_form(request):
    title = request.form.get('title')
    description = request.form.get('description')
    complete_date=request.form.get('complete_date'),   
    ticket_type = request.form.get('ticket_type')
    ticket_priority = request.form.get('ticket_priority')

 
    new_ticket = Tickets(
        id=generate_random_Ticket_id(),  # Generate a random ID for the ticket
        title=title,
        description=description,
        user_id=current_user.id,
        status="New",
        create_date=datetime.now().replace(microsecond=0),
        complete_date=None,
        assigned_to="No one",
        ticket_type=ticket_type,
        ticket_priority=ticket_priority,

    )
    db.session.add(new_ticket)
    db.session.commit()
    flash('Ticket submitted', category='success')

@views.route('/forward/<id>')
def complete(id):
    form_type = request.args.get('form_type', None)

    if request.method == 'GET':
        print(id)
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour, datetime.today().minute, datetime.today().second)

        if form_type == 'tickets':
            db.session.query(Tickets).filter(Tickets.id == id).update({'status': "Completed", 'complete_date': todays_datetime})
            db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user)




# @views.route("/sendemail/<id>/<title>/<category>/<phnumber>/<description>",methods=['POST'])
# def send_email(id,title,category,phnumber,description):
#     if request.method == 'POST':
#         # drop1=request.form.get('drop1')
#         # subject=title
#         # msg=MIMEMultipart()
#         # msg['Subject']=subject
#         # body=" Category: "+category+'\n' +" Pharmacy Number: "+phnumber+'\n'+"Description: "+'\n'+description
#         # msg.attach(MIMEText(body,'plain'))
#         # text=msg.as_string()
#         email=request.form.get('drop1')
        
#         # server=smtplib.SMTP_SSL("smtp.gmail.com",465)
#         # server.login("mohab.elorbany","Mohab@2050")
#         # server.sendmail("Admin",email,text)
#         # server.quit()
#         # print(body)
#         # print (drop1)
#         # flash('Email Sent successfully',category='success')
#         db.session.query(Tickets).filter(Tickets.id==id).update({'assigned_to':email })
#         db.session.commit()

#         return redirect(url_for('views.admin'))
    

#     return render_template('admin.html', user=current_user)



@views.route('/ticket/<string:ticket_id>', methods=['GET', 'POST'])
def ticket_details(ticket_id):
    ticket = Tickets.query.get(ticket_id)

    if not ticket:
        flash('Ticket not found.')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        content = request.form.get('comment_content')
        ticket_priority = request.form.get('ticket_priority')
        assign_admin = request.form.get('assign_admin')

        if content:
            # Create a new comment
            new_comment = Comment(
                id=generate_random_Comment_id(),
                content=content,
                create_date=datetime.now().replace(microsecond=0),
                ticket_id=ticket.id,
                user_id=current_user.id,
                user_fname=current_user.first_name  # Set user_fname to current_user.first_name
            )
            db.session.add(new_comment)

        if ticket_priority:
            ticket.ticket_priority = ticket_priority

        if assign_admin:
            # Assign ticket to the selected admin user
            admin_user = User.query.get(assign_admin)
            if admin_user and admin_user.user_type == 'admin':
                ticket.assigned_to = admin_user.first_name

        db.session.commit()
        flash('Changes saved successfully.', category='success')
        return redirect(url_for('views.ticket_details', ticket_id=ticket_id))

    comments = Comment.query.filter_by(ticket_id=ticket_id).all()
    admin_users = User.query.filter_by(user_type='admin').all()
    return render_template('tickets_details.html', user=current_user, ticket=ticket, comments=comments, admin_users=admin_users)

# ... (existing code)



@views.route("/download/<string:ticket_id>")
def download(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    
    if not ticket or not ticket.img:
        flash('Ticket image not found.', category='error')
        return redirect(url_for('views.home'))
    
    return send_file(BytesIO(ticket.img), attachment_filename='download.png', as_attachment=True)



# Add a new route for editing a ticket
@views.route('/edit_ticket/<string:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('views.tickets'))

    if request.method == 'POST':
        ticket.title = request.form.get('title')
        ticket.description = request.form.get('description')
        ticket.phnumber = request.form.get('phnumber')
        # Update other fields as needed

        # Update the attachment if a new file is provided
        if 'inputFile' in request.files:
            new_attachment = request.files['inputFile']
            if new_attachment:
                ticket.img = new_attachment.read()

        db.session.commit()
        flash('Ticket updated successfully.', category='success')
        return redirect(url_for('views.admin'))

    return render_template('edit_ticket.html', user=current_user, ticket=ticket)



# Add a new route for deleting a ticket
@views.route('/delete_ticket/<string:ticket_id>', methods=['GET', 'POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('views.admin'))

    if request.method == 'POST':
        db.session.delete(ticket)
        db.session.commit()
        flash('Ticket deleted successfully.', category='success')
        return redirect(url_for('views.admin'))

    return render_template('delete_ticket.html', user=current_user, ticket=ticket)



# ... other routes ...

@views.route('/update_status/<string:ticket_id>', methods=['POST'])
@login_required
def update_status(ticket_id):
    ticket = Tickets.query.get(ticket_id)

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('views.admin'))

    new_status = request.form.get('new_status')

    if new_status == 'In Progress':
        if ticket.status == 'New':
            ticket.status = new_status
            db.session.commit()
            flash('Ticket status updated to In Progress.', category='success')
        elif ticket.status == 'In Progress':
            ticket.status = 'Completed'
            ticket.complete_date = datetime.now().replace(microsecond=0)
            db.session.commit()
            flash('Ticket status updated to Completed.', category='success')
        else:
            flash('Ticket is already Completed.', category='info')

    return redirect(url_for('views.admin'))















@views.route('/login',methods=['GET','POST'])
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


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))







@views.route('/signup',methods=['GET','POST'])
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

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


from werkzeug.security import generate_password_hash, check_password_hash

@views.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', category='error')
        return redirect(url_for('views.users'))

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
        return redirect(url_for('views.users'))

    return render_template('edit_user.html', user=user)



@views.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', category='error')
        return redirect(url_for('views.users'))

    if request.method == 'POST':
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        flash('User deleted successfully!', category='success')
        return redirect(url_for('views.users'))

    return render_template('delete_user.html', user=user)




# Existing imports ...

@views.route('/ticket/<string:ticket_id>/update-details', methods=['POST'])
@login_required
def update_ticket_details(ticket_id):
    ticket = Tickets.query.get(ticket_id)

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        ticket_priority = request.form.get('ticket_priority')
        assign_admin = request.form.get('assign_admin')
        content = request.form.get('comment_content')

        if content:
            # Create a new comment
            new_comment = Comment(
                id=generate_random_Comment_id(),
                content=content,
                create_date=datetime.now().replace(microsecond=0),
                ticket_id=ticket.id,
                user_id=current_user.id,
                user_fname=current_user.first_name
            )
            db.session.add(new_comment)

        if ticket_priority:
            ticket.ticket_priority = ticket_priority

        if assign_admin:
            # Assign ticket to the selected admin user
            admin_user = User.query.get(assign_admin)
            if admin_user and admin_user.user_type == 'admin':
                ticket.assigned_to = admin_user.first_name
            elif assign_admin == '':  # Unassign if an empty value is selected
                ticket.assigned_to = None

        db.session.commit()
        flash('Changes saved successfully.', category='success')
        return redirect(url_for('views.ticket_details', ticket_id=ticket_id))

    comments = Comment.query.filter_by(ticket_id=ticket_id).all()
    admin_users = User.query.filter_by(user_type='admin').all()
    return render_template('ticket_details.html', user=current_user, ticket=ticket, comments=comments, admin_users=admin_users)
