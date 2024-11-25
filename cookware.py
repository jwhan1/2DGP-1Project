from pico2d import load_image, draw_rectangle,load_font
import framework
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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