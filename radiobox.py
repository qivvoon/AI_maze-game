import pygame

pygame.font.init()

# Radiobox
# 다른 사람이 구현해 공유해놓은 코드 이용 (stackoverflow 참조)
# 해당 코드의 불필요한 함수 삭제 및 _update() 변경 
# https://stackoverflow.com/questions/38551168/radio-button-in-pygame
class Radiobox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=22, font_color=(0, 0, 0), 
    text_offset=(28, 1), font=None):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        self.idnum = idnum

        # radiobox object
        self.radiobox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.radiobox_outline = self.radiobox_obj.copy()

        # radioibox가 선택되었다면 True, 선택되지 않았다면 False
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 + 
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_radiobox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.radiobox_obj)
            pygame.draw.rect(self.surface, self.oc, self.radiobox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.radiobox_obj)
            pygame.draw.rect(self.surface, self.oc, self.radiobox_outline, 1)
        self._draw_button_text()

    def _update(self, radioboxes):
            if self.checked:
                self.checked = False
            else:
                self.checked = True
                for box in radioboxes:
                    if box != self:
                        box.checked = False
