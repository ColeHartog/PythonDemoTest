# This script has been created with the intention of retrieving data from an API,
# converting that data with some changes to a more manageable form with a class,
# and then saving that data to an external source, in this case I'm making a csv file.

import requests
import multiprocessing as mp
from os.path import exists
import csv


class Pokemon:
    def __init__(self, _data):
        self.id = int(_data['id'])
        self.name = _data['name'].capitalize()
        self.types = ', '.join(list(map(lambda _type: _type['type']['name'].capitalize(), _data['types'])))
        self._types = list(map(lambda _type: _type['type']['name'].capitalize(), _data['types']))

    def entry(self):
        print(f'{self.id}: {self.name} is a {" and ".join(self._types)} type pokemon')


def get_pokemon(_list, _id):
    try:
        # Can't request more than one pokemon data per call
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{_id}')
        _list.append(Pokemon(res.json()))
    except ValueError:
        print(f'There was an error getting the data from the api from id: {_id}.')


def save_pokedex_csv(_pokedex):
    with open('./DemoSave.csv', 'w', newline='', encoding='UTF8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'types'], extrasaction='ignore')
        writer.writeheader()
        for pokemon in pokedex:
            writer.writerow(vars(pokemon))


if __name__ == '__main__':
    # Creating a manager list for easier multi-processing management
    manager = mp.Manager()
    pokedex = manager.list()
    pros = []

    for i in range(1, 152):
        # Multiprocessing the api calls and converting response data to a pokemon to speed up the process
        p = mp.Process(target=get_pokemon, args=(pokedex, i))
        pros.append(p)
        p.start()

    for p in pros:
        p.join()

    # Use the id value (int) as the base for sorting the data
    pokedex = sorted(pokedex, key=lambda x: x.id)

    # This was used for testing
    # for pokemon in pokedex:
    #     pokemon.entry()

    # Check for existing csv file, if one does not exist, then the program creates the file and adds the data
    if len(pokedex) > 0 and not exists('DemoSave.csv'):
        save_pokedex_csv(pokedex)

