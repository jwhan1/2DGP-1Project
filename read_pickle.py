import pickle
import json
from plistlib import loads


class NPC:
    def __init__(self,x,y,name):
        self.x,self.y,self.name=x,y,name

with open("game.sav",'wb') as f:
    group = pickle.loads(f)

for o in group:
    print(o.name,o.x,o.y)






npc1=NPC(100,100,"lala")
print(type(npc1.__dict__))
print(npc1.__dict__)

npc1.__dict__.update({'x':50})
characterdata = {"name":"gas_stove_pan","x":10,"y":10,"w":50,"h":50},
characterdata.update({"name":"gas_stove_pan","x":10,"y":10,"w":50,"h":50})

def create_new_world():
    with open('savedata.json','r') as f:
        savedata_list=json.load(f)
        for item in savedata_list:
            food=Cookware()
            food.__dict__.update(item)
            Game_world.add_object(food)

def load_world():
    pass



def save():
    group=[Ui, charater, foods, counter, cookwares, orders, walls]
    with open('game.sav', 'wb') as f:
        pass