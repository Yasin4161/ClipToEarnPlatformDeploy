from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, DateTimeField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, NumberRange, EqualTo
from datetime import datetime, timedelta

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Ad Soyad', validators=[DataRequired(), Length(min=2, max=100)])
    iban = StringField('IBAN', validators=[DataRequired(), Length(min=26, max=34)])
    consent = BooleanField('KVKK Onayı', validators=[DataRequired()])
    submit = SubmitField('Kayıt Ol')

class StreamTaskForm(FlaskForm):
    title = StringField('Stream Başlığı', validators=[DataRequired(), Length(max=200)])
    stream_url = StringField('Stream URL', validators=[DataRequired(), URL()])
    reward_per_1k_views = FloatField('1K Görüntüleme Başına Ödül (₺)', validators=[DataRequired(), NumberRange(min=0.01)])
    deadline = DateTimeField('Son Teslim Tarihi', validators=[DataRequired()], default=lambda: datetime.now() + timedelta(days=7))
    description = TextAreaField('Açıklama')

class ClipSubmissionForm(FlaskForm):
    task_id = SelectField('Görev', validators=[DataRequired()], coerce=int)
    clip_url = StringField('Klip URL', validators=[DataRequired(), URL()])
    platform = SelectField('Platform', choices=[('youtube', 'YouTube Shorts'), ('tiktok', 'TikTok'), ('instagram', 'Instagram Reels')], validators=[DataRequired()])
    description = TextAreaField('Açıklama')

class UpdateClipForm(FlaskForm):
    view_count = StringField('Görüntüleme Sayısı', validators=[DataRequired()])
    status = SelectField('Durum', choices=[('pending', 'Beklemede'), ('approved', 'Onaylandı'), ('rejected', 'Reddedildi')], validators=[DataRequired()])
