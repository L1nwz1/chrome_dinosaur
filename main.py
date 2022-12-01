import pygame
import os
import random
from settings import *
from dinosaur import Dinosaur

pygame.init() # 初始化pygame
pygame.display.set_caption('chrome dinosaur') # 设置标题

class Cloud:
    def __init__(self):
        # 随机设定云的x，y坐标
        self.x = SCREEN_WIDTH + random.randint(200, 500) # 云先出现在游戏画面外，然后飞入
        self.y = random.randint(50, 200) # 云的y坐标，即离上部分区域的距离
        self.image = CLOUD # image 保存云的图片
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Barrier: # 定义一个障碍物基类， 后面的各个障碍物都是Barrier的子类
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH # 先把障碍物放到地图的右下角，然后出来

    def update(self):
        self.rect.x -= game_speed # x坐标向左移动，即障碍物向左移动
        if self.rect.x < -self.rect.width: # 还需要判断障碍物是否移出了边界，如果越界的话我们要把该障碍物释放掉
            barriers.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Barrier):
    def __init__(self, image):
        self.type = random.randint(0, 2) #随机生成0-2下标，即随机生成3种小仙人掌中的一个
        super().__init__(image, self.type) # super调用父类对象的方法
        self.rect.y = 325

class LargeCactus(Barrier):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Barrier):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_ori_bg, y_ori_bg, points, barriers
    run = True

    clock = pygame.time.Clock()
    player = Dinosaur() # player是Dinosaur的一个对象
    cloud = Cloud()

    game_speed = 15 # 游戏的速度
    # 设置背景图片的初始位置
    x_ori_bg = 0
    y_ori_bg = 380
    points = 0
    font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], 20) # 分数的字体
    barriers = []
    death_cnt = 0 # 记录死亡次数，death_cnt== 0大于0的话就会显示重开界面


    def score():
        global points, game_speed
        points += 1
        if points % 150 == 0: # 分数每过150速度加1，时间越长速度越快
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0)) # render（内容，是否抗锯齿，字体颜色，字体背景颜色）
        textRect = text.get_rect()
        textRect.center = (550, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_ori_bg, y_ori_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_ori_bg, y_ori_bg)) # 保证图片连续
        SCREEN.blit(BG, (image_width + x_ori_bg, y_ori_bg))
        if x_ori_bg <= -image_width: # 越界
            SCREEN.blit(BG, (image_width + x_ori_bg, y_ori_bg))
            x_ori_bg = 0
        x_ori_bg -= game_speed # 背景图片每帧往左移game_speed个单位

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255)) # 背景填充为白色
        userInput = pygame.key.get_pressed() # 从键盘读入按键

        player.draw(SCREEN)
        player.update(userInput) # 调用dinosaur的update函数

        # 如果还没有障碍物，那么生成一个障碍物
        if len(barriers) == 0:
            # 随机等可能生成障碍物
            if random.randint(0, 2) == 0:
                barriers.append(SmallCactus(SMALL_CACTUS)) # 向列表添加障碍物元素
            elif random.randint(0, 2) == 1:
                barriers.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                barriers.append(Bird(BIRD))

        for barrier in barriers:
            barrier.draw(SCREEN) # 调用barrier类的draw函数，渲染画面
            barrier.update()
            if player.dino_rect.colliderect(barrier.rect): # pygame的一个方法colliderect检测两个物体是否碰撞
                SCREEN.blit(DEAD, (player.dino_rect.x, player.dino_rect.y))
                pygame.time.delay(2000)
                death_cnt += 1
                menu(death_cnt) # 调出死亡界面

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(60) #60fps
        pygame.display.update()


def menu(death_cnt):
    global points # 设置分数
    run = True
    while run:
        SCREEN.fill((255, 255, 255)) # 背景色设置为白色
        font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], 50) # 设置字体

        if death_cnt == 0:
            text = font.render("Press any key to start", True, (0, 0, 0))
        elif death_cnt > 0:
            text = font.render("Press any key to restart", True, (0, 0, 0))
            score = font.render("Score: " + str(points), True, (0, 0, 0)) # 分数变化
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50) # 将分数显示在游戏屏幕中间
            SCREEN.blit(score, scoreRect) # 将score图片画在SCREEN画面上
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140)) #把恐龙的图片显示在菜单界面
        pygame.display.update() # 更新画面
        # 判断各个事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
# 开始界面
menu(death_cnt=0)