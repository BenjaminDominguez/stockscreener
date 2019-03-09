from app.auth import bp
from app.auth.forms import RegisterForm, LoginForm
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from app import db
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Email does not exist")
            return redirect(url_for('auth.login'))
        elif not user.check_password(form.password.data):
            flash("Incorrect password")
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')
