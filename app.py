
"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, getJoin, User, Feedback, make_db, seed_db
from forms import FeedbackForm, UserForm, LoginForm
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback' #use this for production
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-test' #use this for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'bythepowerofgreyskull'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    """Redirect to register"""
    return redirect('/register')


@app.route('/register', methods = ['GET', 'POST'])
def adduser():
    
    """Adds new user and redirects back"""
    
    form = UserForm()

    if form.validate_on_submit():
        uname=form.username.data
        firstn=form.first_name.data
        lastn=form.last_name.data
        passwd=form.password.data
        email=form.email.data

        registration = User.add(uname, passwd, email, firstn, lastn)
        if registration['successful']:
            flash("New account created succesfully!", "success")
            session['username'] = registration['user'].username
            session['name'] = f"{registration['user'].first_name} {registration['user'].last_name}"
            return redirect(f"/users/{registration['user'].username}", code=302)
        else:
            return "Something went wrong with registration"  #TODO: handle this better

    else:
        form = UserForm()
        return render_template('register.html', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login_user():

    form = LoginForm()

    if form.validate_on_submit():
        uname=form.username.data
        passwd=form.password.data

        authenticated = User.login(uname, passwd)
        if not authenticated:
            flash('Login failed!', "warning")
            return render_template("login.html", form = form)
        else:
            session['username'] = authenticated.username
            session['name'] = f"{authenticated.first_name} {authenticated.last_name}"
            flash("Login successful", "success")
            return redirect(f"/users/{authenticated.username}")         
    else:
        return render_template("login.html", form = form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    session.pop('name')
    return redirect("/")


@app.route('/users/<username>')
def show_user(username):
    """Shows user information"""
    if 'username' in session and session['username'] == username:
        user = User.query.filter_by(username = username).first()
        feedback = Feedback.query.filter_by(contributor = username).all()
        return render_template('showuser.html',user = user, feedback=feedback)
    else:
        flash('Get an account first', "warning")
        return redirect('/')


@app.route('/users/<username>/delete')
def delete(username):
    if 'username' in session and session['username'] == username:
        User.delete_user(username)
        session.pop('username')
        flash("Sorry to see you go. Bye!", 'primary')
        return redirect('/')
    else:
        flash("Now you know you can't do that!  Think about what you have done.", "danger")
        return redirect('/')


@app.route('/users/<username>/feedback/add')
def show_Feedback_form(username):
    """displays a form to add a feedback"""

    if 'username' in session and session['username'] == username:
        form = FeedbackForm()
    
        usr = User.query.get_or_404(username)
        return render_template('add_feedback.html', form=form, user=username, firstname=usr.first_name, lastname=usr.last_name)
    else:
        flash("Access denied", "danger")
        return redirect('/')



@app.route('/users/<username>/feedback/new', methods = ['POST'])
def add_new_Feedback(username):
    """ Adds a new Feedback to the database """
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        newFeedbackID = Feedback.add(ftitle=title, fcontent=content, fcontributor=username)

        return redirect(f'/users/{username}')
    else:
        usr = User.query.get_or_404(username)
        return render_template('add_feedback.html', form=form, user=username, firstname=usr.first_name, lastname=usr.last_name)


@app.route('/Feedback/<int:feedbackid>/update', methods = ['GET', 'POST'])
def edit_Feedback(feedbackid):
    """update a Feedback in the database"""
    select = getJoin(fields=(*Feedback.all, User.first_name, User.last_name), joinTable=User, filter=(Feedback.id==feedbackid)).first()

    # import pdb
    # pdb.set_trace()

    if select.contributor != session['username']:
        flash("Uncontributorised to edit that Feedback", "danger")
        return redirect("/")


    form=FeedbackForm(obj=select)
    if form.validate_on_submit():
        Feedback.edit_Feedback(Feedbackid, request=request)
        return redirect(f'/Feedback/{Feedbackid}')
    else:
        return render_template('edit_Feedback.html', form=form, Feedback=select)


@app.route('/Feedback/<int:feedback_id>/delete', methods = ["POST"])
def delete_Feedback(feedback_id):
    """Delete a Feedback"""

    Feedback = Feedback.query.get_or_404(feedback_id)
    uid = Feedback.contributor

    if 'username' not in session:
        flash("please login first", "warning")
        return redirect('/login')
    if uid == session['username']:
        Feedback.delete_Feedback(feedback_id)
        return redirect(f'/users/{uid}')
    else:
        flash("You are not contributorized to remove that Feedback.", "danger")
        return redirect("/")

