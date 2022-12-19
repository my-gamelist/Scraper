import bs4
import requests


steam_page_url = "https://store.steampowered.com/app/"
steam_api_url = "https://store.steampowered.com/api/appdetails?appids={0}&json=1&cc=ID"


# gets a list of game app ids from the steam API
def get_appid_list():
    appid_list = []

    allgames = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    data = allgames.json()
    data = data['applist']['apps']

    # append each item to the list (list of integers)
    for item in data:
        appid_list.append(item['appid'])
    
    return appid_list


# check if an app id on list is a valid game
def check_game_validity(game_json, appid):
    try:
        # if the game does not exist
        if game_json == None:
            return False

        success = game_json[str(appid)]['success']

        # if the game has an info tab
        if not success:
            return False

        game_json = game_json[str(appid)]['data']

        # if the appid correlates to a game and the game is not in development
        if game_json['type'] == 'game':
            if game_json['release_date']['coming_soon'] == False:
                return True

        # returns false by default
        return False
    except:
        raise Exception(f'Failed to check game validity for {appid}')


# get the app detail from the steam API
def get_app_detail(appid):
    try:
        game_info = requests.get(steam_api_url.format(appid))

        # convert json request into a python dictionary
        game_json = game_info.json()

        # check if the game is valid
        if check_game_validity(game_json, appid): 
            game_json = game_json[str(appid)]['data']

            # initialize the game dictionary
            data = {
                'appid': -1,
                'name': None,
                'release_date': None,
                'detailed_description': None,
                'developers': None,
                'publishers': None
            }
            
            # check if the keys exist in json, then add to the dictionary
            if 'steam_appid' in game_json:
                data['appid'] = game_json['steam_appid']

            if 'name' in game_json:
                data['name'] = game_json['name']

            if 'release_date' in game_json:
                if 'date' in game_json['release_date']:
                    data['release_date'] = game_json['release_date']['date']

            if 'detailed_description' in game_json:
                data['detailed_description'] = game_json['detailed_description']

            if 'developers' in game_json:
                data['developers']= ", ".join(game_json['developers'])

            if 'publishers' in game_json:
                data['publishers']= ", ".join(game_json['publishers'])
            
            return data
        
        # return None if the game is not valid
        return None
    except:
        raise Exception(f'Failed to get game info for {appid}')


def get_image_url(app_id: str) -> str:
    """Get the image for a given app id"""
    # get the page
    page = requests.get(steam_api_url.format(app_id))

    # parse the page
    data = page.json()

    # check if the app id is valid
    if not data[app_id]['success']:
        return ''
    
    # get the image url
    if 'header_image' in data[app_id]['data']:
        return data[app_id]['data']['header_image']
    
    return ''


def get_metacritic_score(app_id: str):
    """Get the metacritic score for a given app id"""
    # get the page
    page = requests.get(steam_api_url.format(app_id))

    # parse the page
    data = page.json()

    # check if the app id is valid
    if not data[app_id]['success']:
        return 0

    # get the metacritic score
    if 'metacritic' in data[app_id]['data']:
        metacritic = data[app_id]['data']['metacritic']

        # check if the metacritic score is valid
        if metacritic is None:
            return 0

        # return the metacritic score
        return int(metacritic['score'])
    
    return 0


def get_steam_rating(app_id: str):
    """Get the steam rating for a given app id"""
    # get the page
    page = requests.get(steam_page_url + app_id)    

    # parse the page
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    # find the number of reviews
    game_review = soup.find_all('span', {'class': 'game_review_summary'})

    if game_review is None or len(game_review) == 0:
        return 0,0
    
    info = None
    for element in game_review:
        if 'data-tooltip-html' in element.attrs:
            info = element['data-tooltip-html']
            break
        
    if info is None:
        return 0,0

    steam_rating = info.split(' ')[0][:-1]
    reviews = info.split(' ')[3].replace(',', '')

    try:
        steam_rating = int(steam_rating)
        reviews = int(reviews)
        return reviews, steam_rating
    except:
        return 0,0

if __name__ == '__main__':
    print(get_image_url('730'))