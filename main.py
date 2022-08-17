from board import Board
from board_gui import Board_gui
from moving_piece import Moving_piece
import pygame as pg
import sys
import math

black = (0,0,0) # color for background
red = (202,0,42) # color for AI
white = (255,255,255) # color for player
rows = 6 # number of rows in connect4
columns = 7 # number of columns in connect4
slot = 100 # Size of slot containg a piece into the board
width = columns * slot # Width of the board, which determite the one of the window
height = (rows+1) * slot # Height of the board, which determite the one of the window
size = (width, height) # The size of the global window
radius = int(slot/2 - 5) # Needed for the pg module to create circles

def update(m, screen, allSprites, clock):
    """ Update the moving piece, draw a black screen so there is no residual image of it, and displays it
        Parameters
            screen : The screen needed to create circles
            allSprites : The group sprite containing the objects
            the clock for the ticks needed for the movement being readable
    """
    m.update()
    screen.fill(pg.Color('black'))
    allSprites.draw(screen)
    pg.display.flip()
    clock.tick(120)

def main():
    color = 1 # Initializing color to one si the player can always begin. The IA is pretty good so it is a little needed advantage
    keepPlaying = True # variable to iterate during the game. When False, game is over

    allSprites = pg.sprite.LayeredUpdates()
    board = Board(columns, rows)
    pg.init()
    screen = pg.display.set_mode(size)
    boardGui = Board_gui(allSprites, width, height)
    clock = pg.time.Clock() 
    boardGui.displayBoard(board, screen)
    allSprites.draw(screen)
    myfont = pg.font.SysFont("calibri", 75, bold=True, italic=True)
    while keepPlaying:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEMOTION:
                # As the mouse move with a cercle on it (The piece we want to play), we have to draw a rectangle behind. If not, we have residual image of the circle
                pg.draw.rect(screen, black, (0,0, width, slot))
                posx = event.pos[0] # Position of the mouse to draw the circle on
                if color == 1:
                    pg.draw.circle(screen, white, (posx, int(slot/2)), radius)
                else: 
                    pg.draw.circle(screen, red, (posx, int(slot/2)), radius)
            pg.display.update()

            if event.type == pg.MOUSEBUTTONDOWN:
                # Ask for Player 1 Input
                if color == 1:
                    posx = event.pos[0]
                    # We divide the position of the mouse by the size of the slot to get a round number between 0 and 6 (The column to put the piece into)
                    column = int(math.floor(posx/slot))
                    nextMove = board.getNextValidPosition(column)
                    if nextMove != None:
                        m = Moving_piece(allSprites, column, nextMove, white)
                        while m.rect.y < m.posyDest:
                            #Making the piece move from top to bottom
                            update(m, screen, allSprites, clock)
                        board.playPiece(nextMove, column, 1)
                        keepPlaying = board.verifKeepPlaying(color)
                        if not keepPlaying:
                            winner = myfont.render("White wins !", 1, white)
                            screen.blit(winner, (150,10))
                        color = 2 if color == 1 else 1
                boardGui.displayBoard(board, screen)
        # Turn of the AI
        if color == 2:
            #Little pause so the AI doesnt play to fast, which is annoying
            column, score = board.minimax(4, 2)
            nextMove = board.getNextValidPosition(column)
            if nextMove != None:
                m = Moving_piece(allSprites, column, nextMove, red)
                while m.rect.y < m.posyDest:
                    update(m, screen, allSprites, clock)
                board.playPiece(nextMove, column, 2)
                keepPlaying = board.verifKeepPlaying(color) 
                if not keepPlaying:
                    label = myfont.render("Red wins!", 1, red)
                    screen.blit(label, (200,10))
            color = 2 if color == 1 else 1
            boardGui.displayBoard(board, screen)

        if keepPlaying == False:
            #Pause at the end to appreciate the win, or the defeat !
            pg.time.wait(3000)
            # Reinitiate the board to continue playing
            screen.fill(pg.Color('black'))
            board = Board(columns, rows)
            allSprites = pg.sprite.LayeredUpdates()
            boardGui = Board_gui(allSprites, width, height)
            keepPlaying = True
            boardGui.displayBoard(board, screen)
            allSprites.draw(screen)
if __name__ == "__main__":
    main()
