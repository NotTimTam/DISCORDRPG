# Imports.
import json
import random

# Open Data File.
with open('users.json') as json_file:
    data = json.load(json_file)

# List of consumable items...
consumables = ['health potion', 'mysterious bag', 'ancient relic', 'cram']


# Create a user.
def create_user(data, name, category):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if not user_exists(data, name):
        data['users'].update({
            name: {
                'category': category,
                'level': 1,
                'health': 10,
                'inventory': {
                    'sword': 1,
                    'coins': 5
                }
            }
        })
    else:
        ret = ":no_entry_sign: **" + name + "** already exists! :no_entry_sign:"
        return ret

    with open('users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    output = ":scroll: Started **" + name + "** on their quest as a **" + category + "**! :scroll:"
    return output


# Check if a user exists.
def user_exists(data=data, name='username'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if name in data['users']:
        return True
    else:
        return False


# Level up a user.
def level_up_user(data=data, name='username'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        data['users'][name]['level'] += 1
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        ret = ":scroll: **" + name + "** is now level **" + str(
            data['users'][name]['level']) + "**! :scroll:"
        return ret
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Check a user's class.
def check_class(data=data, name='username'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        cls = data['users'][name]['category']
        ret = ":scroll: **" + name + "**'s class is **" + cls + "**! :scroll:"
        return ret
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Get contents of a user's inventory.
def get_inventory(data=data, name='username'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        inv = []
        for i in data['users'][name]['inventory']:
            string = str(i) + " | " + str(data['users'][name]['inventory'][i])
            inv.append(string)
        return inv
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Check if user has a certain amount of money.
def check_balance(data=data, name='username', price=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        if data['users'][name]['inventory']['coins'] >= price:
            return True
        else:
            return False
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Check if user has an item.
def check_item(data=data, name='username', item='item name', amount=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        try:
            if data['users'][name]['inventory'][item] >= amount:
                return True
            else:
                return False
        except:
            return False
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Check user stats.
def check_stats(data=data, name='username'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        stats = []
        stats.append("Class | " + str(data['users'][name]['category']))
        stats.append("Level | " + str(data['users'][name]['level']))
        stats.append("Health | " + str(data['users'][name]['health']))
        return stats
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Purchase item for user.
def make_purchase(data=data,
                  name='username',
                  price=1,
                  item="healing potion",
                  item_count=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        if check_balance(data, name, price):
            data['users'][name]['inventory']['coins'] -= price
            if item in data['users'][name]['inventory']:
                data['users'][name]['inventory'][item] += 1
            else:
                data['users'][name]['inventory'][item] = 1
            with open('users.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            ret = "**" + name + "** purchased **" + str(
                item_count) + " " + item + "** for **$" + str(price) + "**..."
            return ret
        else:
            return ":no_entry_sign:  Failed to make purchase. Not Enough money... :no_entry_sign:"
    else:
        ret = "**" + name + "** doesn't exist!"
        return ret


# Give item to another user.
def give_item(data=data,
              name='username',
              other_person="other_username",
              item="healing potion",
              item_count=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        if user_exists(data, other_person):
            if check_item(data, name, item, item_count) == True:
                data['users'][name]['inventory'][item] -= item_count
                if item in data['users'][other_person]['inventory']:
                    data['users'][other_person]['inventory'][
                        item] += item_count
                else:
                    data['users'][other_person]['inventory'][item] = item_count
                with open('users.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                ret = ":handshake: **" + name + "** gave **" + str(
                    item_count
                ) + " " + item + "** to **" + other_person + "**! :handshake:"
                return ret
            else:
                ret = ":no_entry_sign: Sender **" + name + "** doesn't have enough **" + item + "**! :no_entry_sign:"
                return ret
        else:
            ret = ":no_entry_sign: Reciever **" + other_person + "** doesn't exist! :no_entry_sign:"
            return ret
    else:
        ret = ":no_entry_sign: Sender **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Damage player.
def damage_player(data=data, name='username', amount=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        amount = round(amount, 2)
        data['users'][name]['health'] -= amount
        data['users'][name]['health'] = round(data['users'][name]['health'], 2)
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        if data['users'][name]['health'] <= 0:
            data['users'][name]['health'] = (
                10 * data['users'][name]['level']) / 2
            ret = ":dizzy_face: **" + name + "** took **" + str(
                amount
            ) + "** damage! *Killing* them instantly.\nThey have now been revived to half HP at the cost of 5 gold coins. :dizzy_face:"
            if data['users'][name]['inventory']['coins'] >= 5:
                data['users'][name]['inventory']['coins'] -= 5
            elif data['users'][name]['inventory']['coins'] < 5:
                data['users'][name]['inventory']['coins'] = 0
            with open('users.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            return ret
        else:
            ret = ":heart: **" + name + "** took **" + str(
                amount) + "** damage! Leaving them with **" + str(
                    data['users'][name]['health']) + "** HP... :heart:"
            with open('users.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            return ret
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Player attack system.
def player_give_damage(data, name):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        level = data['users'][name]['level']
        damage_vector = round(random.uniform(1.0, 4.0), 2)
        damage = level * damage_vector
        return damage
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Player change class.
def change_class(data, name, value):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        data['users'][name]['category'] = value
        ret = ":scroll: Changed **" + name + "'s** class to **" + value + "**! :scroll:"
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return ret
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Give player an item.
def give_player_item(data=data, name='username', itemname="item", amount=1):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        if itemname in data['users'][name]['inventory']:
            data['users'][name]['inventory'][itemname] += amount
        else:
            data['users'][name]['inventory'][itemname] = amount
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        ret = ":scroll: An Administrator gave **" + name + " " + str(
            amount) + " " + itemname + "**! :scroll:"
        return ret
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret


# Consume an item.
def consume_item(data=data, name='username', itemname='item'):
    with open('users.json') as json_file:
        data = json.load(json_file)
    if user_exists(data, name):
        if check_item(data, name, itemname, 1) == True:
            if itemname in consumables:
                data['users'][name]['inventory'][itemname] -= 1
                if itemname == 'health potion':
                    data['users'][name]['health'] += (
                        (10 * data['users'][name]['level']) / 2)
                    with open('users.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
                    ret = ":package: **" + name + "** consumed their **" + itemname + "** for half HP!:package:"
                    return ret
                elif itemname == 'ancient relic':
                    with open('users.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
                    ret = ":package: **" + name + "** consumed their **" + itemname + "**... *Nothing* happened.:package:"
                    return ret
                elif itemname == 'mysterious bag':
                    bagdrop = random.choice([
                        'health potion', 'health potion', 'health potion',
                        'health potion', 'health potion', 'ancient relic'
                    ])
                    if bagdrop in data['users'][name]['inventory']:
                        data['users'][name]['inventory'][bagdrop] += 1
                    else:
                        data['users'][name]['inventory'][bagdrop] = 1
                    with open('users.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
                    ret = ":package: **" + name + "** opened a *mysterious bag* and it dropped a **" + bagdrop + "**!:package:"
                    return ret
            else:
                ret = ":no_entry_sign: **" + itemname + "** isn't consumable... :no_entry_sign:"
                return ret
        else:
            ret = ":no_entry_sign: **" + name + "** doesn't have a **" + itemname + "**... :no_entry_sign:"
            return ret
    else:
        ret = ":no_entry_sign: **" + name + "** doesn't exist! :no_entry_sign:"
        return ret
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


# Examples.
# print(check_class(data, "TimTam"))
# print(level_up_user(data, "TimTam"))
# print(create_user(data, "TimTam", "Dungeon Master"))
# print(user_exists(data, "steven"))
# print(get_inventory(data, "TimTam"))
# print(check_balance(data, "TimTam", 5))
# print(make_purchase(data, "TimTam", 5, "healing potion", 1))
# print(check_item(data, "TimTam", "healing potion"))
# print(give_item(data, "TimTam", "Philip", "healing potion", 1))
# print(damage_player(data, "TimTam", 7846578))
# print(check_stats(data, "TimTam"))
# print(give_damage(data, "TimTam"))
