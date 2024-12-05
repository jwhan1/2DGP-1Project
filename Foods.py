from pico2d import load_image, draw_rectangle, load_font
import StateMachine
import framework
import time
from Game_data import Raw_food, cooked_food
whatfood = {'apple_green','apple_red','apple_yellow','abocado_whole',
            'banana','beet','blueberries',
            'cantaloupe_whole','carrot','cheese','cherries',
            'tomato',
            'watermelon',
            'strawberry'}

class Foods:
    
    def __init__(self, name, x, y):
        self.x, self.y = x, y # 위치
        self.w, self.h = 50, 50 # 크기
        self.name = name#음식 이름
        self.state = "raw"  # raw -> cooking -> cooked
        self.timer = time.time()
        self.cook_time = 8  # 조리 완료 시간 (초)
        self.remaining_time = 8  # 남은 조리 시간

        self.held_by = None  # 현재 들고 있는 캐릭터 (없으면 None)
        self.inside_cookware = None #조리중인 조리도구(다른 도구에 들어갈 때 갱신)
        self.image = load_image(f'image/food/{self.name}.png')

        self.imgW, self.imgH = self.image.w, self.image.h # 이미지 크기
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass
    def move_to(self,held):
        if self.held_by:
            self.held_by.remove_food(self)
        self.w, self.h = 50, 50
        self.x = held.x
        self.y = held.y
        self.timer = time.time()
        held.add_food(self)
#충돌
    def get_bb(self):
       return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            pass
    




