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


class Text:
    def __init__(self, text):
        self.text = text

    def draw(self, window, loc):
        text_loc = [loc[i] - self.text.get_size()[i]//2 for i in range(2)]
        window.blit(self.text, text_loc)


class Button:
    def __init__(self, text):
        self.text = text

    def draw(self, window, events, loc, size):
        loc = list(loc)
        loc[0] -= size[0]//2

        clicked = self.clicked(events, loc, size)
        color = (GRAY_DARK if clicked else GRAY_LIGHT) if self.hovered(loc, size) else WHITE
        text_loc = [loc[i] + (size[i]-self.text.get_size()[i])//2 for i in range(2)]

        pygame.draw.rect(window, color, (*loc, *size))
        pygame.draw.rect(window, BLACK, (*loc, *size), 2)
        window.blit(self.text, text_loc)

        return clicked

    def hovered(self, loc, size):
        mouse = pygame.mouse.get_pos()
        if loc[0] <= mouse[0] <= loc[0]+size[0] and loc[1] <= mouse[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events, loc, size):
        if self.hovered(loc, size):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False


class TextInput:
    """Also written by Arjun Sahlot <https://github.com/ArjunSahlot"""

    def __init__(self, font, label="", password=False, on_enter=None):
        self.font = font
        self.label = label
        self.password = password
        self.on_enter = on_enter

        self.cursor_pos = 0
        self.text = ""
        self.editing = False
        self.frame = 0

        self.key_rpt_count = {}
        self.key_rpt_init = 400
        self.key_rpt_int = 35
        self.clock = pygame.time.Clock()

    def draw(self, window, events, loc, size):
        self.frame += 1
        loc = list(loc)
        loc[0] -= size[0]//2

        clicked = self.clicked(events, loc, size)
        str_text = self.label if not self.editing and self.text == "" else self.text
        if self.password and not self.text == "":
            str_text = "*" * len(str_text)
        text = self.font.render(str_text, 1, BLACK)
        text_loc = [loc[i] + (size[i]-text.get_size()[i])//2 for i in range(2)]

        color = GRAY_DARK if clicked else (GRAY_LIGHT if self.hovered(loc, size) and not self.editing else WHITE)
        pygame.draw.rect(window, color, (*loc, *size))
        pygame.draw.rect(window, BLACK, (*loc, *size), 2)
        window.blit(text, text_loc)
        if self.editing and (self.frame//30) % 2 == 0:
            cursor_x = text_loc[0] + self.font.render(str_text[:self.cursor_pos], 1, BLACK).get_width()
            pygame.draw.line(window, BLACK, (cursor_x, loc[1]+12), (cursor_x, loc[1]+size[1]-12))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.editing = self.hovered(loc, size)
            elif event.type == pygame.KEYDOWN and self.editing:
                if event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                    self.editing = False
                elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    self.editing = False
                    if self.on_enter is not None:
                        self.editing = True
                        self.on_enter()
                        self.text = ""

                else:
                    if event.key not in self.key_rpt_count:
                        self.key_rpt_count[event.key] = [0, event.unicode]

                    if event.key == pygame.K_LEFT:
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_pos += 1
                    elif event.key in (pygame.K_HOME, pygame.K_PAGEDOWN):
                        self.cursor_pos = 0
                    elif event.key in (pygame.K_END, pygame.K_PAGEUP):
                        self.cursor_pos = len(self.text)

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_DELETE:
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    else:
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1

                self.cursor_pos = min(max(self.cursor_pos, 0), len(self.text))

            elif event.type == pygame.KEYUP:
                if event.key in self.key_rpt_count:
                    del self.key_rpt_count[event.key]

        for key in self.key_rpt_count:
            self.key_rpt_count[key][0] += self.clock.get_time()

            if self.key_rpt_count[key][0] >= self.key_rpt_init:
                self.key_rpt_count[key][0] = self.key_rpt_init - self.key_rpt_int
                event_key, event_unicode = key, self.key_rpt_count[key][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        self.clock.tick()

    def hovered(self, loc, size):
        mouse = pygame.mouse.get_pos()
        if loc[0] <= mouse[0] <= loc[0]+size[0] and loc[1] <= mouse[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events, loc, size):
        if self.hovered(loc, size):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False
