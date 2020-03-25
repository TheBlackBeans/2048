#!/usr/bin/python3
# -*- coding: utf-8 -*-
from main import Game
import json, queue

NBTHREADS = 4
MAXSIZE = -1
SCORETARGET = 600000

boundary = queue.LifoQueue(MAXSIZE)

boundary.put(Game())

maxscore = -1
nbgames = 1
bgame = None
while not boundary.empty():
    game = boundary.get()
    game.init_turn()
    moves = game.avail_moves(game.table)
    if not moves:
        if game.score > maxscore:
            print("new maxscore (%s branch): %s" % (nbgames, maxscore))
            maxscore = game.score
            bgame = game
        if maxscore > SCORETARGET:
            break
    nbgames += len(moves) - 1
    for move in moves:
        game2 = game.copy()
        game2.play(move)
        boundary.put(game2)
        
with open("result.out", "w") as f:
    f.write(json.dumps(bgame.save()))
