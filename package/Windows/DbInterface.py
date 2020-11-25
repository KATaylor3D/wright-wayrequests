import webbrowser
import os
import Sqlick
import time



db = Sqlick.Database()
clear = lambda: os.system('cls')
data_categories = [(0, 'Identifying_Number'),
                    (1, 'Name'),
                    (2, 'Stage'),
                    (3, 'Age'),
                    (4, 'Intake_Date'),
                    (5, 'Species'),
                    (6, 'Breed'),
                    (7, 'Sex'),
                    (8, 'Size'),
                    (9, 'Color'),
                    (10, 'Declawed'),
                    (11, 'House_Trained'),
                    (12, 'Location'),
                    (13, 'Spayed_Neutered'),
                    (14, 'Description'),
                    (15, 'Photo_Link_1'),
                    (16, 'Photo_Link_2'),
                    (17, 'Photo_Link_3')]
main_overlay = '1: Clear Search   |   2: Show Available Dogs   |   3: Custom Search   |   4: Pictures   |   Q: Quit'
empty_screen = [['','','','','','','','','','','','','','','','','','']]



def display_screen(resp):
    try:
        for r in resp:
            for itor, cate in data_categories:
                if itor == 15 and r[itor] not in {'', 'Unknown'}:
                    print('Photos: Available')
                elif itor == 15:
                    print('Photos: Unavailable')
                elif itor > 13:
                    pass
                else:
                    print(cate + ': ' + r[itor])
            print('\n')

    finally:
        if resp[0][0] != '':
            print('Entries: ' + str(len(resp)))
        else:
            print('Entries: 0')
        print(main_overlay)

def overlay_interface(response):
    clear()
    display_screen(response)
    action_key = input('Input: ').strip()
    if action_key == '1':
        response = empty_screen
        return response
    elif action_key == '2':
        response = db.get_data_equal_to_values_in_columns([('Stage', 'Available')])
        return response
    elif action_key == '3':
        response = custom_search()
        return response
    elif action_key == '4':
        pictures_opener()
        return response
    elif action_key.lower() == 'q':
        return False
    else:
        return response

def custom_search():
    choice = input('Custom Parameter: ').strip()
    cust_data = []
    for itor, cate in data_categories:
        choice_data = db.get_data_equal_to_values_in_columns([('Stage', 'Available'), (cate, choice)])
        if choice_data:
            return choice_data
    return empty_screen

def pictures_opener():
    choice = input('Dog_ID: ').strip()
    choice_data = db.get_data_equal_to_values_in_columns([('Identifying_Number', choice)])[0]
    pic_links = choice_data[15:]
    for link in pic_links:
        if link != 'Unknown':
            webbrowser.open(link)
        else:
            print('No photo')
            time.sleep(1)



if __name__ == '__main__':
    responce = empty_screen
    while responce:
        responce = overlay_interface(responce)
    clear()