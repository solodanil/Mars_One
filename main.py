from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
import datetime

from werkzeug.exceptions import abort

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.news import News
from forms.job import JobForm
from forms.users import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/index")
@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    res = []
    for job in jobs:
        if current_user.is_authenticated:
            editable = job.team_leader == current_user.id or current_user.id == 1
        else:
            editable = False
        res.append({
            'description': job.description,
            'collaborators': job.collaborators,
            'duration': job.work_size,
            'team_leader': db_sess.query(User).filter(User.id == job.team_leader).first().name,
            'is_finished': 'is finished' if job.is_finished else 'is not finished',
            'editable': editable
        })
    return render_template("index.html", jobs=res, authorized=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.description = form.description.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.team_leader.data
        job.start_date = datetime.datetime.strptime(form.start_date.data, "%d/%m/%Y %H:%M")
        job.end_date = datetime.datetime.strptime(form.end_date.data, "%d/%m/%Y %H:%M")
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/index')

    return render_template('addjob.html', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter((Jobs.id == id),
                                         ((Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1))
                                         ).first()
        if job:
            form.description.data = job.description
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.team_leader.data = job.team_leader
            form.start_date.data = datetime.datetime.strftime(job.start_date, "%d/%m/%Y %H:%M")
            form.end_date.data = datetime.datetime.strftime(job.end_date, "%d/%m/%Y %H:%M")
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1))
                                         ).first()
        if job:
            job.description = form.description.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.team_leader = form.team_leader.data
            job.start_date = datetime.datetime.strptime(form.start_date.data, "%d/%m/%Y %H:%M")
            job.end_date = datetime.datetime.strptime(form.end_date.data, "%d/%m/%Y %H:%M")
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     ((Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1))
                                     ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")

    app.run(debug=True)


if __name__ == '__main__':
    main()
