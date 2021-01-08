#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
from _constants import *


class Button:
    def __init__(self, loc, size, text):
        self.loc = loc
        self.size = size
        self.text = text
        self.text_loc = (loc[0] + (size[0]-text.get_width())//2, loc[1] + (size[1]-text.get_height())//2)

    def draw(self, window, events):
        color = (GRAY_DARK if self.clicked(events) else GRAY_LIGHT) if self.hovered() else WHITE
        pygame.draw.rect(window, color, self.loc+self.size)
        pygame.draw.rect(window, WHITE, self.loc+self.size, 2)
        window.blit(self.text, self.text_loc)

    def hovered(self):
        loc = self.loc
        size = self.size
        mouse_pos = pygame.mouse.get_pos()
        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered():
                return True
        return False


class Slider:
    def __init__(self, loc, size, circle_size, font, label, default_val, val_range):
        self.loc = loc
        self.size = size
        self.circle_size = circle_size
        self.font = font
        self.label = label
        self.value = default_val
        self.range = val_range
        self.val_dist = val_range[1] - val_range[0]
        self.dragging = False

    def draw(self, window, events):
        loc = self.loc
        size = self.size

        text = self.font.render(f"{self.label}: {self.value}", 1, WHITE)
        text_loc = (loc[0] + (self.size[0]-text.get_width())//2, self.loc[1]+self.size[1]+7)
        pygame.draw.rect(window, GRAY, loc+size)
        pygame.draw.rect(window, WHITE, loc+size, 1)
        pygame.draw.circle(window, WHITE, (self.value_to_loc(), self.loc[1]+self.size[1]//2), self.circle_size)
        window.blit(text, text_loc)

        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
                    self.dragging = True

        clicked = pygame.mouse.get_pressed()[0]
        if not clicked:
            self.dragging = False
        
        if clicked and self.dragging:
            self.value = self.loc_to_value(mouse_pos[0])

    def loc_to_value(self, loc):
        fac = max(min((loc-self.loc[0]) / self.size[0], 1), 0)
        return int(fac*self.val_dist + self.range[0])

    def value_to_loc(self):
        fac = (self.value-self.range[0]) / self.val_dist
        return fac * self.size[0] + self.loc[0]
