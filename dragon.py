import pygame

class Dragon:
    # 小恐龙的默认参数
    def __init__(self):
        self.rectangle = pygame.Rect(50, 210, 40, 45)  # 小恐龙的边框,预先设计好就不需要移动到地上
        # 定义小恐龙的两种状态(读取图片放在列表里)
        self.status = [
            pygame.image.load('./images/dragon1.png'),
            pygame.image.load('./images/dragon2.png')
        ]
        self.Y_axis = 210  # 小恐龙所在Y轴坐标
        self.jump_flag = False  # 跳跃标志，判断小恐龙是否跳跃
        self.jump_speed = 0  # 小恐龙的跳跃速度，当为正的时候上升，为负的时候下降
        self.alive = True  # 生命状态，默认为活着
        self.jump_permission = True  # 小恐龙的跳跃权限，如果在空中时不给跳跃

    # 更新小恐龙的状态
    def update_v(self):
        if self.jump_flag:  # 如果检测到按下跳跃
            self.jump_speed = 15  # 将上升速度调为10
            self.jump_permission = False  # 跳跃期间不给小恐龙再次跳跃
            self.jump_flag = False  # 设置好后回复默认值等待下次跳跃

        if self.jump_speed != 0:  # 如果小恐龙的跳跃速度不为0，说明正在跳跃周期
            self.Y_axis -= self.jump_speed  # 移动小恐龙的Y坐标
            if self.Y_axis > 210:  # 防止将小恐龙移动到地下
                self.Y_axis = 210
                self.jump_permission = True  # 回到地上，允许跳跃
            self.rectangle[1] = self.Y_axis  # 将框真正移动

        if self.jump_permission == False:  # 如果此时不允许跳跃，即正在跳跃过程中
            self.jump_speed -= 1  # 将速度降低，效果为上升越来越慢，下降越来越快

    def update(self):
        self.update_v()

