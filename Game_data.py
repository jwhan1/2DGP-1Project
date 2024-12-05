import json

best_point=0
Game_point=[]
what_input=[]


#음식 종류
Ingredient = ['egg_whole_white', 'egg_fried', 'steak_raw', 'steak_grilled', 'fish_fillet', 'fish_sticks']
Raw_food = ['egg_whole_white','steak_raw','fish_fillet']
cooked_food =  ['egg_fried','steak_grilled','fish_sticks']
#조리되는 음식
cooking = {'egg_whole_white':'egg_fried','steak_raw':'steak_grilled','fish_fillet':'fish_sticks'}

#조리 도구들
Cookwares = ['gas_stove_pan','gas_stove_pot','chopping_board']


Ingredient_string = json.dumps(Ingredient)
print(type(Ingredient_string))
print(Ingredient_string)
value_string = '{"x":10,"y":10,"size":100}'
value=json.loads(value_string)
print(type(value))
print(value)

