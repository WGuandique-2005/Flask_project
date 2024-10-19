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

<<<<<<< HEAD
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

=======
try:
    mysql_conn = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
except mysql.connector.Error as err:
    app.logger.error("Error de conexión a MySQL: %s", err)
    exit(1)

>>>>>>> 3881961036b5956677748d22f8dcc8b518aeb632
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
    
<<<<<<< HEAD
    return render_template("login.html") 
=======
    try:
        cursor = mysql_conn.cursor()
        query = "SELECT contraseña FROM usuario WHERE user_name = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            hashed_password = result[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                app.logger.error("Contraseña incorrecta, intente de nuevo!")
                return "Contraseña invalida"
        else:
            return "Nombre de usuario invalido"
    except mysql.connector.Error as err:
        app.logger.error("Error en la ejecución: %s", err)
        return "Error en la ejecución"
    finally:
        cursor.close()
>>>>>>> 3881961036b5956677748d22f8dcc8b518aeb632

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
<<<<<<< HEAD
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
=======
    synopsis = request.form.get("sinopsis")
    date = request.form.get("fecha_publicacion")
    status = request.form.get("estado")
        
    if not all([title, author, genr, editorial, synopsis, date, status]):
        app.logger.error("Error: Campos necesarios vacíos")
        return "Error: Porfavor llene todos los campos"
    try:
        cursor = mysql_conn.cursor()
        query = "INSERT INTO libro (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, author, genr, editorial, synopsis, date, status))
        mysql_conn.commit()
        app.logger.info("Libro agregado con éxito")
        return "Libro agregado con éxito"
    except mysql.connector.Error as error:
        app.logger.error("Error en la ejecución: %s", error)
        return "Error en la ejecución"
>>>>>>> 3881961036b5956677748d22f8dcc8b518aeb632
    finally:
        connection.close()

@app.route("/registrarse")
def registrarse_U():
    return render_template("sign_up.html")
<<<<<<< HEAD

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
=======
@app.route("/sign_up", methods=["POST"])
def reg():
    name = request.form.get("nombre")
    lastname = request.form.get("apellido")
    un = request.form.get("user_name")
    email = request.form.get("correo")
    pw = request.form.get("password")
    pw2 = request.form.get("re_pw")
    
    if not all([name, lastname, un, email, pw, pw2]):
        app.logger.error("Error: Campos necesarios vacíos")
        return "Error: Porfavor llene todos los campos"
    try:
        if pw != pw2:
            app.logger.error("Error: La contraseña no coincide")
            return "Error: La contraseña no coincide"
        else:
            hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt(12))
            cursor = mysql_conn.cursor()
            query = "INSERT INTO usuario (nombre, apellido, user_name, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, lastname, un, email, hashed_pw))
            mysql_conn.commit()
            app.logger.info("Usuario registrado correctamenete!")
            return redirect(url_for('index'))    
    except mysql.connector.Error as err:
        app.logger.error("Error en la ejecución: %s", err)
    finally:
        cursor.close()
>>>>>>> 3881961036b5956677748d22f8dcc8b518aeb632

if __name__ == "__main__":
    app.run(debug=True)
