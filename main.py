import random

import pygame.time

from settings import *
from dinosaur import Dinosaur
from cloud import Cloud
from bullet import Bullet


pygame.init() # 初始化pygame
pygame.display.set_caption('chrome dinosaur') # 设置标题

class Barrier: # 定义一个障碍物基类， 后面的各个障碍物都是Barrier的子类
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH # 先把障碍物放到地图的右下角，然后出来
        self.game_speed = game_speed
        self.hp = 100 # 血量
    def update(self):
        self.rect.x -= self.game_speed # x坐标向左移动，即障碍物向左移动
        if self.rect.x < -self.rect.width or self.hp <= 0: # 还需要判断障碍物是否移出了边界，如果越界的话我们要把该障碍物释放掉
            barriers.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    # 头顶显示血量
    def showHp(self):
        font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], 30)
        text = font.render("Hp: " + str(self.hp), True, (0, 0, 0))
        SCREEN.blit(text, (self.rect.x, self.rect.y - 20))

    def showHit(self):
        font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], 30)
        text = font.render("┗|`O'|┛", True, (0, 0, 0))
        SCREEN.blit(text, (self.rect.x, self.rect.y - 70))
# barriers的子类
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
        self.ori_vy = 5
        self.vy = self.ori_vy

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1
    def update(self): # 多态实现鸟的上下移动
        self.rect.x -= self.game_speed
        if self.rect.x < -self.rect.width or self.hp <= 0: # 还需要判断障碍物是否移出了边界，如果越界的话我们要把该障碍物释放掉
            barriers.pop()
        self.rect.y -= self.vy * 3
        self.vy -= 0.5
        if self.rect.y <= 0:
            self.vy = self.ori_vy
            self.vy = -self.vy
        elif self.rect.y >= SCREEN_HEIGHT - 250:
            self.vy = 10
def menu(death_cnt):
    global points, max_score# 引入points, max_score全局变量
    run = True
    while run:
        SCREEN.fill((255, 255, 255)) # 背景色设置为白色
        font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], 50) # 设置字体


        if death_cnt == 0:
            text = font.render("Press Any Key To Start", True, (0, 0, 0))
        elif death_cnt > 0:
            text = font.render("Press Any Key To Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0)) # 分数
            if death_cnt == 1:
                max_score = points
            else:
                max_score = max(max_score, points)
            maxScore = font.render("Max Score: " + str(max_score), True, (0, 0, 0)) # 最高分

            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50) # 将分数显示在游戏屏幕中间
            SCREEN.blit(GAMEOVER, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200)) # 显示GAMEOVER图片
            SCREEN.blit(score, scoreRect) # 显示分数
            SCREEN.blit(maxScore, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 + 70)) # 显示最高分数
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 140)) #把恐龙的图片显示在菜单界面
        pygame.display.update() # 更新画面
        # 判断各个事件, 开始游戏
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                run = False
            if event.type == pygame.KEYUP:
                main()


def main():
    global game_speed, x_ori_bg, y_ori_bg, points, barriers, death_cnt, barrier, clock_cnt
    run = True

    clock = pygame.time.Clock()

    game_speed = 5  # 游戏的速度
    player = Dinosaur(game_speed) # 实例化对象

    cloud = Cloud(game_speed)

    # 设置背景图片的初始位置
    x_ori_bg = 0
    y_ori_bg = 380
    points = 0
    font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], 20) # 分数的字体

    # 设置障碍物列表
    barriers = []
    # 设置子弹列表
    bullets = []

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
        SCREEN.blit(BG, (x_ori_bg, y_ori_bg))
        SCREEN.blit(BG, (image_width + x_ori_bg, y_ori_bg)) # 保证图片连续
        if x_ori_bg <= -image_width: # 越界
            SCREEN.blit(BG, (image_width + x_ori_bg, y_ori_bg))
            x_ori_bg = 0
        x_ori_bg -= game_speed # 背景图片每帧往左移game_speed个单位

    flag_hit = 0  # 标记恐龙是否被击中过
    death_cnt = 0  # 记录死亡次数，death_cnt = 0显示开始界面，大于0的就会显示重开界面
    last_timestamp = 0  # 记录时钟记录的上一个时刻
    last_timestamp_hit = 0 # 记录恐龙受到伤害时钟记录的上一个时刻
    last_timestamp_barr_hit = 0 # 记录障碍物受到伤害时钟记录的上一个时刻
    flag_barr_hit = 0 # 记录障碍物有没有受得伤害


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255)) # 背景填充为白色
        userInput = pygame.key.get_pressed() # 从键盘读入按键

        # 3s内显示血量的简单逻辑

        if flag_hit == 1:
            if pygame.time.get_ticks() - last_timestamp_hit <= 3000:
                player.showHit()
            if pygame.time.get_ticks() - last_timestamp_hit > 3000:
                flag_hit = 0




        background()  # 画出背景

        cloud.draw(SCREEN)  # 画出云的图像
        cloud.update()  # 更新云的位置

        score()  # 显示分数

        clock.tick(60)  # 60fps

        # 如果还没有障碍物，那么生成一个障碍物
        if len(barriers) <= 1:

            # 防止障碍物为0的情况下恐龙闪烁
            player.draw(SCREEN)  # 渲染恐龙画面
            player.update(userInput)  # 调用dinosaur的update函数每次渲染都判断一次是否按下相应的键位
            player.showHp()

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
            barrier.showHp() # 显示血量

            if flag_barr_hit == 1:
                if barrier.hp < 100 and pygame.time.get_ticks() - last_timestamp_barr_hit <= 3000:
                    barrier.showHit()
                if pygame.time.get_ticks() - last_timestamp_barr_hit > 3000:
                    flag_barr_hit = 0

            if player.dino_rect.colliderect(barrier.rect): # pygame的一个方法colliderect检测两个物体是否碰撞
                last_timestamp_hit = pygame.time.get_ticks()
                player.hp -= 1  # 被击中生命值减1
                flag_hit = 1
                if not len(barriers) == 0:
                    barriers.remove(barrier)
            else:
                player.draw(SCREEN)  # 渲染恐龙画面
                player.update(userInput)  # 调用dinosaur的update函数每次渲染都判断一次是否按下相应的键位
                player.showHp()

            if player.hp == 0: # 血量为0时
                player.showDead()
                player.draw_death(SCREEN)
                pygame.display.update() # 显示死亡动画
                pygame.time.delay(1000)
                death_cnt += 1
                menu(death_cnt) # 调出死亡界面

            # 子弹击中障碍物部分
            for bullet in bullets:
                bullet.draw(SCREEN)
                bullet.update()
                if bullet.rect.x > SCREEN_WIDTH:
                    if not len(bullets):
                        bullets.remove(bullet)
                if bullet.rect.colliderect(barrier.rect):
                    last_timestamp_barr_hit = pygame.time.get_ticks()
                    barrier.hp -= 50
                    flag_barr_hit = 1
                    bullets.remove(bullet)
                    if not len(barriers) == 0 and barrier.hp <= 0:
                        points += 50
                        barriers.remove(barrier)


        # 发射子弹， 并且保证每个子弹的发射间隔小于200毫秒
        if (userInput[pygame.K_SPACE] and pygame.time.get_ticks() - last_timestamp >= 200) or (userInput[pygame.K_SPACE] and last_timestamp == 0):
            last_timestamp = pygame.time.get_ticks() # 更新当前时间
            bullets.append(Bullet(game_speed, player))

        pygame.display.update()

if __name__ == '__main__':
    menu(death_cnt = 0)
    main()
