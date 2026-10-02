import requests
import json

# We are excluding mega evolutions, all Pikachu variants, gigantamax variants, 
# and totem variants from analysis, as well as legendary and mythical Pokemon
disqualifying_strings = ["mega", "pikachu-", "gmax", "totem"]

# Limit set to 2000, there are definitely under 2000 pokemon so this just pulls everything
pokemon_list = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=2000").json()

# We're dumping everything to a .json file
# Faster to access this way, API calls take a while
with open("pokemon_data.json", "w") as file:
    file.write("[\n")
    first_entry = True
    for pokemon in pokemon_list["results"]:
        current_pokemon = requests.get(pokemon["url"]).json()
        is_valid_pokemon = True
        current_pokemon_species = requests.get(current_pokemon["species"]["url"]).json()

        # Checking if the pokemon is in one of the categories marked for exclusion
        if(current_pokemon_species["is_legendary"] or 
           current_pokemon_species["is_mythical"]):
            is_valid_pokemon = False
        for disqualifier in disqualifying_strings:
            if(disqualifier in current_pokemon["name"]):
                is_valid_pokemon = False

        # Only add the Pokemon if it is not marked for exclusion
        if(is_valid_pokemon):
            # This ensures that commas are only added after json entries
            if first_entry:
                first_entry = False
            else:
                file.write(",\n")

            # Only pulling the name, types, base stats, weight, and height
            # from the database
            current_pokemon_json = dict()
            current_pokemon_json["name"] = current_pokemon["name"]

            current_pokemon_types = current_pokemon["types"]
            current_pokemon_types_list = []
            for type in current_pokemon_types:
                current_pokemon_types_list.append(type["type"]["name"])
            current_pokemon_json["types"] = current_pokemon_types_list

            current_pokemon_json["weight"] = current_pokemon["weight"] / 10 #hectogram -> kg
            current_pokemon_json["height"] = current_pokemon["height"] * 10 #decimeter -> cm

            base_stat_total = 0

            for stat in current_pokemon["stats"]:
                stat_name = stat["stat"]["name"]
                base_stat_total += stat["base_stat"]
                current_pokemon_json[stat_name] = stat["base_stat"]
            current_pokemon_json["base_stat_total"] = base_stat_total
            json.dump(current_pokemon_json, file)

    file.write("\n]")
