import requests
import Sqlick
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import winsound
import os

n = '\n'

table_urls = [
             'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=UnderYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque', 
             'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=OverYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque'
             ]

tag_ids = [
          'span lblID',
          'span lbName',
          'span lblStage',
          'span lbAge',
          'span lblIntakeDate',
          'span lblSpecies',
          'span lbBreed',
          'span lbSex',
          'span lblSize',
          'span lblColor',
          'span lbDeclawed',
          'span lbHousetrained',
          'span lblLocation',
          'img ImageAltered',
          'span lbDescription',
          'a lnkPhoto1',
          'a lnkPhoto2',
          'a lnkPhoto3'
          ]

column_values = [
                'Identifying_Number TEXT',
                'Name TEXT',
                'Stage TEXT',
                'Age TEXT',
                'Intake_Date TEXT',
                'Species TEXT',
                'Breed TEXT',
                'Sex TEXT',
                'Size TEXT',
                'Color TEXT',
                'Declawed TEXT',
                'House_Trained TEXT',
                'Location TEXT',
                'Spayed_Neutered TEXT',
                'Description TEXT',
                'Photo_Link_1 TEXT',
                'Photo_Link_2 TEXT',
                'Photo_Link_3 TEXT'
                ]


def finished():
    print('...Complete')
    winsound.Beep(4400, 2_500)

def site_soup_after_sleep(url):
    time_to_sleep = randint(12,26) / 10
    sleep(time_to_sleep)
    site = requests.get(url).text
    soup = BeautifulSoup(site, 'lxml')
    return soup

def return_available_animals(animals):
    available = []
    for animal in animals:
        if animal[2].lower() == "available":
            available.append(animal)
    return available

def is_info_complete(animal):
    return len(animal) == 18

def animal_ids():
    ids = []
    for site in table_urls:
        soup = site_soup_after_sleep(site)
        id_list = soup.find_all('div', class_='list-animal-id')
        for i in id_list:
            ids.append(''.join(i.findAll(text=True)))
    return ids

def convert_animal_id_to_link(id_):
    link = f'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimalDetails.aspx?id={id_}&amp;css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css'
    return link

def convert_animal_ids_to_links(ids):
    links = []
    for id_ in ids:
        links.append(f'https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimalDetails.aspx?id={id_}&amp;css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css')
    return links

def get_table_values(soup_obj):
    site_values = []
    for ids in tag_ids:
        tag = ids.split()[0]
        id_ = ids.split()[1]
        if tag == 'img':
            try:                
                value = soup_obj.find(tag, id= id_).attrs['src']
                if value == "images/GreenCheck.JPG":
                    site_values.append('Is  Spayed/Neutered')
                else:
                    site_values.append('Unknown')
            except:
                site_values.append('Unknown')
        elif tag == 'a':
            try:                
                value = soup_obj.find(tag, id= id_).attrs['href']
                if value:
                    site_values.append(value)
                else:
                    site_values.append('Missing Photo')
            except:
                site_values.append('Missing Photo')
        else:        
            try:                
                value = soup_obj.find(tag, id= id_).text
                if value:
                    site_values.append(value)
                else:
                    site_values.append('Unknown')
            except:
                site_values.append('Unknown')
    return site_values

def update_data():
    os.system("cls")
    db = Sqlick.Database(column_values)
    ids = animal_ids()
    links = convert_animal_ids_to_links(ids)
    count = (int(number_of_animals()) -1)
    for link in links:
        soup = site_soup_after_sleep(link)
        table_value = get_table_values(soup)
        db.add_data(table_value)
        os.system("cls")
        print('Working: ', count)
        count -= 1

# def update_data():
#     os.system("cls")
#     db = Sqlick.Database(column_values)
#     ids = animal_ids()
#     links = convert_animal_ids_to_links(ids)
#     count = 3
#     for l in range(0, 3):
#         soup = site_soup_after_sleep(links[l])
#         table_value = get_table_values(soup)
#         db.add_data(table_value)
#         os.system("cls")
#         print('Working: ', count)
#         count -= 1

def update_last(new_value):
    os.remove("last.txt")
    with open("last.txt", "x") as file:
        file.write(str(new_value))

def presence_of_new_data():
    new_length = number_of_animals()
    with open("last.txt", "r") as file:
        old_length = file.read()
    if new_length != old_length:
        update_last(new_length)
        return True
    else:
        return False

def number_of_animals():
    count = 0
    for site in table_urls:
        site_text = str(site_soup_after_sleep(site))
        number = (len(site_text.split('<div class="list-animal-id">')) - 1)
        count += number
    return str(count)


if __name__ == '__main__':
    print('Not run directly')
