import pygame

pygame.font.init()
fonts = {"fira": [
            pygame.font.SysFont('firacodenerdfont', 20),
            pygame.font.SysFont('firacodenerdfont', 30),
            pygame.font.SysFont('firacodenerdfont', 40)
        ],
        "notosans": [
            pygame.font.SysFont('notosans', 20),
            pygame.font.SysFont('notosans', 30),
            pygame.font.SysFont('notosans', 40)
        ],

}
class Button:
    # alignment -> (x, y)
    # alignment 1 will center the button, 2 -> right align, 0 -> left align
    def __init__(self, pos:list[int], size, alignment, text, colors, next_state, on_click=None):
        self.text_surface = fonts["fira"][size].render(text, False, colors[0], colors[1])
        
        self.pos = pos

        self.pos[0] -= (self.text_surface.get_width() * alignment[0]) //2
        self.pos[1] -= (self.text_surface.get_height() * alignment[1]) //2

        self.rect = pygame.Rect(*pos, *self.text_surface.get_size())

        self.on_click = on_click

        self.next_state = next_state
        
    def handle_input(self, mouse_pos, mouse_state):
        if self.rect.collidepoint(mouse_pos) and mouse_state == (1, 0, 0):

            if self.on_click: self.on_click()

            return (True, self.next_state)

        return (False, None)

    def draw(self, surface):
        surface.blit(self.text_surface, self.pos)



class ButtonList:
    def __init__(self) -> None:
        self.buttons = []

    def handle_input(self, mouse_pos, mouse_state):
        for button in self.buttons:
            change_state, new_state = button.handle_input(mouse_pos, mouse_state)

            if change_state:
                return change_state, new_state

        return (False, None)

    def draw(self, surface):
        for button in self.buttons: button.draw(surface)
