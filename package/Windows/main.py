import Scraper
import Email
import Sqlick
from time import sleep
import os
import general

n = '\n'
s = ' '

def logic():
    if Scraper.presence_of_new_data():
        Sqlick.create_temp_database()
        new_animals = Sqlick.get_new_data()
        complete_animals = []
        if new_animals:
            for animal_data in new_animals:
                if Scraper.is_info_complete(animal_data):
                    complete_animals.append(animal_data)
                    Sqlick.add_singular_data_to_main_database(animal_data)
                else:
                    with open('concant.txt', 'a') as file:
                        concant_animal = n + str(animal_data) + n + "... Failed"
                        file.write(concant_animal)
        if complete_animals:
            available_animals = Scraper.return_available_animals(complete_animals)
            if available_animals:
                Email.send_email(available_animals)
        Sqlick.remove_temp_database()
        general.text_timer('Message sent\n', 180)
    else:
        general.text_timer("No New Data\n", 180)

if __name__ == '__main__':
    running = True
    while running:
        running = general.while_crash_alarm(logic)
