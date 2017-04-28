"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask_wtf import FlaskForm
from flask import render_template, request, redirect, url_for, jsonify,flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from wtforms import TextField, Form, IntegerField, SelectField, validators, PasswordField, ValidationError
from bs4 import BeautifulSoup
import requests
import urlparse
import thumbScrape

from app import db
from app.Models import User

@app.route('/')
def home():
    return render_template('home.html')

class RegisterForm(FlaskForm):
    email = TextField('email', [validators.Required()])
    password = PasswordField('password', [validators.Required()])
    name = TextField('name', [validators.Required()])
    age = IntegerField('age', [validators.Required()])
    gender = SelectField('gender',choices=[('male', 'Male'), ('female','Female')])

class loginForm(FlaskForm):
    email = TextField('E-mail',[validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    
    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count()>0:
            raise ValidationError('Duplicate username')
   
@app.route('/api/users/register', methods=['POST', 'GET'])
def register():
    """route to register a new user"""
    form = RegisterForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            image = request.form['image']
            newUser = User(email, password, name, age, gender, image)
            db.session.add(newUser)
            db.session.commit()
        flash('New user has been registered successfully', 'success')
    return render_template('register.html', form=form)
    

@app.route('/api/users/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wishlist'))
    
    form = loginForm()
    if form.validate_on_submit():
        
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email,password=password)\
        .first()
        
        if user is not None:
            login_user(User)
            flash('user logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('Email address or password is incorrect', 'danger')
    return render_template('login.html', form=form)

@app.route('/api/users/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))
    
@app.route('/api/users/{userid}/wishlist', methods=['POST', 'GET'])
@login_required
def wishlist(userid):
    if request.method=='POST':
        user = User.query.filter_by(id=userid).first()
        if user:
            title = request.form.get('title')
            description = request.form.get('description')
            url = request.form.get('url')
            
            wishlist = User.wishlist
        else:
            return redirect(url_for('home'))
            
            
    elif request.method == 'GET':
        return render_template('wishlist.html')
    else:
        return redirect(url_for('home'))

#@app.route('/api/thumbnails', methods=['GET'])

#@app.route('api/users/{userid}/wishlist/{itemid}', methods = ['DELETE'])


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
