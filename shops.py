# Imports
import random, json

# Open Data File.
with open('shops.json') as json_file:
    shopdata = json.load(json_file)


# Check whats in the shop.
def check_shop(shopdata):
    shop = []
    for i in shopdata['shop']:
        string = str(i) + " | " + str(shopdata['shop'][i])
        shop.append(string)
    return shop
    with open('shops.json', 'w') as outfile:
        json.dump(shopdata, outfile, indent=4)
