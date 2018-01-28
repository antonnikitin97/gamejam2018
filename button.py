import pygame

class Button:
    def __init__(self, screen, x, y, sprite, pressfunction):
        self.screen = screen
        self.x = x
        self.y = y
        self.sprite = sprite
        self.highlitsprite = sprite.copy()
        self.highlitsprite.fill((100, 20, 255, 20), special_flags=pygame.BLEND_RGBA_SUB)
        self.collider = pygame.Rect(self.x - (self.sprite.get_width() / 2), self.y,
                                    sprite.get_width(), sprite.get_height())
        self.pressfunction = pressfunction
    
    def show(self, highlight):
        mouseover = self.collider.collidepoint(pygame.mouse.get_pos())
        if highlight or mouseover:
            self.screen.blit(self.highlitsprite, (self.x - (self.sprite.get_width() / 2), self.y))
        else:
            self.screen.blit(self.sprite, (self.x - (self.sprite.get_width() / 2), self.y))
        if pygame.mouse.get_pressed()[0] and mouseover:
            self.pressfunction()

class ButtonWithStuffOn:
    def __init__(self, screen, x, y, sprite, image, sound, pressfunction):
        self.screen = screen
        self.x = x
        self.y = y
        self.sprite = sprite
        self.image = image
        self.sound = sound
        self.highlitsprite = sprite.copy()
        self.highlitsprite.fill((100, 20, 255, 20), special_flags=pygame.BLEND_RGBA_SUB)
        self.collider = pygame.Rect(self.x - (self.sprite.get_width() / 2), self.y,
                                    sprite.get_width(), sprite.get_height())
        self.pressfunction = pressfunction
        self.channel = pygame.mixer.Channel(3)
    
    def show(self, highlight):
        mouseover = self.collider.collidepoint(pygame.mouse.get_pos())
        if highlight or mouseover:
            self.screen.blit(self.highlitsprite, (self.x - (self.sprite.get_width() / 2), self.y))
            if not self.channel.get_busy():
                self.channel.play(self.sound)
        else:
            self.screen.blit(self.sprite, (self.x - (self.sprite.get_width() / 2), self.y))
        self.screen.blit(self.image, ((self.x - self.image.get_width()/2), self.y + 50 + self.image.get_height()/2))
        if pygame.mouse.get_pressed()[0] and mouseover:
            self.pressfunction()