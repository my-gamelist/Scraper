import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            host=os.environ['host'],
            database=os.environ['database'],
            user=os.environ['user'],
            password=os.environ['password']
        )
        self.cursor = self.connection.cursor()

        self.connection.autocommit = True

    # query to add a new game to the database
    def add_game(self, app_id, game_name, release_date, rating, num_reviews, description, studio, publisher, steam_rating, metacritic_score, steam_reviews, image_url):
        query = "INSERT INTO game (app_id, game_name, release_date, rating, num_reviews, description, developers, publishers, steam_rating, metacritic_score, steam_reviews, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"     
        self.cursor.execute(query, (app_id, game_name, release_date, rating, num_reviews, description, studio, publisher, steam_rating, metacritic_score, steam_reviews, image_url))
        self.connection.commit()
    
    # query to update a game in the database
    def update_game(
        self, app_id, game_name,
        release_date, rating,
        num_reviews, description,
        studio, publisher,
        steam_rating, metacritic_score,
        steam_reviews, image_url
    ):
        query = f'UPDATE game SET game_name = {game_name},release_date = "{release_date}", rating = {rating}, num_reviews = {num_reviews}, description = {description}, developers = {studio}, publishers = {publisher}, steam_rating = {steam_rating}, metacritic_score = {metacritic_score}, steam_reviews = {steam_reviews}, image_url = "{image_url}" WHERE app_id = {app_id};'
        self.cursor.execute(query)
        self.connection.commit()

    # save and close the connection
    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    # gets the row in the database given an id
    def get_game(self, app_id):
        query = f"SELECT * FROM game WHERE app_id = {app_id};"
        self.cursor.execute(query)
        return self.cursor.fetchone()
       
    # get total row count from the game table 
    def get_row_count(self):
        query = 'SELECT COUNT(*) FROM game;'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    # check if the given app_id is in the excluded table
    def check_excluded(self, app_id):
        query = f"SELECT * FROM excluded_apps WHERE app_id = {app_id};"
        self.cursor.execute(query)

        if self.cursor.fetchone():
            return True
        
        return False
    
    # adds a row to the excluded table with given app_id 
    def add_exclusion(self, app_id):
        query = "INSERT INTO excluded_apps (app_id) VALUES (%s)"     
        self.cursor.execute(query, (app_id,))
        self.connection.commit()