from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, StreamTask, Clip
from forms import LoginForm, RegisterForm, StreamTaskForm, ClipSubmissionForm, UpdateClipForm
from datetime import datetime
from encryption import encrypt_iban, decrypt_iban, mask_iban

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Başarıyla giriş yaptınız!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Geçersiz email veya şifre!', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Bu email adresi zaten kayıtlı!', 'error')
                return render_template('auth/register.html', form=form)
            
            if User.query.filter_by(username=form.username.data).first():
                flash('Bu kullanıcı adı zaten alınmış!', 'error')
                return render_template('auth/register.html', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                full_name=form.full_name.data,
                iban=encrypt_iban(form.iban.data) if form.iban.data else None,
                consent_given=form.consent.data,
                consent_date=datetime.now() if form.consent.data else None,
                consent_ip=request.remote_addr if form.consent.data else None
            )
            db.session.add(user)
            db.session.commit()
            
            flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Registration error: {str(e)}')
            flash('Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'error')
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız!', 'info')
    return redirect(url_for('index'))



@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('clipper_dashboard'))

# Clipper routes
@app.route('/clipper/dashboard')
@login_required
def clipper_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    clips = Clip.query.filter_by(clipper_id=current_user.id).order_by(Clip.created_at.desc()).all()
    total_earnings = sum(clip.earnings for clip in clips if clip.is_paid)
    pending_earnings = sum(clip.earnings for clip in clips if not clip.is_paid and clip.status == 'approved')
    
    # En yeni görevleri getir
    recent_tasks = StreamTask.query.filter_by(is_active=True).order_by(StreamTask.created_at.desc()).limit(5).all()
    
    return render_template('clipper/dashboard.html', 
                         clips=clips, 
                         total_earnings=total_earnings,
                         pending_earnings=pending_earnings,
                         recent_tasks=recent_tasks)

@app.route('/clipper/tasks')
@login_required
def clipper_tasks():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    active_tasks = StreamTask.query.filter(
        StreamTask.is_active == True,
        StreamTask.deadline > datetime.now()
    ).order_by(StreamTask.created_at.desc()).all()
    
    return render_template('clipper/tasks.html', tasks=active_tasks, moment=datetime)

@app.route('/clipper/submit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def submit_clip(task_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    task = StreamTask.query.get_or_404(task_id)
    
    if not task.is_active or task.deadline < datetime.now():
        flash('Bu görev artık aktif değil!', 'error')
        return redirect(url_for('clipper_tasks'))
    
    form = ClipSubmissionForm()
    form.task_id.choices = [(task.id, task.title) for task in [task]]
    form.task_id.data = task_id
    
    if form.validate_on_submit():
        clip = Clip(
            clip_url=form.clip_url.data,
            platform=form.platform.data,
            description=form.description.data,
            clipper_id=current_user.id,
            task_id=task_id
        )
        db.session.add(clip)
        db.session.commit()
        
        flash('Klip başarıyla gönderildi!', 'success')
        return redirect(url_for('clipper_dashboard'))
    
    return render_template('clipper/submit_clip.html', form=form, task=task)

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    tasks = StreamTask.query.order_by(StreamTask.created_at.desc()).all()
    total_tasks = len(tasks)
    active_tasks = len([t for t in tasks if t.is_active])
    
    recent_clips = Clip.query.order_by(Clip.created_at.desc()).limit(10).all()
    total_clips = Clip.query.count()
    
    return render_template('admin/dashboard.html',
                         tasks=tasks,
                         total_tasks=total_tasks,
                         active_tasks=active_tasks,
                         recent_clips=recent_clips,
                         total_clips=total_clips)

@app.route('/admin/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    form = StreamTaskForm()
    if form.validate_on_submit():
        task = StreamTask(
            title=form.title.data,
            stream_url=form.stream_url.data,
            reward_per_1k_views=form.reward_per_1k_views.data,
            deadline=form.deadline.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        
        flash('Görev başarıyla oluşturuldu!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_task.html', form=form)

@app.route('/admin/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    task = StreamTask.query.get_or_404(task_id)
    form = StreamTaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.stream_url = form.stream_url.data
        task.reward_per_1k_views = form.reward_per_1k_views.data
        task.deadline = form.deadline.data
        task.description = form.description.data
        
        db.session.commit()
        flash('Görev başarıyla güncellendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_task.html', form=form, task=task)

@app.route('/admin/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    task = StreamTask.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    flash('Görev başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/submissions')
@login_required
def admin_submissions():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    clips = Clip.query.order_by(Clip.created_at.desc()).all()
    # Decrypt IBANs for admin view
    for clip in clips:
        if clip.clipper.iban:
            clip.clipper.decrypted_iban = decrypt_iban(clip.clipper.iban)
        else:
            clip.clipper.decrypted_iban = None
    return render_template('admin/submissions.html', clips=clips)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    # Decrypt IBANs for admin view
    for user in users:
        if user.iban:
            user.decrypted_iban = decrypt_iban(user.iban)
        else:
            user.decrypted_iban = None
    return render_template('admin/users.html', users=users)

@app.route('/admin/privacy-compliance')
@login_required
def admin_privacy_compliance():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    total_users = User.query.count()
    consented_users = User.query.filter_by(consent_given=True).count()
    encrypted_ibans = User.query.filter(User.iban.isnot(None)).count()
    
    return render_template('admin/privacy-compliance.html', 
                         total_users=total_users,
                         consented_users=consented_users,
                         encrypted_ibans=encrypted_ibans)

@app.route('/admin/update_clip/<int:clip_id>', methods=['POST'])
@login_required
def update_clip(clip_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    clip = Clip.query.get_or_404(clip_id)
    
    view_count = request.form.get('view_count', '0')
    status = request.form.get('status', 'pending')
    is_paid = request.form.get('is_paid') == 'on'
    
    try:
        clip.view_count = int(view_count)
        clip.status = status
        clip.is_paid = is_paid
        clip.calculate_earnings()
        clip.updated_at = datetime.now()
        
        db.session.commit()
        flash('Klip başarıyla güncellendi!', 'success')
    except ValueError:
        flash('Geçersiz görüntüleme sayısı!', 'error')
    
    return redirect(url_for('admin_submissions'))

@app.route('/admin/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('clipper_dashboard'))
    
    task = StreamTask.query.get_or_404(task_id)
    task.is_active = not task.is_active
    db.session.commit()
    
    status = "aktif" if task.is_active else "pasif"
    flash(f'Görev {status} duruma getirildi!', 'success')
    return redirect(url_for('admin_dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', error_message="Sayfa bulunamadı"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', error_message="Bir hata oluştu"), 500
