#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import random, choice
from curses import wrapper, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, A_REVERSE
import sys, pyfiglet

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

class Game:
    def __init__(self, table=None, score=0, size=(4,4), record=None, turn=0):
        if table == None:
            self.table = [[0 for i in range(size[0])] for i in range(size[1])]
        else:
            self.table = table
        self.score = score
        self.size = size
        self.turn = turn
        if record == None:
            self.record = []
        else:
            self.record = record
    def copy(self):
        return Game(table=self.table.copy(), score=self.score, size=self.size, record=self.record.copy(), turn=self.turn)
    def save(self):
        return (self.table, self.score, self.size, self.record, self.turn)
    def init_turn(self):
        self.turn += 1
        self.add_item(self.table)
    def play(self, move):
        self.record.append((self.table, self.score))
        self.table, self.score = self.shift(self.table, move)
    def add_item(self, table):
        free_coords = tuple((x,y) for y in range(self.size[1]) for x in range(self.size[0]) if table[x][y] == 0)
        x, y = choice(free_coords)
        table[x][y] = (1+self.bool_random(.25))
        del free_coords
    def bool_random(self, prob):
        return int(random()<prob)

    def avail_moves(self, table):
        moves = {RIGHT: self.shift(table, RIGHT),
                 LEFT: self.shift(table, LEFT),
                 UP: self.shift(table, UP),
                 DOWN: self.shift(table, DOWN)
        }
        for key in list(moves.keys()):
            if moves[key][0] == table:
                del moves[key]
        return list(moves.keys())
    
    def shift(self, table, direction):
        ntable = [[0 for i in range(self.size[0])] for i in range(self.size[1])]
        dscore = 0
        if direction == RIGHT:
            for i in range(self.size[0]):
                last = 1
                for j in range(1,self.size[1]+1):
                    if table[i][-j] == 0:
                        continue
                    if ntable[i][-last] == 0:
                        ntable[i][-last] = table[i][-j]
                    elif ntable[i][-last] == table[i][-j]:
                        ntable[i][-last] += 1
                        dscore += 2**ntable[i][-last]
                        last += 1
                    elif ntable[i][-last] != table[i][-j]:
                        last += 1
                        ntable[i][-last] = table[i][-j]
        elif direction == LEFT:
            for i in range(self.size[0]):
                last = 0
                for j in range(self.size[1]):
                    if table[i][j] == 0:
                        continue
                    if ntable[i][last] == 0:
                        ntable[i][last] = table[i][j]
                    elif ntable[i][last] == table[i][j]:
                        ntable[i][last] += 1
                        dscore += 2**ntable[i][last]
                        last += 1
                    elif ntable[i][last] != table[i][j]:
                        last += 1
                        ntable[i][last] = table[i][j]
        elif direction == UP:
            for i in range(self.size[0]):
                last = 0
                for j in range(self.size[1]):
                    if table[j][i] == 0:
                        continue
                    if ntable[last][i] == 0:
                        ntable[last][i] = table[j][i]
                    elif ntable[last][i] == table[j][i]:
                        ntable[last][i] += 1
                        dscore += 2**ntable[last][i]
                        last += 1
                    elif ntable[last][i] != table[j][i]:
                        last += 1
                        ntable[last][i] = table[j][i]
        elif direction == DOWN:
            for i in range(self.size[0]):
                last = 1
                for j in range(1,self.size[1]+1):
                    if table[-j][i] == 0:
                        continue
                    if ntable[-last][i] == 0:
                        ntable[-last][i] = table[-j][i]
                    elif ntable[-last][i] == table[-j][i]:
                        ntable[-last][i] += 1
                        dscore += 2**ntable[-last][i]
                        last += 1
                    elif ntable[-last][i] != table[-j][i]:
                        last += 1
                        ntable[-last][i] = table[-j][i]
        return ntable, self.score+dscore
    
def render_item(item):
    if item == 0:
        return "     "
    else:
        r = str(2**item)
        return " "*(5-len(r))+r
def render_info(game, screen):
    screen.addstr(0, 0, "Score: %8s\tTurn: %6s" % (game.score, game.turn), A_REVERSE)
    screen.addstr(1, 0, pyfiglet.figlet_format("2048"), A_REVERSE)
    render_table(game, screen)
    screen.addstr(screen.getmaxyx()[0]-1, 0, "[q] - Quit ; [arrows] - Move ; [space] - Next")
    
def render_table(game, screen):
    y, x = screen.getmaxyx()
    offset = y - 2*game.size[0]-2
    for i in range(game.size[0]):
        screen.addstr(offset+2*i, 0, "+" + "+".join("-----" for j in range(game.size[1])) + "+", A_REVERSE)
        screen.addstr(2*i+offset+1, 0, "|"+"|".join(render_item(game.table[i][j]) for j in range(game.size[1])) + "|", A_REVERSE)
    screen.addstr(offset+2*game.size[0], 0, "+" + "+".join("-----" for j in range(game.size[1])) + "+", A_REVERSE)

def prompt_move(screen, moves):
    rkeys = set()
    if DOWN in moves:
        rkeys.add(KEY_DOWN)
    if UP in moves:
        rkeys.add(KEY_UP)
    if LEFT in moves:
        rkeys.add(KEY_LEFT)
    if RIGHT in moves:
        rkeys.add(KEY_RIGHT)
    while True:
        char = screen.getch()
        if char == ord("q"):
            sys.exit(0)
        if char in rkeys:
            return {KEY_DOWN: DOWN, KEY_UP: UP, KEY_RIGHT: RIGHT, KEY_LEFT: LEFT}[char]
    

def main(stdscr):
    stdscr.clear()
    game = Game()
    while True:
        game.init_turn()
        stdscr.bkgd(" ", A_REVERSE)
        render_info(game, stdscr)
        moves = game.avail_moves(game.table)
        if not moves:
            stdscr.addstr(8, 0, pyfiglet.figlet_format("You lose!"), A_REVERSE)
            while stdscr.getch() != ord("q"): pass
            break
        move = prompt_move(stdscr, moves)
        game.play(move)
        stdscr.refresh()
if  __name__ == "__main__":
    wrapper(main)
