import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
