import requests
import json

# We are excluding mega evolutions, all Pikachu variants, gigantamax variants, 
# and totem variants from analysis, as well as legendary and mythical Pokemon
disqualifying_strings = ["mega", "pikachu-", "gmax", "totem"]

pokemon_list = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=2000").json()

# For storage, everything will be dumped to a .json file
# This way, API calls only have to be made once
with open("pokemon_data.json", "w") as file:
    file.write("[\n")
    first_entry = True
    for pokemon in pokemon_list["results"]:
        current_pokemon = requests.get(pokemon["url"]).json()
        is_valid_pokemon = True
        current_pokemon_species = requests.get(current_pokemon["species"]["url"]).json()

        # This section checks to see if the given Pokemon is legendary, mythical,
        # or falls into one of the aforementioned disallowed categories
        if(current_pokemon_species["is_legendary"] or 
           current_pokemon_species["is_mythical"]):
            is_valid_pokemon = False
        for disqualifier in disqualifying_strings:
            if(disqualifier in current_pokemon["name"]):
                is_valid_pokemon = False

        # Only add the Pokemon if it fits the criteria
        if(is_valid_pokemon):
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