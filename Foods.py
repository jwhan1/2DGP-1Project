from pico2d import load_image, draw_rectangle, load_font
import StateMachine
import framework
import time

whatfood = {'apple_green','apple_red','apple_yellow','abocado_whole',
            'banana','beet','blueberries',
            'cantaloupe_whole','carrot','cheese','cherries',
            'tomato',
            'watermelon',
            'strawberry'}

class Foods:
    
    def __init__(self, what, x, y):
        self.x, self.y = x, y # 위치
        self.w, self.h = 50, 50 # 크기
        self.name = what#음식 이름
        self.state = "raw"  # raw -> cooking -> cooked
        self.cook_time = 180  # 조리 완료 시간 (초)
        self.remaining_time = 180  # 남은 조리 시간

        self.held_by = None  # 현재 들고 있는 캐릭터 (없으면 None)
        self.inside_cookware = None #현재 들어간 조리도구
        self.image = load_image(f'image/food/{what}.png')

        self.imgW, self.imgH = self.image.w, self.image.h # 이미지 크기
    def update(self):
        #조리도구에 들어가면
        if self.state == "raw": 
            self.state = "cooking"
            self.cook_time = time.time() + 15
        self.remaining_time = self.cook_time - time.time()

        if self.remaining_time <= 0:
            self.state = "cooked"
            self.remaining_time = 0
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
#충돌
    def get_bb(self):
       return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            if group == 'charater:food' and  (other.held_item == None or other.held_item == self):
                pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
