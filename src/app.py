from config import config
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
import logging
# Entities:
from models.entities.User import User
# Models:
from models.ModelUser import ModelUser

app = Flask(__name__, static_folder='static')
app.secret_key = '42a835aa17930776f53f10d010b108ca'  # Set a secret key for CSRF protection
csrf = CSRFProtect(app)

db=MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'  # Especifica la vista de login
login_manager_app.login_message = 'Por favor inicie sesión para acceder a esta página'
login_manager_app.login_message_category = 'warning'
login_manager_app.session_protection = "strong"


# @login_manager_app.user_loader
# def load_user(id):
#     return ModelUser.get_by_id(db, id)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)  # Solo pasamos el id



@app.route('/')
def index():
    return redirect(url_for('login'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # print(request.form['username'])
#         # print(request.form['password'])
#         user = User(0, request.form['username'], request.form['password'])
#         logged_user = ModelUser.login(user)
#         print(logged_user)
#         if logged_user != None:
#             if logged_user.password:
#                 login_user(logged_user)
#                 return redirect(url_for('home'))
#             else:
#                 flash("Invalid password...")
#                 return render_template('auth/login.html')
#         else:
#             flash("User not found...")
#             return render_template('auth/login.html')
#     else:
#         return render_template('auth/login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Creas el objeto User con el username y password proporcionados
        user = User(0, username, password)  # No necesitas un id para la autenticación

        # Intentas obtener al usuario mediante el modelo
        logged_user = ModelUser.login(user)

        if logged_user is not None:
            # Si el usuario fue encontrado y la contraseña es correcta, se inicia sesión
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            # Si no se encuentra al usuario o la contraseña es incorrecta, se muestra un mensaje de error
            flash("Usuario o contraseña incorrectos...")
            return render_template('auth/login.html')

    else:
        # Si la solicitud es GET, solo renderiza la página de login
        return render_template('auth/login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/looker-studio')
def looker_studio():
    return render_template('Looker-studio.html')

@app.route('/scraping')
def scraping():
    return render_template('scraping.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401,status_401)
    app.register_error_handler(401,status_401)
    csrf.init_app(app)
    app.run()

logging.basicConfig(
    filename='app.log',  
    level=logging.DEBUG,  # Nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Prueba de log
logging.info("La aplicación Flask ha iniciado correctamente.")

