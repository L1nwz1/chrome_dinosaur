from dinosaur import *

class Bullet:
    def __init__(self, game_speed, dinosaur):
        self.game_speed = game_speed
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.rect.x = dinosaur.dino_rect.x + dinosaur.dino_rect[2] + 10
        self.rect.y = dinosaur.dino_rect.y + dinosaur.dino_rect[3] / 2
        print(self.rect)

    def update(self):
        self.rect.x += self.game_speed
    def draw(self,SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))