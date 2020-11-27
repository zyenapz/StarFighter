# Draw functions

import pygame

def draw_background(surf, img, img_rect, ypos):
    surf_h = surf.get_height()
    rel_y = ypos % img_rect.height
    surf.blit(img, (0, rel_y - img_rect.height))

    if rel_y < surf_h:
        surf.blit(img, (0, rel_y))

def draw_text(surf, text, size, font, x, y, color):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.bottom = y
    surf.blit(text_surface, (text_rect.x, text_rect.y))

def draw_hp(surf, x, y, hp, color, height):
    if hp < 0:
        hp = 0
    rect_height = height
    rectangle = pygame.Rect(x, y-rect_height,  hp * (surf.get_width() // 10), rect_height)
    pygame.draw.rect(surf, color, rectangle)

def shake(intensity, n):
    # Credits to sloth from StackOverflow, thanks buddy!
    shake = -1
    for _ in range(n):
        for x in range(0, intensity, 5):
            yield (x*shake, 0)
        for x in range(intensity, 0, 5):
            yield (x*shake, 0)
        shake *= -1
    while True:
        yield (0, 0)
