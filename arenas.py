# Imports
import random, json
from users import data
from users import *


# Check if a fight is active.
def fight_active(data):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if data['fight_active'] == False:
        return False
    else:
        return True


# Boss name variables.
names = [
    'Wanjin', 'Malak', 'Sligo', 'Vuzembi', 'Makas', 'Jumoke', 'Nuenvan',
    'Seshi', 'Tzane', 'Rhazin', 'Yesha', 'Valja', 'Meenah', 'Zulmara',
    'Vanjin', 'Ronjaty', 'Ziataja', 'Ejie', 'Kanjin', 'Vonjai', 'Thanos'
]
status = [
    'Wise', 'Powerful', 'Godlike', 'Demented', 'Vengeful', 'Drunk', 'Crazed',
    'Infuriated', 'Fire-Breather', 'Tainted', 'Demonic', 'Destroyer',
    'Inevitable', 'Conquerer', 'All-Knowing', 'All-Seeing', 'Timeless',
    'Taboo', 'Hideous', 'Ugly'
]


# Create a name for the boss.
def boss_namer():
    boss_name = random.choice(names) + " the " + random.choice(status)
    return boss_name


# Create a boss fight.
def start_fight(data, name):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if not fight_active(data):
        data['fight_active'] = True
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        # Create difficulty settings.
        starter_level = data['users'][name]['level']
        difficulty_vector = round(random.uniform(1.0, 2.0), 2)
        difficulty = round((starter_level * difficulty_vector),2)

        # Create name.
        bossname = boss_namer()

        # Create health.
        health = difficulty * 10

        # Add boss to user list.
        data['users'].update({
            'boss': {
                'name': bossname,
                'difficulty': difficulty,
                'health': health,
                'fight_starter': name,
                'attackers': {}
            }
        })

        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        ret = ":crossed_swords: **" + name + "** started a fight at *difficulty* level **" + str(
            difficulty) + "** with ***" + bossname + "***! :crossed_swords:"
        return ret
    else:
        return ":scroll: Finish the current fight before starting another one... :scroll:"


# Calculate boss damage.
def give_damage(data):
    if fight_active(data):
        with open('users.json') as json_file:
            data = json.load(json_file)
        level = data['users']['boss']['difficulty']
        damage_vector = round(random.uniform(1.0, 2.0), 2)
        damage = level * damage_vector
        return damage
    else:
        return ":scroll: No fight currently active! :scroll:"


# Damage boss.
def damage_boss(data, damage_from):
    if fight_active(data):
        with open('users.json') as json_file:
            data = json.load(json_file)
        amount = player_give_damage(data, damage_from)
        name = get_bossname(data)
        data['users']['boss']['health'] -= amount
        data['users']['boss']['health'] = round(
            data['users']['boss']['health'], 2)
        if damage_from in data['users']['boss']['attackers']:
            data['users']['boss']['attackers'][damage_from] += 1
        else:
            data['users']['boss']['attackers'][damage_from] = 1
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        data['users']['boss']['attackers'][damage_from] = True
        if data['users']['boss']['health'] <= 0:
            data['users']['boss']['health'] = 0
            loot_list = []
            with open('users.json') as json_file:
                data = json.load(json_file)
            # LOOT
            fight_starter = data['users']['boss']['fight_starter']
            head = name + "'s head"
            if head in data['users'][fight_starter]['inventory']:
                data['users'][fight_starter]['inventory'][head] += 1
            else:
                data['users'][fight_starter]['inventory'][head] = 1
            for i in data['users']['boss']['attackers']:
                coins = round((data['users']['boss']['attackers'][i]) * round(
                    random.uniform(0.5, 3.0), 1))
                data['users'][i]['inventory']['coins'] += coins
                loot_list.append("**" + i + "** got **" + str(coins) +
                                 "** coins!")
                data['users'][i]['level'] += random.choice([0,1])
            ret = ":crossed_swords: **" + name + "** took **" + str(
                amount
            ) + "** damage from **" + damage_from + "**! Killing them instantly. The fight is now over. Congrats! :crossed_swords:\n\n:moneybag:**LOOT**:moneybag:"
            for i in loot_list:
                ret = ret + ("\n" + i)
            del data['users']['boss']
            data['fight_active'] = False
            with open('users.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            return ret
        else:
            damage = round(give_damage(data),2)
            ret = ":crossed_swords: **" + name + "** took **" + str(
                amount
            ) + "** damage! Leaving them with **" + str(
                data['users']['boss']['health']
            ) + "** health... :crossed_swords:\n" + ":crossed_swords: **" + name + "** retaliated against **" + damage_from + "** with **" + str(
                damage) + "** damage! :crossed_swords:\n" + str(
                    damage_player(data, damage_from, damage))
            return ret
    else:
        return ":scroll: No fight currently active! :scroll:"


# Get boss name...
def get_bossname(data):
    if fight_active(data):
        return data['users']['boss']['name']
    else:
        return ":scroll: No fight currently active! :scroll:"


#print(start_fight(data, "TimTam"))
#print(boss_namer())
