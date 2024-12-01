import os
import json
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm, EditProfileForm, OlympiadRegistrationForm
from app.db.archive.models import OlympiadRegistration, Student, User, Olympiad
from app.db.database import db

# Проверка разрешенных форматов файлов
def allowed_file(filename):
    """Проверка, что файл имеет разрешенное расширение."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Сохранение фотографии пользователя
def save_profile_picture(file, user_id):
    """Сохраняет фотографию профиля в папке app/static/images/profile_pics/<user_id>."""
    try:
        max_size = 2 * 1024 * 1024  # 2 MB
        if file.content_length > max_size:
            raise ValueError('Размер файла превышает допустимый предел (2 MB).')

        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
        os.makedirs(user_folder, exist_ok=True)

        # Удаляем старую фотографию, если она есть
        for existing_file in os.listdir(user_folder):
            file_path = os.path.join(user_folder, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        # Возвращаем относительный путь для записи в базу данных
        relative_path = os.path.relpath(file_path, 'app')
        return relative_path
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f'Ошибка сохранения файла: {e}')

# Загрузка данных из базы данных вместо JSON
def load_olympiads_from_db():
    """Загружает все олимпиады из базы данных."""
    return Olympiad.query.all()

# Инициализация маршрутов
def init_routes(app):
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'images', 'profile_pics')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            flash('Вы уже вошли в систему.', 'info')
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            flash('Неправильное имя пользователя или пароль.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            flash('Вы уже зарегистрированы и вошли в систему.', 'info')
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash('Пользователь с таким email уже существует.', 'danger')
                return redirect(url_for('register'))

            try:
                new_user = User(email=form.email.data, role='student')
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()

                file = request.files.get('photo')
                if file and allowed_file(file.filename):
                    photo_path = save_profile_picture(file, new_user.id)
                    new_user.photo = photo_path
                    db.session.commit()

                flash('Регистрация прошла успешно. Теперь вы можете войти в систему.', 'success')
                return redirect(url_for('login'))
            except ValueError as ve:
                flash(f'Ошибка при загрузке фотографии: {ve}', 'danger')
            except Exception as e:
                flash(f'Ошибка при регистрации: {e}', 'danger')
                db.session.rollback()

        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы успешно вышли из системы.', 'success')
        return redirect(url_for('index'))

    @app.route('/profile/<int:student_id>')
    @login_required
    def profile(student_id):
        student = Student.query.get_or_404(student_id)
        return render_template('profile.html', student=student)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm()
        if form.validate_on_submit():
            try:
                current_user.email = form.email.data

                file = request.files.get('photo')
                if file and allowed_file(file.filename):
                    photo_path = save_profile_picture(file, current_user.id)
                    current_user.photo = photo_path

                db.session.commit()
                flash('Профиль успешно обновлен!', 'success')
                return redirect(url_for('profile', student_id=current_user.id))
            except ValueError as ve:
                flash(f'Ошибка при загрузке фотографии: {ve}', 'danger')
            except Exception as e:
                flash(f'Ошибка обновления профиля: {e}', 'danger')
                db.session.rollback()

        return render_template('edit_profile.html', form=form)

    @app.route('/olympiads')
    def olympiads():
        try:
            olympiads = load_olympiads_from_db()
            return render_template('olympiads.html', olympiads=olympiads)
        except Exception as e:
            flash(f'Ошибка загрузки олимпиад: {e}', 'danger')
            return redirect(url_for('index'))

    @app.route('/register_olympiad/<int:olympiad_id>', methods=['GET', 'POST'])
    @login_required
    def register_olympiad(olympiad_id):
        olympiad = Olympiad.query.get_or_404(olympiad_id)

        form = OlympiadRegistrationForm()
        if form.validate_on_submit():
            if OlympiadRegistration.query.filter_by(student_id=current_user.id, olympiad_id=olympiad_id).first():
                flash('Вы уже зарегистрированы на эту олимпиаду!', 'warning')
                return redirect(url_for('olympiads'))

            try:
                new_registration = OlympiadRegistration(student_id=current_user.id, olympiad_id=olympiad_id)
                db.session.add(new_registration)
                db.session.commit()
                flash('Вы успешно зарегистрировались на олимпиаду!', 'success')
                return redirect(url_for('olympiads'))
            except Exception as e:
                flash(f'Ошибка при регистрации на олимпиаду: {e}', 'danger')
                db.session.rollback()

        return render_template('register_olympiad.html', olympiad=olympiad, form=form)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
