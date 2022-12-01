from settings import *

class Dinosaur:
    X_ori = 80 # 恐龙的初始x坐标
    Y_ori = 310 # 恐龙的初始y坐标
    Y_ori_DUCK = 340 # 恐龙的初始低头y坐标
    ORI_V = 7 # 恐龙的初始跳跃速度

    def __init__(self):
        # 读入setting中恐龙三种状态所属的列表图片
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # 恐龙的三种状态：低头，奔跑，跳跃
        self.status = 1 # 状态机：0表示低头， 1表示奔跑， 2表示跳跃状态

        self.index = 0
        self.v = self.ORI_V # 设定初始速度为ORI_V
        self.image = self.run_img[0] # 初始的跑步动作下标为0
        self.dino_rect = self.image.get_rect() # get_rect是获取图像的位置信息以及宽度高度
        self.dino_rect.x = self.X_ori
        self.dino_rect.y = self.Y_ori

    def update(self, userInput): # userInput <== 键盘输入
        # 三种状态不断切换
        if self.status == 0:
            self.duck()
        if self.status == 1:
            self.run()
        if self.status == 2:
            self.jump()

        if self.index >= 10:
            self.index = 0

        # 读入按键，要额外判定恐龙是否处于跳跃状态，不然就会连跳
        if userInput[pygame.K_UP] and not self.status == 2:
            self.status = 2
        elif userInput[pygame.K_DOWN] and not self.status == 2:
            self.status = 0
        elif not (userInput[pygame.K_DOWN] or self.status == 2):
            self.status = 1

    def duck(self):
        self.image = self.duck_img[self.index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_ori
        self.dino_rect.y = self.Y_ori_DUCK
        self.index += 1

    def run(self):
        self.image = self.run_img[self.index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_ori
        self.dino_rect.y = self.Y_ori
        self.index += 1

    def jump(self):
        self.image = self.jump_img
        if self.status == 2:
            self.dino_rect.y -= self.v * 5 # 在空中下降
            self.v -= 0.5 # 加速度为-0.5
        if self.v < - self.ORI_V: # 恢复初始跳跃速度
            self.status = 1
            self.v = self.ORI_V

    # 定义draw函数以刷新画面
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    # 死亡动画
    def draw_death(self,SCREEN):
        SCREEN.blit(DEAD, (self.dino_rect.x, self.dino_rect.y))
