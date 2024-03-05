#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# NimGame
# Copyright (C) 2024 Shubham Tiwari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Shubham Tiwari    shubhamtiwari71488@gmail.com

import pygame as pg
import gi
import sys
import random
import const as c

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NimGame:

    def __init__(self, journal=True):
        self.journal = journal
        self.checkbox_state = [[False] * c.NUM_COLS for _ in range(c.NUM_ROWS)]
        self.winner_player = None
        self.need_help = False

        self.clock = pg.time.Clock()  # Set up clock for managing FPS.
        self.randomly_fill_checkboxes()  # First time fill all box randomly

    def set_canvas(self, canvas):
        self.canvas = canvas
        pg.display.set_caption("Nim Game")

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    def quit(self):
        self.running = False

    # Declare the winner
    def winner(self, who):
        self.winner_player = who
        font = pg.font.Font(None, 36)
        win_text = "You won!"
        if who is None:
            return
        elif who == 0:
            win_text = "Computer won! Better Luck next time :("

        win_surf = font.render(win_text, True, c.WHITE)
        rec_surf = win_surf.get_rect(center=(c.WIDTH - c.WIDTH // 2,
                                             c.HEIGHT - c.HEIGHT // 2 + 100))
        c.WIN.blit(win_surf, rec_surf)

    def draw_checkboxes(self):
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                val1 = c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN
                rect = pg.Rect(
                    (c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * val1,
                    (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * val1,
                    c.CHECKBOX_SIZE, c.CHECKBOX_SIZE
                )
                pg.draw.rect(c.WIN, c.BLACK, rect, 2)
                # Fill checkbox with color if it's checked
                if self.checkbox_state[i][j]:
                    pg.draw.rect(c.WIN, "green", rect)

    def randomly_fill_checkboxes(self):
        # Reset all checkbox states to False
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                self.checkbox_state[i][j] = False

        # Randomly fill checkboxes
        for i in range(c.NUM_ROWS):
            # Total checkboxes to be filled in current row
            num_to_fill = random.randint(1, c.NUM_COLS)
            start_col = 0
            for j in range(start_col, start_col + num_to_fill):
                self.checkbox_state[i][j] = True

    # Deleting a range of columns selected by computer
    def delete_column(self, row):
        end = c.NUM_COLS - 1
        if not self.checkbox_state[row][c.NUM_COLS - 1]:
            end = (self.checkbox_state[row]).index(False)

        no_column_remove = random.randint(1, end)
        for i in range(no_column_remove + 1):
            self.checkbox_state[row][end - i] = False

        if not any(self.checkbox_state[i][0] for i in range(c.NUM_ROWS)):
            self.winner(0)

    # This is the easy mode
    def computer_move(self):
        if not any(self.checkbox_state[i][0] for i in range(c.NUM_ROWS)):
            self.winner(1)

        # Computer chooses a row to click on
        elif self.checkbox_state[0][0] is True:
            self.delete_column(0)
        elif self.checkbox_state[1][0] is True:
            self.delete_column(1)
        elif self.checkbox_state[2][0] is True:
            self.delete_column(2)

    # Making a Reset game button and help menu
    def draw(self):
        if self.need_help is True:
            c.HELP_SYMBOL = "X"
            y = c.MARGIN
            c.LINE_SPACING = c.HEIGHT // 27
            font = pg.font.Font(None, c.WIDTH // 39)
            for line in c.GAME_RULE:
                text_surface = font.render(line, True, c.WHITE)
                text_rect = text_surface.get_rect(topleft=(c.MARGIN, y))
                c.WIN.blit(text_surface, text_rect)
                y += c.LINE_SPACING

        BUTTON_FONT = pg.font.SysFont(None, c.BUTTON_FONT_SIZE)
        self.button_rect = pg.Rect(
            (c.WIDTH - c.BUTTON_WIDTH) // 2,
            c.HEIGHT - c.BUTTON_HEIGHT * 3,
            c.BUTTON_WIDTH,
            c.BUTTON_HEIGHT
        )
        pg.draw.rect(c.WIN, c.WHITE, self.button_rect, 0, border_radius=20)
        button_text = BUTTON_FONT.render(c.BUTTON_TEXT, True, c.GUNMETAL)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        c.WIN.blit(button_text, text_rect)

        HELP_FONT = pg.font.SysFont(None, 80)
        self.help_cicle = pg.draw.circle(
            c.WIN, c.WHITE,
            [c.WIDTH - 100, c.HEIGHT - (c.HEIGHT) + 100],
            40, 40)
        help_text = HELP_FONT.render(c.HELP_SYMBOL, True, c.GUNMETAL)
        help_rect = help_text.get_rect(center=self.help_cicle.center)
        c.WIN.blit(help_text, help_rect)

    # Handling events of mouse clicks on boxes
    def player_move(self, x, y):
        for i in range(c.NUM_ROWS):
            for j in range(c.NUM_COLS):
                val1 = c.CHECKBOX_SIZE + c.CHECKBOX_MARGIN
                rect = pg.Rect(
                    (c.WIDTH - c.CHECKBOX_WIDTH) // 2 + j * val1,
                    (c.HEIGHT - c.CHECKBOX_HEIGHT) // 2 + i * val1,
                    c.CHECKBOX_SIZE, c.CHECKBOX_SIZE)
                if rect.collidepoint(x, y):
                    if not self.checkbox_state[i][j]:
                        break
                    self.checkbox_state[i][j] = not self.checkbox_state[i][j]
                    if not self.checkbox_state[i][j]:
                        for k in range(j, c.NUM_COLS):
                            self.checkbox_state[i][k] = False
                    self.computer_move()
                    break

    # The main game loop.
    def run(self):
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                c.WIDTH, c.HEIGHT = event.size
                break
        self.running = True
        c.init()
        pg.font.init()
        while self.running:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    pg.display.set_mode(
                        (c.WIDTH, c.HEIGHT), pg.RESIZABLE)
                    break
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pg.mouse.get_pos()
                    if self.button_rect.collidepoint(x, y):  # Reset button
                        self.randomly_fill_checkboxes()
                        self.winner_player = None
                        break
                    elif self.help_cicle.collidepoint(x, y):
                        self.need_help = not self.need_help
                        c.HELP_SYMBOL = "?"
                        self.draw()

                    self.player_move(x, y)

            c.WIN.fill(pg.Color(c.GUNMETAL))
            self.draw_checkboxes()
            self.draw()
            self.winner(self.winner_player)
            pg.display.flip()
            self.clock.tick(30)
        pg.display.quit()
        pg.quit()
        sys.exit(0)


def main():
    pg.init()
    pg.display.set_mode((c.WIDTH, c.HEIGHT))
    game = NimGame(journal=False)
    game.run()


if __name__ == '__main__':
    main()
