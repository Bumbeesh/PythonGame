import pygame

class Button():
    def __init__(self,x,y,image, single_clicked):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.single_clicked = single_clicked

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not(self.clicked) :
                action = True
                if self.single_clicked:
                    self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image,self.rect)

        return action