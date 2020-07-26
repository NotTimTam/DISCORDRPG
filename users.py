# Imports
import json

def create_user(name, category):
  data={}
  data['users'].append({
    'name': name,
    'category': category
  })

  with open('users.json', 'a') as outfile:
    json.dump(data, outfile)

create_user("TIMTAM", "RETARD")