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
pygame.init()


def main():
    pygame.display.set_caption("Game")
    window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    width, height = 1280, 720
    resized = False

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                resized = True

            elif event.type == pygame.ACTIVEEVENT and resized:
                window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                resized = False

        window.fill(BLACK)


main()
