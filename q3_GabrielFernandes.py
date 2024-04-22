import mysql.connector

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NBHL84ownD6ihT",
    database="GeekStore"
)

cursor = mydb.cursor()
# Criando banco de dados questão 3
createdb = lambda : cursor.execute("CREATE DATABASE IF NOT EXISTS GeekStore")

# Lambda para criar tabela de usuários
create_users_table = lambda : cursor.execute(
    "CREATE TABLE IF NOT EXISTS USERS ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "name VARCHAR(255), "
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
    for func in (createdb, create_users_table, create_videogames_table, create_games_table, create_company_table)
]
create_tables()

# Funções lambda para insersão de dados
insert_new_user = lambda user_data: (
    cursor.execute("INSERT INTO USERS (name, country, id_console) VALUES (%s, %s, %s)", (user_data[0], user_data[1], user_data[2])), 
    mydb.commit()
)
insert_new_videogame = lambda videogame_data: (
    cursor.execute("INSERT INTO VIDEOGAMES (name, id_company, release_date) VALUES (%s, %s, %s)", (videogame_data[0], videogame_data[1], videogame_data[2])),
    mydb.commit()
)
insert_new_game = lambda game_data: (
    cursor.execute("INSERT INTO GAMES (title, genre, release_date, id_console) VALUES (%s, %s, %s, %s)", (game_data[0], game_data[1], game_data[2], game_data[3])), 
    mydb.commit()
)
insert_new_company = lambda company_data: (
    cursor.execute("INSERT INTO COMPANY (name, country) VALUES (%s, %s)", (company_data[0], company_data[1])), 
    mydb.commit()
)

# Funções lambda para seleção de dados
select_and_print_all_users = lambda: (
    cursor.execute("SELECT * FROM USERS"),
    [print(row) for row in cursor.fetchall()]
)

select_and_print_user_by_id = lambda user_id: (
    cursor.execute("SELECT * FROM USERS WHERE id = %s", (user_id,)),
    [print(row) for row in cursor.fetchall()]
)

select_and_print_all_videogames = lambda: (
    cursor.execute("SELECT * FROM VIDEOGAMES"),
    [print(row) for row in cursor.fetchall()]
)

select_and_print_videogame_by_id = lambda videogame_id: (
    cursor.execute("SELECT * FROM VIDEOGAMES WHERE id_console = %s", (videogame_id,)),
    [print(row) for row in cursor.fetchall()]
)
select_and_print_all_games = lambda : (
    cursor.execute("SELECT * FROM GAMES"),
    [print(row) for row in cursor.fetchall()]        
) 
select_and_print_game_by_id = lambda game_id: (
    cursor.execute("SELECT * FROM GAMES WHERE id_game = %s", (game_id,)),
    [print(row) for row in cursor.fetchall()]
)
select_and_print_all_companies = lambda : (
    cursor.execute("SELECT * FROM COMPANY"),
    [print(row) for row in cursor.fetchall()]
)
select_and_print_company_by_id = lambda company_id: (
    cursor.execute("SELECT * FROM COMPANY WHERE id_company = %s", (company_id,)),
    [print(row) for row in cursor.fetchall()]
)

# Funções lambda para atualização de dados
update_user = lambda user_data: (
    cursor.execute("UPDATE USERS SET name = %s, country = %s, id_console = %s WHERE id = %s", (user_data[0], user_data[1], user_data[2], user_data[3])),
    mydb.commit()
)
update_videogame = lambda videogame_data: (
    cursor.execute("UPDATE VIDEOGAMES SET name = %s, id_company = %s, release_date = %s WHERE id_console = %s", (videogame_data[0], videogame_data[1], videogame_data[2], videogame_data[3])),
    mydb.commit()
) 
update_game = lambda game_data: (
    cursor.execute("UPDATE GAMES SET title = %s, genre = %s, release_date = %s, id_console = %s WHERE id_game = %s", (game_data[0], game_data[1], game_data[2], game_data[3], game_data[4])),
    mydb.commit()
)
update_company = lambda company_data: (
    cursor.execute("UPDATE COMPANY SET name = %s, country = %s WHERE id_company = %s", (company_data[0], company_data[1], company_data[2])),
    mydb.commit()
)

# Funções lambda para deletar dados
delete_user = lambda user_id: (
    cursor.execute("DELETE FROM USERS WHERE id = %s", (user_id,)),
    mydb.commit()
)
delete_videogame = lambda videogame_id: (
    cursor.execute("DELETE FROM VIDEOGAMES WHERE id_console = %s", (videogame_id,)),
    mydb.commit()
)
delete_game = lambda game_id: (
    cursor.execute("DELETE FROM GAMES WHERE id_game = %s", (game_id,)),
    mydb.commit()
) 
delete_company = lambda company_id: (
    cursor.execute("DELETE FROM COMPANY WHERE id_company = %s", (company_id,)),
    mydb.commit()
) 

# Insere novos dados
# insert_new_user(("John Doe", "USA", 1))
# insert_new_videogame(("Awesome Game Console", 1, "2024-01-01"))
# insert_new_game(("Exciting Adventure", "Adventure", "2024-01-01", 1))
# insert_new_company(("GameCorp", "USA"))

# Seleciona e imprime dados
select_and_print_all_users()
select_and_print_user_by_id(1)  
select_and_print_all_videogames()
select_and_print_videogame_by_id(1)  
select_and_print_all_games()
select_and_print_game_by_id(1)  
select_and_print_all_companies()
select_and_print_company_by_id(1)  

# Atualiza dados existentes
# update_user(("Jane Doe", "Canada", 2, 1))  
# update_videogame(("Super Game Console", 2, "2025-01-01", 1))  
# update_game(("Incredible Adventure", "RPG", "2025-01-01", 2, 1))  
# update_company(("DevStudio", "Canada", 1)) 

# Deleta dados
# delete_user(1)
# delete_videogame(1)
# delete_game(1)
# delete_company(1)
