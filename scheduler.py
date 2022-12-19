import os
import signal

import time

from database import Database
from logger import Logger
from steam import get_appid_list, get_app_detail, get_steam_rating, get_metacritic_score, get_image_url

pwd = os.getcwd()

# Updates the database every 24 hours
# can optionally take in a predefined app id list for testing or manual updating 
def update_gamelist(current_gamelist=None):
    db = Database()
    logger = Logger()

    def signal_handler(sig, frame):
        logger.close_files()
        db.close_connection()
        print('Exiting...')
        exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    # get current list by calling steam API if a preset one was not given
    if current_gamelist == None:
        current_gamelist = set(get_appid_list())
    
    # look at all game ids in updated list and see if they are in the previous list
    for appid in current_gamelist:
        try:
            # check if in excluded table
            if db.check_excluded(appid) == True:
                continue
        
             # if they are not in the current database, check if valid then add to database via query
            if db.get_game(appid) == None:
                
                game = get_app_detail(appid)
                if game != None:
                    reviews, steam_rating = get_steam_rating(str(appid))
                    metacritic_score = get_metacritic_score(str(appid))
                    image_url = get_image_url(str(appid))
                    # add the game to the database
                    db.add_game(
                        game['appid'],
                        game['name'],
                        game['release_date'],
                        0, # rating
                        0, # num_reviews
                        game['detailed_description'],
                        game['developers'],
                        game['publishers'],
                        steam_rating,
                        metacritic_score,
                        reviews,
                        image_url
                    )

                    # save the game id to the log file
                    logger.save_logs(str(game['appid']))     
                
                # if the game is not valid, add it to the exclude list for next time
                else:
                    db.add_exclusion(appid)
            
            # if the game is in the database, update its info
            else:
                game = get_app_detail(appid)
                if game != None:
                    reviews, steam_rating = get_steam_rating(str(appid))
                    metacritic_score = get_metacritic_score(str(appid))
                    image_url = get_image_url(str(appid))
                    db.update_game(
                        game['appid'],
                        game['name'],
                        game['release_date'],
                        0, # rating
                        0, # num_reviews
                        game['detailed_description'],
                        game['developers'],
                        game['publishers'],
                        steam_rating,
                        metacritic_score,
                        reviews,
                        image_url
                    )
                    
        except Exception as e:
            # add the game to the failed file
            print(str(e))
            print(f'Failed to add game {appid} to database')
            logger.save_failed(str(appid))
            continue
        
    # close the connection
    db.close_connection()

    # close the files
    logger.close_files()


def main():
    update_gamelist()


if __name__ == '__main__':
    main()