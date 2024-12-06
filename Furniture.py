from pico2d import load_image,load_music,load_wav, draw_rectangle
import play_mode
import Game_world
import framework
from Foods import Foods
from Game_data import  what_input, Raw_food, cooking

class Cookware:
    sound = None
    def __init__(self, what, x, y,w,h):
        self.max_capacity = 2# 최대 조리 가능 음식 수
        self.held_item = []  # 보괸 중인 음식 목록
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        
        self.timer = framework.frame_time # 요리 시작시간

        self.ware = what
        self.image = load_image(f'image/furniture/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h

        self.sound = load_music(f'sound\{what}_sound.mp3')
        self.sound.set_volume(32)
        if Cookware.sound == None:
            Cookware.sound = load_wav('sound\sound.mp3')
            Cookware.sound.set_volume(16)

    def update(self):
        #음식 조리
        for ingredient in self.held_item:
            if ingredient.state != "cooked":
                ingredient.state == "cooking"
                if ingredient.inside_cookware != self.ware:
                    ingredient.inside_cookware = self.ware
                    ingredient.timer = play_mode.Ui.elapsed_time#조리 시작 시간
                    self.sound.repeat_play()

                ingredient.remaining_time = ingredient.timer - play_mode.Ui.elapsed_time

                if ingredient.remaining_time > ingredient.cook_time and ingredient.name in Raw_food:# 시간이 되면
                    self.sound.stop()#소리 멈춤
                    Cookware.sound.play()
                    ingredient.state = "cooked"#조리된다
                    ingredient.name = cooking[ingredient.name]
                    ingredient.image = load_image(f'image/food/{ingredient.name}.png')
                break
            
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())
        
    def handle_event(self, event):
        pass
    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            pass

    def add_food(self, food):
        food.held_by=self
        self.held_item.append(food)
        

    def remove_cooked_food(self):
        cooked_foods = [food for food in self.held_item if food.state == "cooked"]
        self.held_item = [food for food in self.held_item if food.state != "cooked"]
        return cooked_foods
  
    def remove_food(self, food):
        self.held_item.remove(food)
    def __getstate__(self):
        state = {"x":self.x, "y":self.y, "ware":self.ware,"held_item":self.held_item}
        return state
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
class Furniture:
    def __init__(self, what, left, bottom,right,top):
        self.max_capacity = float("inf")
        self.held_item=[]
        self.x = (left + right)/2
        self.y = (bottom + top)/2
        self.w = right-left
        self.h = top-bottom
        self.what = what
        self.image = load_image(f'image/furniture/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
          
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            pass
    def add_food(self, food):
        #점수를 주고 음식을 제거
        order=False
        for i in play_mode.orders:
            if food.name == i.food:
                play_mode.Ui.point+=i.point
                Game_world.remove_object(i)
                play_mode.orders.remove(i)
                order=True
                break
        if not order:
            play_mode.Ui.point+=50
        Game_world.remove_collision_object(food)
        Game_world.remove_object(food)
        what_input.append(food.name)
        del food
    def __getstate__(self):
        left, bottom,right,top=self.get_bb()
        state = {"what":self.what, "left":left, "bottom":bottom, "right":right, "top":top}
        return state
    def __setstate__(self, state):
        self.__init__()

class FoodBox:
    max_capacity = 2
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = load_image(f'image/furniture/food_box.png')
        self.imgW = self.image.w
        self.imgH = self.image.h

        self.food = what#음식의 종류
        self.held_item = []#보관중인 음식

        self.add_food()
    def update(self):
        #없으면 재생성
        if len(self.held_item) <= 0:
            self.add_food()
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass
    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            pass
    def add_food(self, food):
        food.held_by=self
        self.held_item.append(food)
    def add_food(self):
        food = Foods(self.food,self.x,self.y)
        food.held_by=self
        self.held_item.append(food)
        Game_world.add_object(food,4)
        Game_world.add_collision_pair('charater:food',None,food)
        Game_world.add_collision_pair('cookware:food',None,food)
    def remove_food(self, food):
        self.held_item.remove(food)
    def __getstate__(self):
        state = {"x":self.x, "y":self.y, "food":self.food,"held_item":self.held_item}
        return state
    def __setstate__(self, state):
        self.__init__(state["food"],state["x"],state["w"],state["h"])
        self.update(state)