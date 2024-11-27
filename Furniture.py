from pico2d import load_image, draw_rectangle
import play_mode
import Game_world
import framework
from Foods import Foods

class Cookware:
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_capacity = 5  # 최대 조리 가능 음식 수
        self.food_items = []  # 조리 중인 음식 목록
        
        self.timer = framework.frame_time # 요리 시작시간


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
        if len(self.food_items) < self.max_capacity:
            self.food_items.append(food)
            print(f"{food.name}을 조리한다")
        else:
            print("남은 공간이 없다!")

    def remove_cooked_food(self):
        cooked_foods = [food for food in self.food_items if food.state == "cooked"]
        self.food_items = [food for food in self.food_items if food.state != "cooked"]
        return cooked_foods
    
    def build_behavior_tree(self):
       pass


class Furniture:
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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
        print('on')
        play_mode.Ui.point+=100
        Game_world.remove_collision_object(food)
        Game_world.remove_object(food)
        del food
        pass

class FoodBox:
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h

        self.food = what#음식의 종류
        self.held_item = []#보관중인 음식
        self.held_item.append(Foods(what,self.x,self.y))
    def update(self):
        if self.held_item.index<=0:
            self.held_item.append(Foods(self.food ,self.x,self.y))
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
        pass
