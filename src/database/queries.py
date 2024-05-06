from psycopg2 import sql
from database import access
import bcrypt

# USER REGISTRATION QUERIES
def add_user(username, email, password, admin):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    
    # check if user_name already used
    cursor.execute("SELECT user_name FROM users")
    usernames = cursor.fetchall()
    for name, in usernames:
        if name == username:
            cursor.close()
            conn.close()
            return False # failed to add user
        
    # check if user_email already used
    cursor.execute("SELECT user_email FROM users")
    emails = cursor.fetchall()
    for user_email, in emails:
        if user_email == email:
            cursor.close()
            conn.close()
            return False # failed to add user
        
    # execute command
    query = sql.SQL("INSERT INTO users (user_name, user_email, password, isadmin) VALUES (%s, %s, %s, %s)")
    cursor.execute(query, (username, email, password, admin))
    
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True # succesfully added user

# USERS QUERIES
def get_users():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return users

def get_all_usernames():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT user_name FROM public_users")
    user_names = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return user_names

def get_user_id(username):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT user_id FROM users WHERE user_name = %s")
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    return user_id

def get_user_info_by_name(username):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM public_users WHERE user_name = %s")
    cursor.execute(query, (username,))
    user_count = cursor.fetchone()
    if user_count[0] == 1:
        query = sql.SQL("SELECT * FROM public_users WHERE user_name = %s")
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()
    else:
        user_info = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return user_info


# GENRE QUERIES 
def get_genres():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return genres

def get_genre_by_id(genre_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT * FROM genres WHERE genre_id = %s")
    cursor.execute(query, (genre_id,))
    genre = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    return genre

def add_genre(genre_name):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("INSERT INTO genres(genre_name) VALUES (%s)")
    cursor.execute(query, (genre_name,))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def remove_genre(genre_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM genres WHERE genre_id = %s")
    cursor.execute(query, (genre_id,))
    num_games = cursor.fetchone()
    num_games = num_games[0]
    if num_games == 1:
        query = sql.SQL("DELETE FROM genres WHERE genre_id = %s")
        cursor.execute(query, (genre_id,))
        # commit transaction
        conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    if num_games == 1:
        return True
    else:
        return False

def get_genre_names():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT genre_name FROM genres")
    genres = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return genres

# GAMES QUERIES
def get_public_games(sorting="title", order="desc"):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    match sorting, order:
        case "Title", "Descending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY title DESC")
        case "Title", "Ascending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY title")
        case "Genre", "Descending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY genre_name DESC")
        case "Genre", "Ascending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY genre_name")
        case "Publisher", "Descending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY pub_name DESC")
        case "Publisher", "Ascending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY pub_name")
        case "Release Date", "Descending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY release_date DESC")
        case "Release Date", "Ascending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY release_date")
        case "Rating", "Descending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY avg DESC")
        case "Rating", "Ascending":
            query = sql.SQL("SELECT * FROM public_games ORDER BY avg")
        case _:
            query = sql.SQL("SELECT * FROM public_games")
    
    cursor.execute(query)
    games = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def get_games():
    # Literally just get the whole GAMES table
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def add_game(release_date, title, pub_id, genre_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    
    # check if title of game already exists || NO DUPE TITLES
    cursor.execute("SELECT title FROM games")
    games = cursor.fetchall()
    
    for n, in games:
        if n == title:
            cursor.close()
            conn.close()
            return False # failed to add game
            
    # execute command
    query = sql.SQL("INSERT INTO games (release_date, title, pub_id) VALUES (%s, %s, %s)")
    cursor.execute(query, (release_date,title,pub_id))
    
    # get the game id
    query = sql.SQL("SELECT game_id FROM games WHERE title = %s")
    cursor.execute(query,(title,))
    game_id = cursor.fetchone()
    
    # add game to the genre based on game_id
    query = sql.SQL("INSERT INTO gamegenre(game_id,genre_id) VALUES (%s, %s)")
    cursor.execute(query, (game_id, genre_id))

    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True

def get_game_id(title):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
        
    # execute command
    query = sql.SQL("SELECT game_id FROM games WHERE title = %s ")
    cursor.execute(query, (title,))
    game_id = cursor.fetchone()
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return game_id

def add_game_to_genre(game_id, genre_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return

    query = sql.SQL("INSERT INTO gamegenre(game_id,genre_id), VALUES (%s, %s)")
    cursor.execute(query, (game_id, genre_id))

    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True # succesfully added game

def remove_game(game_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("DELETE FROM gamegenre WHERE game_id = %s")
    cursor.execute(query, (game_id,))
    query2 = sql.SQL("DELETE FROM games WHERE game_id = %s")
    cursor.execute(query2, (game_id,))

    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True

def get_games_by_user_id(user_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM public_user_game WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    num_games = cursor.fetchone()
    if num_games[0] > 0:
        query = sql.SQL("SELECT title, genre_name, pub_name, release_date FROM public_user_game WHERE user_id = %s")
        cursor.execute(query, (user_id,))
        games = cursor.fetchall()
    else:
        games = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def get_game_titles_by_user_id(user_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM public_user_game WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    num_games = cursor.fetchone()
    if num_games[0] > 0:
        query = sql.SQL("SELECT title FROM public_user_game WHERE user_id = %s")
        cursor.execute(query, (user_id,))
        games = cursor.fetchall()
    else:
        games = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def get_unplayed_games_by_user_id(user_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT title FROM games WHERE game_id NOT IN (SELECT game_id FROM user_game WHERE user_id = %s)")
    cursor.execute(query, (user_id,))
    game_titles = cursor.fetchall()
    if len(game_titles) == 0:
        game_titles = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return game_titles

def add_user_game(user_id, game_id):
    # get conn and cursor
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("INSERT INTO user_game(user_id, game_id) VALUES (%s, %s)")
    cursor.execute(query, (user_id, game_id))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def remove_user_game(user_id, game_id):
    # get conn and cursor
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("DELETE FROM user_game WHERE user_id = %s AND game_id = %s")
    cursor.execute(query, (user_id, game_id))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def get_public_games_by_genre(genre_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    query = sql.SQL("SELECT * FROM public_games WHERE title IN (SELECT title FROM games NATURAL JOIN genres WHERE genre_id = %s)")
    cursor.execute(query, (genre_id,))
    games = cursor.fetchall()
    
    # close cursor and conn
    cursor.close()
    conn.close()
    return games
    
def get_game_titles():
    # get conn and cursor
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT title FROM public_games")
    games = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def get_games_by_genre_name(genre_name, sorting="title", order="desc"):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    match sorting, order:
        case "Title", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY title DESC")
        case "Title", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY title")
        case "Publisher", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY pub_name DESC")
        case "Publisher", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY pub_name")
        case "Release Date", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY release_date DESC")
        case "Release Date", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY release_date")
        case "Rating", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY avg DESC")
        case "Rating", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s ORDER BY avg")
        case _:
            query = sql.SQL("SELECT * FROM public_games WHERE genre_name = %s")
    cursor.execute(query, (genre_name,))
    games = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

def get_games_by_publisher_name(publisher_name, sorting="title", order="desc"):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    match sorting, order:
        case "Title", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY title DESC")
        case "Title", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY title")
        case "Genre", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY genre_name DESC")
        case "Genre", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY genre_name")
        case "Release Date", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY release_date DESC")
        case "Release Date", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY release_date")
        case "Rating", "Descending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY avg DESC")
        case "Rating", "Ascending":
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s ORDER BY avg")
        case _:
            query = sql.SQL("SELECT * FROM public_games WHERE pub_name = %s")
    cursor.execute(query, (publisher_name,))
    games = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return games

# PUBLISHERS  QUERIES
def get_publishers():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT * FROM publishers")
    publishers = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return publishers

def add_publisher(pub_name):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("INSERT INTO publishers(pub_name) VALUES (%s)")
    cursor.execute(query, (pub_name,))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def remove_publisher(pub_id):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM games WHERE pub_id = %s")
    cursor.execute(query, (pub_id,))
    num_games = cursor.fetchone()
    num_games = num_games[0]
    if num_games == 0:
        query = sql.SQL("DELETE FROM publishers WHERE pub_id = %s")
        cursor.execute(query, (pub_id,))
        # commit transaction
        conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    if num_games == 0:
        return True
    else:
        return False

def get_publisher_names():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT pub_name FROM publishers")
    publishers = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return publishers

# USER / ADMIN PROPERTIES 
# LOGN CONFIRMATION
def authenticate_login(username, password):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # retrieve the expected password
    query = sql.SQL("SELECT password FROM users WHERE user_name = %s")
    cursor.execute(query, (username,))
    expected_password = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    # check if it matches
    if expected_password:
        expected_hash = expected_password[0].encode('utf-8')
        password_hash = password.encode('utf-8')
        if bcrypt.checkpw(password_hash, expected_hash):
            return True
    return False

def get_user_name(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # retrieve the user data
    query = sql.SQL("SELECT user_name FROM users WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    username = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    return username

def user_id_exists(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT COUNT(*) FROM users WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    count = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True if count[0] == 1 else False

def is_admin(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # retrieve the user data
    query = sql.SQL("SELECT isadmin FROM users WHERE user_id = %s")

    #unpack user_id if it is in a list
    #if isinstance(user_id, list):
    #    user_id = user_id[0]
    cursor.execute(query, (user_id,))
    isadmin = cursor.fetchone()
    # close cursor and conn
    cursor.close()
    conn.close()
    return isadmin[0]

def set_admin(user_id, admin_status):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # retrieve the user data
    query = sql.SQL("UPDATE users SET isadmin = %s WHERE user_id = %s")
    cursor.execute(query, (admin_status, user_id))
    
    # commit changes
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def toggle_admin(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # retrieve the user data
    query = sql.SQL("UPDATE users SET isadmin = NOT isadmin WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    
    # commit changes
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def remove_user(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("DELETE FROM reviews WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    query = sql.SQL("DELETE FROM user_game WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    query = sql.SQL("DELETE FROM users WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True

def change_password(user_id, password):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("UPDATE users SET password = %s WHERE user_id = %s")
    cursor.execute(query, (password, user_id))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True

# REVIEW  QUERIES
def get_all_reviews():
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return reviews

def get_reviews_by_user_name(username):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    user_id = get_user_id(username)
    query = sql.SQL("SELECT COUNT(*) FROM reviews WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    user_count = cursor.fetchone()
    if user_count[0] > 0:
        query = sql.SQL("SELECT r.title, description, rating, g.title FROM reviews r JOIN games g ON r.game_id = g.game_id WHERE r.user_id = %s")
        cursor.execute(query, (user_id,))
        reviews = cursor.fetchall()
    else:
        reviews = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return reviews

def get_reviews_by_user_adminview(user_id): # INPUT user_id , OUTPUT all review_ids of that users reviews
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return

    query = sql.SQL("SELECT COUNT(*) FROM reviews WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    num_reviews = cursor.fetchone()
    if num_reviews[0] > 0:
        query = sql.SQL("SELECT r.review_id, r.title, description, g.title FROM reviews r JOIN games g ON r.game_id = g.game_id WHERE r.user_id = %s")
        cursor.execute(query, (user_id,))
        reviews = cursor.fetchall()
    else:
        reviews = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return reviews

def remove_review(review_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command    
    query = sql.SQL("DELETE FROM reviews WHERE review_id = %s")
    cursor.execute(query, (review_id,))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()
    return True

def add_review(user_id, game_id, title, description, rating):
    # get conn and cuser
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("INSERT INTO reviews(user_id, game_id, title, description, rating) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (user_id, game_id, title, description, rating))
    # commit transaction
    conn.commit()
    # close cursor and conn
    cursor.close()
    conn.close()

def get_game_id_reviews_by_user(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute command
    query = sql.SQL("SELECT game_id FROM reviews WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    game_ids = cursor.fetchall()
    # close cursor and conn
    cursor.close()
    conn.close()
    return game_ids

def get_reviews_by_user_id_public(user_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute query
    query = sql.SQL("SELECT COUNT(*) FROM reviews WHERE user_id = %s")
    cursor.execute(query, (user_id,))
    num_reviews = cursor.fetchone()
    if num_reviews[0] > 0:
        query = sql.SQL("SELECT g.title FROM reviews r JOIN games g ON r.game_id = g.game_id WHERE r.user_id = %s")
        cursor.execute(query, (user_id,))
        reviews = cursor.fetchall()
    else:
        reviews = None
    # close cursor and conn
    cursor.close()
    conn.close()
    return reviews

def get_review_id_by_user_game_id(user_id, game_id):
    # get conn and user
    conn, cursor = access.get_db_cursor()
    # check if conn and cursor were successfully retrieved
    if cursor is None:
        return
    # execute query
    query = sql.SQL("SELECT review_id FROM reviews WHERE user_id = %s AND game_id = %s")
    cursor.execute(query, (user_id, game_id))
    review_id = cursor.fetchone()

    # close cursor and conn
    cursor.close()
    conn.close()
    return review_id

# You've reached the end of this file. To continue, press 1 after the beep.