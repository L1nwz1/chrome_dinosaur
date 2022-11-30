import pygame
import sys
from dragon import Dragon
from map import Map

class Game:
    def __init__(self):
        pygame.init()  # 初始化
        self.flag = True # 创建一个flag标志用于在循环中判断使用哪张图片
        self.count = 0
        self.clock = pygame.time.Clock()  # 创建一个时间对象用于控制游戏运作的快慢
        self.screen = pygame.display.set_mode([734, 286])  # 创建并显示窗口

    def screen_update(self, jump_permission):
        '''更新背景'''
        self.screen.blit(map.background_1, map.background_rectangle_1)  # 将背景图片画到窗口上
        self.screen.blit(map.background_2, map.background_rectangle_2)

        self.count += 1
        self.count %= 100

        if jump_permission:  # 这个if语句是实现小恐龙踏步的
            if self.count % 20 == 0:  # 控制小恐龙速率
                '''更新小恐龙'''
                # 根据flag标志确定显示的图片，这样可以造成小恐龙在跑的现象
                if self.flag == True:
                    self.screen.blit(dragon.status[0], dragon.rectangle)
                else:
                    self.screen.blit(dragon.status[1], dragon.rectangle)
                self.flag = not self.flag
            else:
                if self.flag == True:
                    self.screen.blit(dragon.status[0], dragon.rectangle)
                else:
                    self.screen.blit(dragon.status[1], dragon.rectangle)
        else:  # 如果在空中那就显示两个图片，效果就是两个脚都平行（没有太大意义）
            self.screen.blit(dragon.status[0], dragon.rectangle)
            self.screen.blit(dragon.status[1], dragon.rectangle)

    def run(self):
        while True:
            self.clock.tick(60)  # 越大越快
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
                    sys.exit()  # 将窗口关闭
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if dragon.jump_permission:  # 如果检测到按键按下并且当前允许跳跃
                        dragon.jump_flag = True
            map.update()  # 更新地图元素框的位置
            dragon.update()
            self.screen_update(dragon.jump_permission)  # 根据框显示图片
            pygame.display.flip()

    def update(self):
        self.run()

if __name__ == "__main__":
    game = Game()
    map = Map()  # 创建地图实例
    dragon = Dragon()  # 创建小恐龙实例

    game.update()

    score = 0  # 设置初始分数
    # 这部分暂时测试用 现在背景的移动速度和时间成正比
    score += 1
    if score % 100 == 0:
        map.speed += 0.5
