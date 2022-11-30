import pygame

class Map:
    # 默认参数
    def __init__(self):
        self.speed = 3
        self.background_1 = pygame.image.load('./images/background1.png')  # 加载图片
        self.background_2 = pygame.image.load('./images/background2.png')
        self.background_rectangle_1 = self.background_1.get_rect()  # 获取矩形区域
        self.background_rectangle_2 = self.background_2.get_rect()
        self.background_rectangle_2[0] = self.background_rectangle_1.right

    def map_update(self):
        self.background_rectangle_1 = self.background_rectangle_1.move(-self.speed, 0)  # 将背景向左移动
        self.background_rectangle_2 = self.background_rectangle_2.move(-self.speed, 0)
        if self.background_rectangle_1.right < 0:  # 判断第一个背景框如果移动到了窗口外面
            self.background_rectangle_1[0] = self.background_rectangle_2.right  # 将第一个背景框移动到第二个背景框后面，形成循环
        if self.background_rectangle_2.right < 0:  # 和上面同理，最终实现的效果就是两个图片排着队从窗口前划过
            self.background_rectangle_2[0] = self.background_rectangle_1.right
    def update(self):
        self.map_update()