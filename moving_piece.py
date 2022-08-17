import pygame as pg

rows = 6 # number of rows in connect4
columns = 7 # number of columns in connect4
slot = 100 # Size of slot containg a piece into the board

class Moving_piece(pg.sprite.Sprite):
    """
    A class used to represent moving piece being played.
    Attributes
    ----------
    spriteGrp LayeredUpdates : the groupe of sprite used gather graphical objects
    column int : Number of column used in board
    rows int : Number of rows used
    color (r,g,b) : The player color for the moving piece
    
    Methods
    -------
    update : Method used to move the piece using its vector until it reaches the correct row

    """
    def __init__(self, spriteGrp, column, row, color):
        """ Create the transparent surface, gives it a layer 0 so it moves behind all layers, and draw a circle on it
            It also asign the vector responsible for movement
        """
        IMAGE = pg.Surface((100, 100), pg.SRCALPHA)
        #low layer so it moves behind the wood board
        self._layer = 0
        pg.sprite.Sprite.__init__(self, spriteGrp)
        self.image = IMAGE
        pg.draw.circle(IMAGE, color, (50,50),45)
        self.posx = column * slot + slot/2
        self.posyDep = slot/2
        self.posyDest = (rows - row) * slot
        self.rect = self.image.get_rect(center=(self.posx, self.posyDep))
        self.vec = pg.math.Vector2()
        # direction of the piece, 10px move and 90° which means it goes toward bottom
        self.vec.from_polar((10, 90))

    def update(self):
        """ Update the moving piece by applying its vector again until destination reached
        """
        self.rect.move_ip(*self.vec)
        if self.rect.y <= self.posyDest:
            self.vec.from_polar((10, 90))