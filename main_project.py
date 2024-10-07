from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt
import logging

app = Flask(__name__)
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
    app.logger.error("Error connecting to MySQL: %s", err)
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
                return redirect(url_for('gestion'))
            else:
                app.logger.error("Incorret password, try again!")
                return "Invalid password"
        else:
            return "Invalid username"
    except mysql.connector.Error as err:
        app.logger.error("Error executing query: %s", err)
        return "Error executing query"
    finally:
        cursor.close()

@app.route("/gestion")
def gestion():
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
        app.logger.error("Error: Missing required fields")
        return "Error: Please fill in all required fields"
    try:
        cursor = mysql_conn.cursor()
        query = "INSERT INTO libro (titulo, autor, genero, editorial, sinopsis, fecha_publicacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, author, genr, editorial, synopsis, date, status))
        mysql_conn.commit()
        app.logger.info("Book added successfully")
        return "Libro agregado con éxito"
    except mysql.connector.Error as error:
        app.logger.error("Error executing query: %s", error)
        return "Error executing query"
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
        app.logger.error("Error: Missing required fields")
        return "Error: Please fill in all required fields"
    try:
        if pw != pw2:
            app.logger.error("Error: Passwords do not match")
            return "Error: Passwords do not match"
        else:
            hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt(12))
            cursor = mysql_conn.cursor()
            query = "INSERT INTO usuario (nombre, apellido, user_name, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, lastname, un, email, hashed_pw))
            mysql_conn.commit()
            app.logger.info("User  registered successfully")
            return redirect(url_for('index'))    
    except mysql.connector.Error as err:
        app.logger.error("Error executing query: %s", err)
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(debug=True)