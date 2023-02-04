import copy
import csv
import math
import random
import time
from Pokemon import Pokemon
from Move import Move


pokemon_list = []
move_lookup = {}
type_table = {}


def read_csv_files():
    # Populate Move objects and place in dictionary, move_lookup
    with open('moves-data.csv') as move_data:
        reader = csv.reader(move_data, delimiter=',')
        header = next(reader)
        for row in reader:
            move_lookup[row[0]] = Move(row[0], row[1], row[5])

    # Populate Pokemon objects and place in list, pokemon_list
    with open('pokemon-data.csv') as pokemon_data:
        reader = csv.reader(pokemon_data, delimiter=',')
        header = next(reader)  # grabs first row containing header info
        for row in reader:
            pokemon_list.append(Pokemon(row[0], row[1], row[2], row[3], row[4], convert_to_list(row[7])))

    # Populate type matchup table
    with open('type-matchup.csv') as type_data:
        reader = csv.reader(type_data, delimiter=',')
        header = next(reader)
        for row in reader:
            type_table[row[0]] = {"Normal": row[1], "Fire": row[2], "Water": row[3], "Electric": row[4],
                                  "Grass": row[5]}


def convert_to_list(moves):
    """ Converts the move data from the CSV file into a list of Move objects
        so each Pokemon object will have a property that holds this list of Move objects"""
    move_list = []
    for move in moves[1:len(moves) - 1].split(','):
        move = move.replace("'", ' ')
        move = move.replace('"', ' ')
        move = move.strip()
        if move in move_lookup:
            move_list.append(copy.deepcopy(move_lookup[move]))
        else: # Moves like "Double-Edge", "Mud Slap", "Baby-Doll Eyes", "Self-Destruct"
            move_list.append(Move(move, poke_type='Normal', power=0, power_points=0))
    return move_list


def introduction():
    delay_print('Welcome to ...')

    time.sleep(1)
    print("\n                                  ,'\\")
    print("    _.----.        ____         ,'  _\\   ___    ___     ____")
    print("_,-'       `.     |    |  /`.   \\,-'    |   \\  /   |   |    \\  |`.")
    print("\\      __    \\    '-.  | /   `.  ___    |    \\/    |   '-.   \\ |  |")
    print(" \\.    \\ \\   |  __  |  |/    ,','_  `.  |          | __  |    \\|  |")
    print("   \\    \\/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |")
    print("    \\     ,-'/  /   \\    ,'   | \\/ / ,`.|         /  /   \\  |     |")
    print("     \\    \\ |   \\_/  |   `-.  \\    `'  /|  |    ||   \\_/  | |\\    |")
    print("      \\    \\ \\      /       `-.`.___,-' |  |\\  /| \\      /  | |   |")
    print("       \\    \\ `.__,'|  |`-._    `|      |__| \\/ |  `.__,'|  | |   |")
    print("        \\_.-'       |__|    `-._ |              '-.|     '-.| |   |")
    print("             ___      _          `'                           '-._|")
    print("            / __\\___ | | ___  ___ ___  ___ _   _ _ __ ___  ")
    print("           / /  / _ \\| |/ _ \\/ __/ __|/ _ \\ | | | '_ ` _ \\ ")
    print("          / /__| (_) | | (_) \\__ \\__ \\  __/ |_| | | | | | |")
    print("          \\____/\\___/|_|\\___/|___/___/\\___|\\__,_|_| |_| |_|")
    time.sleep(2)
    return


def delay_print(message):
    """ Used to get a typing effect in the console """
    for character in message:
        print(character, end='')
        time.sleep(0.07)


def print_battle_info(p_pokemon, r_pokemon):
    """ Prints an ASCII representation of the battlefield """
    print("\n\n\n\n\n")
    print("=========================")
    print(f"{r_pokemon.name.ljust(25)}")
    print(f"HP:{r_pokemon.hit_points:03}/{r_pokemon.max_hit_points:03}{r_pokemon.name[0].center(15)}")
    print(f"{r_pokemon.poke_type.ljust(25)}\n")
    print(f"{p_pokemon.name.rjust(25)}")
    print(f"{p_pokemon.name[0].center(15)}HP:{p_pokemon.hit_points:03}/{p_pokemon.max_hit_points:03}")
    print(f"{p_pokemon.poke_type.rjust(25)}")
    print("=========================")


def calculate_damage(move_used, attacking_pokemon, defending_pokemon):
    if move_used.poke_type == attacking_pokemon.poke_type:
        stab = 1.5
    else:
        stab = 1.0

    type_match = 1
    if move_used.poke_type in type_table:
        type_match = type_table.get(move_used.poke_type).get(defending_pokemon.poke_type)

    rand = round(random.uniform(0.5, 1), 2)

    damage = move_used.power \
             * attacking_pokemon.attack \
             / defending_pokemon.defense \
             * stab \
             * float(type_match) \
             * rand
    damage = math.ceil(damage)
    defending_pokemon.hit_points -= damage

    delay_print(attacking_pokemon.name + ' used ' + move_used.name + '!\n')

    if rand >= 0.9:
        delay_print('Critical hit!\n')

    if type_match == '0.5':
        delay_print("It's not very effective...\n")
    elif type_match == '2':
        delay_print("It's super effective!\n")

    delay_print(defending_pokemon.name + ' is hit for ' + str(damage) + ' damage!\n')

    if defending_pokemon.hit_points <= 0:
        delay_print(defending_pokemon.name + ' has fainted!\n')

    return


def turn_menu(pokemon):
    """ Prints the available moves a player can select during their turn,
        and returns the Move object they selected """
    available_moves = []
    available_input = []
    unavailable_moves = ["Double-Edge", "Mud Slap", "Baby-Doll Eyes", "Self-Destruct"]

    # First pass over the pokemon's moves to see if any are available
    for move in pokemon.moves:
        if move.power_points:
            available_moves.append(move)

    # Moves are exhausted so reset power_points, disregarding unavailable moves
    if len(available_moves) == 0:
        for move in pokemon.moves:
            if move.name not in unavailable_moves:
                move.power_points = 1
                available_moves.append(move)

    print(f'Choose the move for {pokemon.name} (Type: {pokemon.poke_type}):')
    i = 1
    for move in pokemon.moves:
        if move.power_points:
            print(f'{i}. {move.name} (Type: {move.poke_type} | Power: {move.power})')
            available_input.append(str(i))
        else:
            print(f'{i}. {move.name} (N/A)')
        i += 1

    while True:
        player_choice = input("Input: ")
        if player_choice not in available_input:
            print("Invalid choice!")
            continue

        break

    pokemon.moves[int(player_choice) - 1].power_points = 0
    return pokemon.moves[int(player_choice) - 1]


def get_random_move(moves_list):
    """ Gets a random move that is available to use, disregarding any preconfigured unavailable moves """
    available_moves = []
    unavailable_moves = ["Double-Edge", "Mud Slap", "Baby-Doll Eyes", "Self-Destruct"]
    # First pass over the pokemon's moves to see if any are available
    for move in moves_list:
        if move.power_points:
            available_moves.append(move)

    # Moves are exhausted so reset power_points, disregarding unavailable moves
    if len(available_moves) == 0:
        for move in moves_list:
            if move.name not in unavailable_moves:
                move.power_points = 1
                available_moves.append(move)

    # Choose a random move to use from the list of available_moves
    selected_move = random.choice(available_moves)
    selected_move.power_points = 0

    return selected_move


def rocket_turn(r_pokemon, p_pokemon):
    print_battle_info(p_pokemon, r_pokemon)
    delay_print("Team Rocket is about to attack...\n")
    selected_move = get_random_move(r_pokemon.moves)
    calculate_damage(selected_move, r_pokemon, p_pokemon)


def player_turn(p_pokemon, r_pokemon):
    print_battle_info(p_pokemon, r_pokemon)
    selected_move = turn_menu(player_pokemon)
    calculate_damage(selected_move, p_pokemon, r_pokemon)


# Introduction and setup
read_csv_files()
introduction()
player_name = input('Enter player name: ')
player_name = player_name.strip().title()

# Grab 6 random, unique Pokemon from pokemon_list
selected_pokemon = random.sample(pokemon_list, 6)

# Populate each team's roster from the 6 random Pokemon
rocket_roster = selected_pokemon[:3]
player_roster = selected_pokemon[3:]

delay_print(f'\nTeam Rocket enters with {rocket_roster[0].name}, {rocket_roster[1].name}, {rocket_roster[2].name}\n')
delay_print(f'Team {player_name} enters with {player_roster[0].name}, {player_roster[1].name}, {player_roster[2].name}')

player_pokemon = player_roster.pop()
rocket_pokemon = rocket_roster.pop()
delay_print('\nTeam ' + player_name + ' sends ' + player_pokemon.name + ' to battle!\n')
delay_print(f'Team Rocket sends ' + rocket_pokemon.name + ' to battle!\n')

# Determine coin toss and first turn
print('\nCoin toss goes to ---- ', end='')
time.sleep(1)

player_turn_first = random.randint(0, 1)
if player_turn_first:
    print(f'Team {player_name} to start the attack!')
    print('Let the battle begin!\n')
    time.sleep(1)
else:
    print('Team Rocket to start the attack!')
    print('Let the battle begin!\n')
    time.sleep(1)
    rocket_turn(rocket_pokemon, player_pokemon)
    if player_pokemon.hit_points <= 0:
        player_pokemon = player_roster.pop()
        delay_print("Team " + player_name + " sends out " + player_pokemon.name + "!")


# Main gameplay loop
while True:
    player_turn(player_pokemon, rocket_pokemon)
    if rocket_pokemon.hit_points <= 0:
        if not rocket_roster:
            delay_print("Team " + player_name + " wins!")
            break
        rocket_pokemon = rocket_roster.pop()
        delay_print("Team Rocket sends out " + rocket_pokemon.name + "!")

    rocket_turn(rocket_pokemon, player_pokemon)
    if player_pokemon.hit_points <= 0:
        if not player_roster:
            delay_print("Team Rocket wins!")
            break
        player_pokemon = player_roster.pop()
        delay_print("Team " + player_name + " sends out " + player_pokemon.name + "!")
