import pygame as pg

black = (0,0,0) # color for background
red = (202,0,42) # color for AI
white = (255,255,255) # color for player

class Board_gui(pg.sprite.Sprite):
    """
    A class used to give a graphic user interface to the board
    Attributes
    ----------
    spriteGrp LayeredUpdates : the groupe of sprite used gather graphical objects
    width int : Width of the board (same as the window)
    height int : Height of the board (same as the window)
    
    Methods
    -------
    displayBoard : Draw the circle on the board according to the values (0 available = black, 1 player = white, 2 AI = red)

    """
    def __init__(self, spriteGrp, width, height):
        self._layer = 1000
        pg.sprite.Sprite.__init__(self, spriteGrp)
        self.image = pg.Surface((width, height))
        self.image.set_colorkey(pg.Color('yellow'))
        wood_texture = pg.image.load('images/wood_texture.jpg')
        self.image.blit(wood_texture, (0,100))
        self.rect = self.image.get_rect()

    def displayBoard(self, board, screen):
        """ Display the board
            Parameters
                board : The board we are playing with
                screen : The screen needed to create circles
        """
        for c in range(board.columns):
            for r in range(board.rows):
                pg.draw.circle(self.image, pg.Color('yellow'), (int(c*100+100/2), int(r*100+100+100/2)), 45)
        
        for c in range(board.columns):
            for r in range(board.rows):
                if board.board[r][c] == 1:
                    pg.draw.circle(screen, white, (int(c*100+100/2), 700-int(r*100+100/2)), 45)
                elif board.board[r][c] == 2: 
                    pg.draw.circle(screen, red, (int(c*100+100/2), 700-int(r*100+100/2)), 45)
        pg.display.update()