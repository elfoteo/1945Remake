import pygame

pygame.font.init()


def darken_texture(texture, intensity):
    """Darkens a given texture by a given intensity"""
    w, h = texture.get_size()
    dark_texture = pygame.Surface((w, h), pygame.SRCALPHA)
    dark_color = (intensity * 255, intensity * 255, intensity * 255, 255)
    dark_texture.fill(dark_color)
    dark_texture.blit(texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return dark_texture


class Button:
    def __init__(self, x, y, width, height, texture, text=None, color=(255, 255, 255), font=None,
                 increase_font_size=0.0):
        self.rect = pygame.Rect(x, y, width, height)
        if type(texture) == pygame.Surface:
            self.texture = texture
        else:
            self.texture = pygame.image.load(texture)
        self.texture = pygame.transform.scale(self.texture, (width, height))
        self.texture_hover = pygame.transform.scale(self.texture, (width, height))
        self.texture_down = darken_texture(self.texture.copy(), 0.7)
        self.is_hovered = False
        self.is_clicked = False
        self.text = text
        self.text_color = color
        if font is None:
            self.font = pygame.font.Font(None, int(self.rect.height * (0.4 + increase_font_size)))
        else:
            self.font = pygame.font.Font(font, int(self.rect.height * (0.3 + increase_font_size)))

    def draw(self, screen):
        if self.is_clicked:
            screen.blit(self.texture_down, self.rect)
        elif self.is_hovered:
            screen.blit(self.texture_hover, self.rect)
        else:
            screen.blit(self.texture, self.rect)

        if self.is_clicked:
            if self.text is not None:
                text = self.font.render(self.text, True, (
                    round(self.text_color[0] * 0.7), round(self.text_color[1] * 0.7),
                    round(self.text_color[2] * 0.7)))
                text_rect = text.get_rect(center=self.rect.center)
                screen.blit(text, text_rect)
        else:
            if self.text is not None:
                text = self.font.render(self.text, True, self.text_color)
                text_rect = text.get_rect(center=self.rect.center)
                screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_clicked = False
                    return True
                self.is_clicked = False
        return False


class TexturedButton(Button):
    def __init__(self, x, y, width, height, texture, texture_down):
        super().__init__(x, y, width, height, texture, None, (255, 255, 255), None, 0)
        self.texture_down = texture_down
