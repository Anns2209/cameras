from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from dotenv import load_dotenv
from flask_selfdoc import Autodoc
import os
from flask import send_from_directory


# Nalozi okoljske spremenljivke iz .env datoteke
load_dotenv()

# Pridobi spremenljivke iz okolja
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)
auto = Autodoc(app)

# Povezava z bazo
try:
    db_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
except mysql.connector.Error as err:
    print(f"Napaka pri povezovanju na bazo: {err}")
    db_connection = None

# Funkcija za iskanje uporabnika po imenu
def get_user_by_username(username):
    if not db_connection:
        return None
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

# Registracija
@app.route('/register', methods=['POST'])
@auto.doc()
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if get_user_by_username(username):
        return jsonify({"msg": "Username already exists"}), 400

    password_hash = generate_password_hash(password)
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                   (username, password_hash, email))
    db_connection.commit()
    cursor.close()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = get_user_by_username(username)
    print("Uporabnik iz baze:", user)

    #  Tukaj popravek: user['password_hash'] namesto user[0]
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# API z informacijami (dostopno brez prijave)
@app.route('/api/info', methods=['GET'])
@auto.doc()
def api_info():
    return jsonify({"message": "Ana Gjorcheska, 164.8.67.103"}), 200


@app.route('/getKamere', methods=['GET'])
@jwt_required()
def get_kamere():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT title, latitude, longitude, image_link FROM kamere")  # tabela najbrž ni users
    kamere = cursor.fetchall()
    cursor.close()
    return jsonify(kamere)


#API za temperaturo (zasciten z JWT)
@app.route('/getTemp', methods=['GET'])
@jwt_required()
def get_temp():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT source_name, latitude, longitude, air_temperature FROM weather_data")
    temperature_data = cursor.fetchall()
    cursor.close()
    return jsonify(temperature_data)

# Dostop do dokumentacije
@app.route('/documentation')
def documentation():
    return auto.html()



# Zagon aplikacije
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
