from pico2d import load_image, draw_rectangle,load_font


class Cookware:
    font = load_font('ENCR10B.TTF', 16)
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stack=[]
        self.cooking=[]
        self.result=[]
        
        self.timer = 15#요리 시작 시간 self.timer - framework.frame_time : 흐르는 시간


        self.image = load_image(f'image/furniture/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h


       
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())
        Cookware.font.draw(self.x-10, self.y + 50, f'{self.timer:02d}', (255, 255, 0))
    def handle_event(self, event):
        pass
    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            pass

