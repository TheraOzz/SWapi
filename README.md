# The Star Wars API

terminal application capable of managing different tasks using command line arguments.

## tasks:
- connect to (https://www.swapi.tech/)
- allow the user of the program to search based on the name of any Star Wars character.
- provide aditional information of the home world for the character we searched, using aditional command line arguments.
- giving some insights into how that world compares with ours here on earth.
- json managment to store and recall information of previous searches in order to avoid unnecessary requests.
- clean cache method

## commands:
- search
- cache

## keywords:
 - character name

## options:
- -w / --world for home world informations
- -c / --clean for cleaning the cache (no keyword needed for this method)

## usage:
python main.py [command] [keyword] [option]
