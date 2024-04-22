# Para essa questão reolvi adaptar o codigo da questão 3

from flask import Flask, request, jsonify
import mysql.connector
import bcrypt

app = Flask(__name__)

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NBHL84ownD6ihT",
    database="GeekStore"
)
cursor = mydb.cursor()

# Lambda para criar tabela de usuários
create_users_table = lambda : cursor.execute(
    "CREATE TABLE IF NOT EXISTS USERS ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "username VARCHAR(255), "
    "password VARCHAR(255), "
    "country VARCHAR(255), "
    "id_console INT)"
)

# Lambda para criar tabela de consoles
create_videogames_table = lambda : cursor.execute(
    "CREATE TABLE IF NOT EXISTS VIDEOGAMES ("
    "id_console INT AUTO_INCREMENT PRIMARY KEY, "
    "name VARCHAR(255), "
    "id_company INT, "
    "release_date DATE)"
)

# Lambda para criar tabela de jogos
create_games_table = lambda : cursor.execute(
    "CREATE TABLE IF NOT EXISTS GAMES ("
    "id_game INT AUTO_INCREMENT PRIMARY KEY, "
    "title VARCHAR(255), "
    "genre VARCHAR(255), "
    "release_date DATE, "
    "id_console INT)"
)

# Lambda para criar tabela de empresas
create_company_table = lambda : cursor.execute(
    "CREATE TABLE IF NOT EXISTS COMPANY ("
    "id_company INT AUTO_INCREMENT PRIMARY KEY, "
    "name VARCHAR(255), "
    "country VARCHAR(255))"
)

create_tables = lambda : [
    func()
    for func in (create_users_table, create_videogames_table, create_games_table, create_company_table)
]
create_tables()

# Funções para criptografia de senhas
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# CRUD para USERS
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    get_user = lambda: cursor.execute("SELECT id, username, country FROM USERS WHERE id = %s", (user_id,))
    get_user()
    user = cursor.fetchone()
    if user:
        return jsonify({'id': user[0], 'username': user[1], 'country': user[2]}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    country = request.json['country']
    password_hash = hash_password(password)
    insert_user = lambda: (
        cursor.execute("INSERT INTO USERS (username, password, country) VALUES (%s, %s, %s)", 
                       (username, password_hash, country)), 
        mydb.commit()
    )
    insert_user()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    username = request.json.get('username')
    country = request.json.get('country')
    update_query = "UPDATE USERS SET "
    update_params = []
    if username:
        update_query += "username = %s,"
        update_params.append(username)
    if country:
        update_query += "country = %s,"
        update_params.append(country)
    update_query = update_query.rstrip(',')
    update_query += " WHERE id = %s"
    update_params.append(user_id)
    update_user = lambda: (cursor.execute(update_query, tuple(update_params)), mydb.commit())
    update_user()
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_user = lambda: (cursor.execute("DELETE FROM USERS WHERE id = %s", (user_id,)), mydb.commit())
    delete_user()
    return jsonify({'message': 'User deleted successfully'}), 200

# CRUD para VIDEOGAMES

if __name__ == '__main__':
    app.run(debug=True)
