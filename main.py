import requests
import json
import sys
import os
import datetime


def main():
    """entrypoint of program"""
    display_title()
    try:
        command = sys.argv[1]
        keyword = sys.argv[2]
    except:
        pass

    option = None
    try:
        option = sys.argv[3]
    except:
        pass

    if command == "search":
        search(keyword, option)
    elif command == "cache":
        cache(keyword)
    else:
        print("wrong command.. (commands: search, cache)")


def display_title():
    """display program title"""
    os.system("clear")
    print("\t**************************************************")
    print("\t**************  The Star Wars API!  **************")
    print("\t**************************************************")
    print("\tusage: python main.py [command] [keyword] [option]\n")


def search(character, option=None):
    """manage all searching functions"""
    data = search_data()
    data_character = search_character(character, data)
    data_world = None
    try:
        if option in ("-w", "--world"):
            data_world = search_world(data_character)
    except:
        pass
    show_results(data_character, data_world)


def search_data():
    """request data and return attributes in a list"""
    response = requests.get("https://www.swapi.tech/api/people")
    data_texted = response.text
    data_loaded = json.loads(data_texted)
    data = data_loaded["results"]
    return data


def search_character(character, data):
    """search for given character's existence and return attributes in a list"""
    myCache={}
    try:
        with open("data.json") as cache_in:
            myCache = json.load(cache_in)
    except:
        pass
    if len(myCache) == 0:
        myCache["name"]=""
    if character in myCache["name"]:
        return myCache
    else:
        for keyval in data:
            if character.lower() in keyval["name"].lower():
                response = requests.get(keyval["url"])
                data_texted = response.text
                data_loaded = json.loads(data_texted)
                data_character = data_loaded["result"]["properties"]

                search_date = datetime.datetime.now()
                data_character["search_date"] = str(search_date)

                with open("data.json", "w") as cache_out:
                    json.dump(data_character, cache_out, indent=4)
                
                return data_character


def search_world(data_character):
    """search for given character's world and return attributes in a list"""
    data_homeworld = data_character["homeworld"]
    response_world = requests.get(data_homeworld)
    data_world_texted = response_world.text
    data_world_loaded = json.loads(data_world_texted)
    data_world = data_world_loaded["result"]["properties"]
    return data_world


def show_results(data_character, data_world):
    """print out character and world info"""
    if data_character != None:
        character_info = {
            "Name" : data_character["name"],
            "Height" : data_character["height"],
            "Mass" : data_character["mass"],
            "Birth Year" : data_character["birth_year"]}

        print("")
        for key, value in character_info.items():
            print(f"{key}: {value}")
        print("")

        if data_world != None:
            orbital_period = "{:.2f}".format(float(data_world['orbital_period']) / 366)
            rotation_period = "{:.2f}".format(float(data_world['rotation_period']) / 24)
            world_info = (
                "Homeworld", 
                "---------", 
                "Name: " + data_world['name'], 
                "Population: " + data_world["population"], "", 
                f"On {data_world['name']}, 1 year on earth is {orbital_period} and 1 day {rotation_period} days")
            print("")
            for line in world_info:
                print(line)
            print("\n")
        if data_character["search_date"]:
            print(f'cached: {data_character["search_date"]}')
    else:
        print("\nThe force is not strong within you")


def cache(keyword=None):
    try:
        if keyword in ("-c", "--clean"):
            if os.path.exists("data.json"):
                open("data.json", "w").close()
                # os.remove("data.json")
    except:
        pass


if __name__ == "__main__":
    main()
