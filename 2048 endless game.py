# -*- coding: utf-8 -*-
"""
Created on Tue May 20 22:32:05 2025

@author: pravi
"""
import numpy as np
import random
def init_board():
    board = np.zeros((4,4), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board
def add_new_tile(board):
    empty = list(zip(*np.where(board == 0)))
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4
def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0]*(4 - len(new_row))
    return new_row
def merge(row):
    for i in range(3):
        if row[i] == row[i+1] and row[i] != 0:
            row[i] *= 2
            row[i+1] = 0
    return row
def move_left(board):
    new_board = np.zeros_like(board)
    for i in range(4):
        row = compress(board[i])
        row = merge(row)
        row = compress(row)
        new_board[i] = row
    return new_board
def move_right(board):
    board = np.fliplr(board)
    board = move_left(board)
    return np.fliplr(board)
def move_up(board):
    board = board.T
    board = move_left(board)
    return board.T
def move_down(board):
    board = board.T
    board = move_right(board)
    return board.T
def game_over(board):
    if np.any(board == 0):
        return False
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] or board[j][i] == board[j+1][i]:
                return False
    return True
def print_board(board):
    print("\n2048 Board:")
    print(board)
def play_2048():
    board = init_board()
    print_board(board)
    while True:
        move = input("Move (w=up, s=down, a=left, d=right, q=quit): ").strip().lower()
        if move == 'q':
            print("Game quit.")
            break
        if move not in ('w','a','s','d'):
            print("Invalid move. Use w, a, s, d or q.")
            continue
        if move == 'w':
            new_board = move_up(board)
        elif move == 's':
            new_board = move_down(board)
        elif move == 'a':
            new_board = move_left(board)
        else:
            new_board = move_right(board)
        if np.array_equal(board, new_board):
            print("Move not possible. Try a different direction.")
            continue
        board = new_board
        add_new_tile(board)
        print_board(board)
        if game_over(board):
            print("Game Over! No more moves possible.")
            break
play_2048()