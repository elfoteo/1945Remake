import pygame

label_img = pygame.transform.scale_by(pygame.image.load("sprites/ui/label.png"), 1.25)


class Label:
    def __init__(self, value, icon, pos, font: pygame.font.Font, prefix="", suffix=""):
        self.value = value
        self.icon = icon
        self.pos = pos
        self.font = font
        self.prefix = prefix
        self.suffix = suffix

    @staticmethod
    def get_width():
        return label_img.get_width()

    def draw(self, screen: pygame.Surface):
        screen.blit(label_img, self.pos)
        tmp_surf = self.font.render(self.prefix+str(self.value)+self.suffix, False, (255, 255, 255))
        screen.blit(tmp_surf, (self.pos[0]+label_img.get_width()-32-tmp_surf.get_width(),
                               self.pos[1]+label_img.get_height()/2-tmp_surf.get_height()/2))
        screen.blit(self.icon, (self.pos[0]+4, self.pos[1]+label_img.get_height()/2-self.icon.get_height()/2))

    def update(self, new_value):
        self.value = new_value
