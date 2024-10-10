from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt
import logging

app = Flask(__name__)
app.secret_key='admin'
app.logger.setLevel(logging.DEBUG)

username = 'root'
password = '12345'
host = 'localhost'
database = 'biblioteca'

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

@app.route("/")
def index():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
    username = request.form["user_name"]
    password = request.form["contraseña"]
    
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

@app.route("/log_out")
def log_out():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route("/home")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template("home.html")

@app.route("/gestion")
def gestion():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template("gestion.html")
@app.route("/gestionar", methods=["POST"])
def gestionar():
    title = request.form.get("titulo")
    author = request.form.get("autor")
    genr = request.form.get("genero")
    editorial = request.form.get("editorial")
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
    finally:
        cursor.close()

@app.route("/registrarse")
def registrarse():
    return render_template("sign_up.html")
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

if __name__ == "__main__":
    app.run(debug=True)