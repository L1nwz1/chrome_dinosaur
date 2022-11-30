import pygame

class Dragon:
    # 恐龙的默认参数
    def __init__(self):
        self.rectangle = pygame.Rect(50, 210, 40, 45)  # 恐龙的边框,预先设计好就不需要移动到地上
        # 定义小恐龙的两种状态(读取图片放在列表里)
        self.image_status = [
            pygame.image.load('./images/dragon1.png'),
            pygame.image.load('./images/dragon2.png')
        ]
        self.status = 0 #初始0表示静止走路状态，1表示跳跃状态
        self.y = 210  # 恐龙的y坐标
        self.jump_flag = False  # 跳跃标志，判断恐龙是否跳跃
        self.jump_speed = 0  # 恐龙的跳跃速度，当为正的时候上升，为负的时候下降
        self.alive = True  # 初始状态为活着
        self.jump_status = True  # 恐龙的跳跃权限，如果在空中时不给跳跃

    # 更新恐龙的状态
    def update_v(self):
        if self.jump_flag:  # 如果检测到按下跳跃
            self.jump_speed = 15  # 将上升速度调为10
            self.jump_status = False  # 跳跃期间不给恐龙再次跳跃
            self.jump_flag = False  # 设置好后回复默认值等待下次跳跃

        if self.jump_speed != 0:  # 如果恐龙的跳跃速度不为0，说明正在跳跃周期
            self.y -= self.jump_speed  # 移动恐龙的Y坐标
            if self.y > 210:  # 防止将恐龙移动到地下
                self.y = 210
                self.jump_status = True  # 回到地上，允许跳跃
            self.rectangle[1] = self.y  # 将框真正移动

        if self.jump_status == False:  # 如果此时不允许跳跃，即正在跳跃过程中
            self.jump_speed -= 1  # 将速度降低，效果为上升越来越慢，下降越来越快

    def update(self):
        self.update_v()

