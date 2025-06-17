from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
# from app import db, bcrypt
# from app.models import User 
# from app.auth.forms import LoginForm, RegistrationForm 
from app.auth import bp

# Rotas de login, registro, logout virão aqui