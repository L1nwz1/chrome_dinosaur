from settings import *
import random

class Cloud:
    def __init__(self, game_speed):
        # 随机设定云的x，y坐标
        self.x = SCREEN_WIDTH + random.randint(200, 500) # 云先出现在游戏画面外，然后飞入
        self.y = random.randint(50, 200) # 云的y坐标，即离上部分区域的距离
        self.image = CLOUD # image 保存云的图片
        self.width = self.image.get_width()
        self.game_speed = game_speed

    def update(self):
        self.x -= self.game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))