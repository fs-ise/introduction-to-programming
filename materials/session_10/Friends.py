

friends = {'friend1' : {'name':'Peter', 'likes':['biking', 'techno'], 'food_intolerances':['pepper', 'cucumber']},
           'friend2' : {'name':'Maria', 'likes':['dancing', 'skiing'], 'food_intolerances':['nuts']}}

import json
file = open('friends.db', 'w')
json.dump(friends, file)

# Remove all variables from kernel namespace

import json
file = open('friends.db', 'r')
friends = json.load(file)

friends
friends['friend1']
friends['friend1']['name']
friends['friend2']['likes']

friends['friend3'] = {'name':'Jane', 'age':22, 'likes':['hiking', 'dancing'], 'food_intolerances':['gluten', 'milk']}

friends['friend1']['likes'].append('reading')

del friends['friend3']['age']

del friends['friend1']

file = open('friends.db', 'w')
json.dump(friends, file)

