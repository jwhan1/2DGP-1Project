from pico2d import load_image, draw_rectangle
import time
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
        self.held_item = []  # 보괸 중인 음식 목록
        
        self.timer = framework.frame_time # 요리 시작시간

        self.ware = what
        self.image = load_image(f'image/furniture/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h

    def update(self):
        #음식 조리
        if len(self.held_item) > 0:
            self.held_item[0].state = "cooking"
            if self.held_item[0].inside_cookware != self.ware:
                self.held_item[0].inside_cookware = self.ware
                self.timer = time.time()#조리 시작
                self.held_item[0].remaining_time = self.held_item[0].cook_time#조리 시간

            self.held_item[0].remaining_time = self.held_item[0].cook_time - (time.time() - self.timer)

            if self.held_item[0].remaining_time < 0:# 시간이 되면
                self.held_item[0].state="cooked"#조리된다

        
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
        if len(self.held_item) < self.max_capacity:
            food.held_by=self
            self.held_item.append(food)
            print(f"{food.name}을 조리한다")
        else:
            print("남은 공간이 없다!")

    def remove_cooked_food(self):
        cooked_foods = [food for food in self.held_item if food.state == "cooked"]
        self.held_item = [food for food in self.held_item if food.state != "cooked"]
        return cooked_foods
  
    def remove_food(self, food):
        self.held_item.remove(food)


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
        play_mode.Ui.Point.point+=100
        play_mode.Ui.add_point(food.name)
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
        Game_world.add_object(food,1)
        Game_world.add_collision_pair('charater:food',None,food)
        Game_world.add_collision_pair('cookware:food',None,food)
    def remove_food(self, food):
        self.held_item.remove(food)

