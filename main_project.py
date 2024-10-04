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
    return render_template("home.html")

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
                return "Correct executing"#redirect(url_for('gestion'))
            else:
                return "Invalid password"
        else:
            return "Invalid username"
    except mysql.connector.Error as err:
        app.logger.error("Error executing query: %s", err)
        return "Error executing query"
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(debug=True)