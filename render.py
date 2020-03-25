#!/usr/bin/python3
# -*- coding: utf-8 -*-

from curses import *
import pyfiglet, json, sys, time
from main import Game

ITEMSIZE = 5

def render_item(item):
    if item == 0:
        return " "*ITEMSIZE
    else:
        r = str(2**item)[:ITEMSIZE]
        return " "*(ITEMSIZE-len(r))+r

def render_score(game, screen):
    screen.addstr(0, 0, "Score: %8s\tTurn: %6s" % (game.score, game.turn), A_REVERSE)

def render_2048(screen):
    screen.addstr(1, 0, pyfiglet.figlet_format("2048"), A_REVERSE)

def render_table(game, screen):
    y, x = screen.getmaxyx()
    offset = y - 2*game.size[0] - 2
    for i in range(game.size[0]):
        screen.addstr(offset+2*i, 0, "+" + "+".join("-"*ITEMSIZE for j in range(game.size[1])) + "+", A_REVERSE)
        screen.addstr(2*i+offset+1, 0, "|" + "|".join(render_item(game.table[i][j]) for j in range(game.size[1])) + "|", A_REVERSE)
    screen.addstr(offset+2*game.size[0], 0, "+" + "+".join("-"*ITEMSIZE for j in range(game.size[1])) + "+", A_REVERSE)

def render_help(screen):
    screen.addstr(screen.getmaxyx()[0]-1, 0, "[q] - Quit ; [arrow] - Move ; [space] - Next")
    
def render_info(game, screen):
    screen.bkgd(" ", A_REVERSE)
    render_score(game, screen)
    render_2048(screen)
    render_table(game, screen)

def prompt_turn(game, screen):
    y, x = screen.getmaxyx()
    screen.erase()
    render_info(game, screen)
    echo()
    nocbreak()
    res = screen.getstr(y-1, 0)
    while not res.isdigit():
        screen.erase()
        render_info(game, screen)
        res = screen.getstr(y-1, 0)
    noecho()
    cbreak()
    return res
    
def prompt_key(game, screen):
    while True:
        c = screen.getch()
        if c == ord("q"): sys.exit(0)
        if c == ord("/"):
            return ("skip", prompt_turn(game, screen))
        if c == ord(":"):
            return ("add", prompt_turn(game, screen))
        elif c in {KEY_RIGHT, ord(" "), ord("n")}: return ("next", None)
        elif c in {KEY_LEFT, ord("p")}: return ("prev", None)
    
def play_game(screen, game, turn=0):
    maxturn = len(game.record)-1
    turn = min(max(turn, 0), maxturn) 
    while True:
        table, score = game.record[turn]
        g = Game(table=table, score=score, size=game.size, turn=turn+1)
        render_info(g, screen)
        render_help(screen)
        action, arg = prompt_key(g, screen)
        if action == "next":
            turn += 1
        elif action == "prev":
            turn -= 1
        elif action == "skip":
            turn = int(arg)-1
            
        elif action == "add":
            turn += int(arg)
        turn = min(max(turn, 0), maxturn)
            
            
def main(stdscr):
    with open("result.out") as f:
        game = Game(*json.loads(f.read()))
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        turn = int(sys.argv[2])-1
    else:
        turn = 0
        
    play_game(stdscr, game, turn=turn)

if __name__ == "__main__":
    wrapper(main)
