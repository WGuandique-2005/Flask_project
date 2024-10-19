from flask import *
import pymysql
import bcrypt
import logging
import os
from functools import *

app = Flask(__name__)
app.secret_key = '1234'
app.logger.setLevel(logging.DEBUG)

usuario = 'root'
contrasena = 'root'
host = 'localhost'
base_datos = 'biblioteca'

def get_db_connection():
    try:
        return pymysql.connect(
            user=usuario,
            password=contrasena,
            host=host,
            database=base_datos
        )
    except pymysql.MySQLError as err:
        app.logger.error("Error al conectar con MySQL: %s", err)
        exit(1)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre_usuario = request.form["user_name"]
        contrasena = request.form["contraseña"]

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                consulta = "SELECT contraseña FROM usuario WHERE user_name = %s"
                cursor.execute(consulta, (nombre_usuario,))
                resultado = cursor.fetchone()
                if resultado:
                    contrasena_hash = resultado[0].encode('utf-8')
                    if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hash):
                        session['logged_in'] = True
                        return redirect(url_for('home')) 
                    else:
                        app.logger.error("Contraseña incorrecta, inténtalo de nuevo!")
                        return render_template("login.html", error="Contraseña incorrecta") 
                else:
                    return render_template("login.html", error="Nombre de usuario incorrecto")  
        except pymysql.MySQLError as err:
            app.logger.error("Error al ejecutar la consulta: %s", err)
            return render_template("login.html", error="Error al ejecutar la consulta")
        finally:
            connection.close()
    
    return render_template("login.html") 

@app.route("/log_out")
def log_out():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/gestion")
@login_required
def gestion():
    return render_template("gestion.html")

@app.route("/gestionar", methods=["POST"])
@login_required
def gestionar():
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    genero = request.form.get("genero")
    editorial = request.form.get("editorial")
    sinopsis = request.form.get("sinopsis")
    fecha_publicacion = request.form.get("fecha_publicacion")
    estado = request.form.get("estado")

    if not all([titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado]):
        app.logger.error("Error: Faltan campos obligatorios")
        return render_template("gestion.html", error="Por favor completa todos los campos obligatorios")
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            consulta = "INSERT INTO libro (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta, (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado))
            connection.commit()
            app.logger.info("Libro agregado con éxito")
            return redirect(url_for('home'))
    except pymysql.MySQLError as error:
        app.logger.error("Error al ejecutar la consulta: %s", error)
        return render_template("gestion.html", error="Error al ejecutar la consulta")
    finally:
        connection.close()

@app.route("/registrarse")
def registrarse_U():
    return render_template("sign_up.html")

@app.route("/sign_up", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        nombre_usuario = request.form.get("user_name")
        correo = request.form.get("correo")
        contrasena = request.form.get("password")
        contrasena2 = request.form.get("re_pw")

        if not all([nombre, apellido, nombre_usuario, correo, contrasena, contrasena2]):
            app.logger.error("Error: Faltan campos obligatorios")
            return render_template("sign_up.html", error="Por favor completa todos los campos obligatorios")

        if contrasena != contrasena2:
            app.logger.error("Error: Las contraseñas no coinciden")
            return render_template("sign_up.html", error="Las contraseñas no coinciden")

        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt(12))

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                consulta = "INSERT INTO usuario (nombre, apellido, user_name, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(consulta, (nombre, apellido, nombre_usuario, correo, contrasena_hash))
                connection.commit()
                app.logger.info("Usuario registrado con éxito")
                return redirect(url_for('login'))
        except pymysql.MySQLError as err:
            app.logger.error("Error al ejecutar la consulta: %s", err)
            return render_template("sign_up.html", error="Ocurrió un error al registrar al usuario")
        finally:
            connection.close()

    return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(debug=True)
