from Game_data import Ingredient, cooked_food
import play_mode

from pico2d import get_canvas_height, get_canvas_width, load_font, load_image


from random import choice, randrange


class Order:
    image = None
    font = None
    def __init__(self, count):
        self.count = count
        self.x,self.y=get_canvas_width()-270, get_canvas_height()-80
        self.w,self.h = 60, 120
        self.food = choice(Ingredient)
        if self.food in cooked_food:
            self.point = randrange(300,500)
        else:
            self.point = randrange(110,150)
        self.image = load_image(f'image/food/{self.food}.png')


        if Order.font == None:
            Order.font = load_font('ENCR10B.TTF', 20)
        if Order.image == None:
            Order.image = load_image('image/order_paper.png')
    def update(self):
        count=0
        for i in play_mode.orders:
            if i == self:
                self.count=count
            count+=1
        pass
    def draw(self):
        Order.image.clip_draw(0, 0, Order.image.w, Order.image.h, self.x + 60 * self.count, self.y, self.w, self.h)

        Order.font.draw(self.x + 60 * self.count - 25, self.y-30,f"{self.point}P")
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + 60 * self.count, self.y + 15, 50, 50)
    def __getstate__(self):
        state = {"count":self.count, "food":self.food, "point":self.point, "image":self.image}
        return state
    def __setstate__ (self,state):
        self.__init__(state["count"])
        self.update(state)