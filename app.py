"""Blogly application."""
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY']="blogly-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

# ************************************************************
# REDIRECT FROM "/" WILL BE FIXED LATER
# ************************************************************
@app.route('/')
def homepage():
    '''Redirect to list of users'''
    return redirect('/users')

@app.route('/users')
def users_page():
    '''Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form'''
    all_users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', all_users=all_users)

@app.route('/users/new')
def newUser():
    '''Show an add form for users'''
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def do_newUser():
    '''Process the add form, adding a new user and going back to /users'''
    f_name = request.form.get('first')
    l_name = request.form.get('last')
    img_url = request.form.get('image')
    if img_url:
       img_url = img_url
    else:
        img_url = None
    
    newUser = User(first_name=f_name, last_name=l_name, image_url=img_url)
    db.session.add(newUser)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def userDetails(user_id):
    '''Show information about the given user. Have a button to get to their edit page, and to delete the user'''
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def editUser(user_id):
    '''Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.'''
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def do_editUser(user_id):
    '''Process the edit form, returning the user to the /users page.'''
    fname = request.form['first']
    lname = request.form['last']
    img = request.form['image']
    
    user = User.query.get_or_404(user_id)
    user.first_name = fname
    user.last_name = lname
    user.image_url = img
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def do_deleteUser(user_id):
    '''Delete the user.'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")