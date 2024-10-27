from flask import Blueprint, redirect, url_for, session, request, render_template, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # For development: accept any username/password
        if username and password:
            session['user'] = {'username': username}
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Please enter both username and password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))
