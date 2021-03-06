#Chess ChessBot-TakeTwo.py
import pygame
import random
import copy
import time
import math
from typing import Union, Type

#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
pygame.mixer.init()

#IMAGES
imagePath = 'V:\Code\ChessProject\IMG' 
PawnW = pygame.transform.scale(pygame.image.load(imagePath + '\Pawn-white.png'), (100,100))
KnightW = pygame.transform.scale(pygame.image.load(imagePath + '\Knight-white.png'), (100,100))
BishopW = pygame.transform.scale(pygame.image.load(imagePath + '\Bishop-white.png'), (100,100))
RookW = pygame.transform.scale(pygame.image.load(imagePath + '\Rook-white.png'), (100,100))
QueenW = pygame.transform.scale(pygame.image.load(imagePath + '\Queen-white.png'), (100,100))
KingW = pygame.transform.scale(pygame.image.load(imagePath + '\King-white.png'), (100,100))

PawnB = pygame.transform.scale(pygame.image.load(imagePath + '\Pawn-black.png'), (100,100))
KnightB = pygame.transform.scale(pygame.image.load(imagePath + '\Knight-black.png'), (100,100))
BishopB = pygame.transform.scale(pygame.image.load(imagePath + '\Bishop-black.png'), (100,100))
RookB = pygame.transform.scale(pygame.image.load(imagePath + '\Rook-black.png'), (100,100))
QueenB = pygame.transform.scale(pygame.image.load(imagePath + '\Queen-black.png'), (100,100))
KingB = pygame.transform.scale(pygame.image.load(imagePath + '\King-black.png'), (100,100))

#SOUNDS
soundPath = 'V:\Code\ChessProject\Sound'
captureSound =  pygame.mixer.Sound(soundPath + '\Capture.wav')
moveSound = pygame.mixer.Sound(soundPath + '\Move.wav')

captureSound.set_volume(0)
moveSound.set_volume(0)

#------------PIECE CLASSES------------
class Piece:
    def __init__(self, pos: list, color: pygame.Color):
        self.pos = pos
        self.color = color

class Pawn(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.val = 100

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(PawnW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(PawnB, (self.pos[0] * 100, self.pos[1] * 100))

    def genMoves(self) -> list:
        output = []
        if self.color == 0:
            output.append((self.pos[0], self.pos[1]-1))
            if self.pos[1] == 6:
                output.append((self.pos[0], self.pos[1]-2))
            output.append((self.pos[0]+1, self.pos[1]-1))
            output.append((self.pos[0]-1, self.pos[1]-1))
        else:
            output.append((self.pos[0], self.pos[1]+1))
            if self.pos[1] == 1:
                output.append((self.pos[0], self.pos[1]+2))
            output.append((self.pos[0]+1, self.pos[1]+1))
            output.append((self.pos[0]-1, self.pos[1]+1))
        return output

class Bishop(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.val = 300

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(BishopW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(BishopB, (self.pos[0] * 100, self.pos[1] * 100))

    def genMoves(self) -> list:
        output = []
        xacc = self.pos[0]
        yacc1 = self.pos[1]
        yacc2 = self.pos[1]
        while xacc <= 7:
            if yacc1 <= 7:
                output.append((xacc, yacc1))
                yacc1+=1
            if yacc2 >= 0:
                output.append((xacc,yacc2))
                yacc2-=1
            xacc+=1
        xacc = self.pos[0]
        yacc1 = self.pos[1]
        yacc2 = self.pos[1]
        while xacc >= 0:
            if yacc1 <= 7:
                output.append((xacc, yacc1))
                yacc1+=1
            if yacc2 >= 0:
                output.append((xacc,yacc2))
                yacc2-=1
            xacc-=1
        output.remove(self.pos)
        output.remove(self.pos)
        output.remove(self.pos)
        output.remove(self.pos)
        return output

class Knight(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.val = 300

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(KnightW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(KnightB, (self.pos[0] * 100, self.pos[1] * 100))

    def genMoves(self) -> list:
        output = []
        output.append((self.pos[0]-1, self.pos[1]+2))
        output.append((self.pos[0]+1, self.pos[1]+2))
        output.append((self.pos[0]+2, self.pos[1]+1))
        output.append((self.pos[0]+2, self.pos[1]-1))
        output.append((self.pos[0]+1, self.pos[1]-2))
        output.append((self.pos[0]-1, self.pos[1]-2))
        output.append((self.pos[0]-2, self.pos[1]-1))
        output.append((self.pos[0]-2, self.pos[1]+1))
        return output

class Rook(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.val = 500

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(RookW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(RookB, (self.pos[0] * 100, self.pos[1] * 100))

    def genMoves(self) -> list:
        output = []
        for i in range(8):
            output.append((self.pos[0], i))
            output.append((i, self.pos[1]))
        output.remove(self.pos)
        output.remove(self.pos)
        return output

class Queen(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.val = 900

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(QueenW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(QueenB, (self.pos[0] * 100, self.pos[1] * 100))

    def genMoves(self) -> list:
        diagMoves = Bishop(self.pos, self.color).genMoves()
        straightMoves = Rook(self.pos, self.color).genMoves()
        output = diagMoves + straightMoves
        return output

class King(Piece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.kingSide = True
        self.queenSide = True
        self.val = 100000 #arbitarily large number(could be positive infinity?)

    def draw(self, win: pygame.Surface) -> pygame.Surface:
        if self.color == 0:
            win.blit(KingW, (self.pos[0] * 100, self.pos[1] * 100))
        else:
            win.blit(KingB, (self.pos[0] * 100, self.pos[1] * 100))

    def valid(self, posLast: list) -> bool:
        output = True
        diffx = self.pos[0] - posLast[0]
        diffy = self.pos[1] - posLast[1]

        return ((-1 <= diffy <= 0) or (0 <= diffy <= 1)) and ((0 >= diffx >= -2) or (2 >= diffx >= 0))

    def genMoves(self) -> list:
        output = []
        output.append((self.pos[0], self.pos[1]+1))
        output.append((self.pos[0]+1, self.pos[1]+1))
        output.append((self.pos[0]+1, self.pos[1]))
        output.append((self.pos[0]+1, self.pos[1]-1))
        output.append((self.pos[0], self.pos[1]-1))
        output.append((self.pos[0]-1, self.pos[1]-1))
        output.append((self.pos[0]-1, self.pos[1]))
        output.append((self.pos[0]-1, self.pos[1]+1))
        output.append((self.pos[0]+2, self.pos[1]))
        output.append((self.pos[0]-2, self.pos[1]))
        return output

class emptyPiece():
    def __init__(self):
        self.pos = (-1,-1)
        self.color = -1
        self.val = 0

    def draw(self,win: pygame.Surface) -> pygame.Surface:
        return win

    def genMoves(self) -> list:
        return []

#---------- GAME/BOARD CLASSES -----------
#Bresenham's line algorithm
def line(x0: int, y0: int, x1: int, y1: int) -> list:
    points_in_line = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            points_in_line.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            points_in_line.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points_in_line.append((x, y))
    return points_in_line

class Move:
    def __init__(self, pieceIndex: int, posLast: list, posNew: list):
        self.pieceIndex = pieceIndex
        self.posLast = posLast
        self.posNew = posNew

    def moveBack(self, board: list):
        board.pieces[self.pieceIndex].pos = self.posLast

#BOARD CLASS
class Board:
    scale = 100
    brown = pygame.Color('0xDCD3EA')
    beige = pygame.Color('0xF5F5F5')

    def __init__(self, win: pygame.Surface):
        self.win = win
        self.pieces = []
        self.moves = []
        self.movecount = 0
        self.checkmate = False

    # -------------- DRAW METHODS----------------
    #draws blank chess board
    def initBoard(self):
        for i in range(0,8):
            for j in range(0,8):
                color = (self.beige, self.brown)[(i + j) % 2 == 1]
                pygame.draw.rect(self.win, color, (i * self.scale, j * self.scale, self.scale, self.scale))

    #draws board withg pieces
    def drawBoard(self):
        for i in range(0, len(self.pieces)):
            self.pieces[i].draw(self.win)

    #draws all possible moves on self.win
    def drawGen(self, index: int, posLast: list):
        genLegalMoves = self.genPieceLegalMoves(index, posLast)
        for i in range(len(genLegalMoves)):
            pygame.draw.rect(self.win, pygame.Color('0xFF6482'), (genLegalMoves[i][0] * self.scale, genLegalMoves[i][1] * self.scale, self.scale, self.scale))
    
    #draws all moves in input 'moves' list
    def drawLegalMoves(self, moves: list):
        for i in range(len(moves)):
            pygame.draw.rect(self.win, pygame.Color('0xFF6482'), (moves[i][0] * self.scale, moves[i][1] * self.scale, self.scale, self.scale))

    #-------GENERAL BOARD METHODS------------
    def initPieces(self):
        #WHITE PIECES
        for i in range(0,8):
            self.pieces.append(Pawn((i, 6), 0)) #0-7
        self.pieces.append(Rook((0,7), 0)) #8
        self.pieces.append(Rook((7,7), 0)) #9
        self.pieces.append(Knight((1,7), 0)) #10
        self.pieces.append(Knight((6,7), 0)) #11
        self.pieces.append(Bishop((2,7), 0)) #12
        self.pieces.append(Bishop((5,7), 0)) #13
        self.pieces.append(Queen((3,7), 0)) #14
        self.pieces.append(King((4,7), 0)) #15

        for i in range(0,8):
            self.pieces.append(Pawn((i, 1), 1)) #16-23
        self.pieces.append(Rook((0,0), 1)) #24
        self.pieces.append(Rook((7,0), 1)) #25
        self.pieces.append(Knight((1,0), 1)) #26
        self.pieces.append(Knight((6,0), 1)) #27
        self.pieces.append(Bishop((2,0), 1)) #28
        self.pieces.append(Bishop((5,0), 1)) #29
        self.pieces.append(Queen((3,0), 1)) #30
        self.pieces.append(King((4,0), 1)) #31

    def addMove(self, index: int, posLast: list):
        self.moves.append(Move(index, posLast, self.pieces[index].pos))

    def lastMove(self):
        self.moves[len(self.moves) - 1].moveBack(self)
        self.moves.pop(len(self.moves) - 1)

    def findPiece(self, posx: int, posy: int) -> int:
        for i in range(0, len(self.pieces)):
            if not isinstance(self.pieces[i], emptyPiece) and self.pieces[i].pos[0] == posx and self.pieces[i].pos[1] == posy:
                return i

    def clearSquare(self, search: int):
        if search is not None:
            self.pieces[search] = emptyPiece()

    def hasPieceMoved(self, index: int) -> bool: 
        output = False
        for i in range(1,len(self.moves) - 1):
            output = self.moves[i].pieceIndex == index or output
        return output 

    def movePiece(self, search: int, index: int, posLast: list, posNew: list):
        self.pieces[index].pos = posNew
        self.specialMover(search, index, posLast, False)
        self.clearSquare(search)
        self.addMove(index, posLast)
        self.movecount += 1

        if self.isCheckmate(self.movecount % 2):
            self.checkmate = True

    def makeBoardCopy(self):
        output = Board(self.win)
        output.pieces = copy.deepcopy(self.pieces)
        output.moves = copy.deepcopy(self.moves)
        output.movecount = copy.deepcopy(self.movecount)
        return output

    #--------PSEUDO VALID MOVE CHECK METHODS-----------------
    def isMovePseudoValid(self, search: int, index: int, posLast: list) -> bool:
        output = True

        if search is not None:
            output = self.pieces[search].color != self.pieces[index].color and output
        
        output = self.hopStop(index, posLast) and output

        #USED FOR PAWN CAPTURES AND ENPASSANT
        if isinstance(self.pieces[index], Pawn):
            output = self.pawnTake(search, index, posLast) and output

        #CASTLING
        if isinstance(self.pieces[index], King) and output:
            output = self.KingMove(search, index, posLast)

        return output
    
    def hopStop(self, index: int, posLast: list) -> bool:
        if isinstance(self.pieces[index], Knight):
            return True

        posCurr = self.pieces[index].pos
        temp = line(posLast[0], posLast[1], posCurr[0], posCurr[1])
        path = temp[1:len(temp) - 1]
        for i in range(0, len(self.pieces)):
            if self.pieces[i].pos in path:
                return False
        return True

    def enPassant(self, search: int, index: int, posLast: list) -> bool:
        diffx = self.pieces[index].pos[0] - posLast[0]
        diffy = self.pieces[index].pos[1] - posLast[1]
        xOffset = (diffx == -1 or diffx == 1)

        temp = self.findPiece(self.pieces[index].pos[0], posLast[1])
        isPawn = temp is not None and isinstance(self.pieces[temp], Pawn)

        lastMove = self.moves[len(self.moves) - 1]
        justMoved = len(self.moves) > 1 and lastMove.pieceIndex == temp
        doublePawnPush = justMoved and (lastMove.posLast[1] - lastMove.posNew[1] == -2 or lastMove.posLast[1] - lastMove.posNew[1] == 2)

        possible = search is None and isPawn and xOffset and doublePawnPush
        return possible

    def pawnTake(self, search: int, index: int, posLast: list) -> bool:
        if self.enPassant(search, index, posLast):
            return True
        diffx = self.pieces[index].pos[0] - posLast[0]
        diffy = self.pieces[index].pos[1] - posLast[1]
        if search is not None:
            return (diffx == -1 or diffx == 1)
        else:
            return not (diffx == -1 or diffx == 1)

    def doublePawnPush(self, index: int) -> bool:
        if self.pieces[index].pos[1] == 6 and self.pieces[index].color ==  0:
            return True
        elif self.pieces[index].pos[1] == 1 and self.pieces[index].color ==  1:
            return True
        return False

    def promotePawn(self, index: int, genFlag: bool) -> Union[bool, None]:
        temp = self.pieces[index]
        if (temp.pos[1] == 0 and temp.color == 0) or (temp.pos[1] == 7  and temp.color == 1):
            if genFlag:
                self.pieces[index] = Queen(temp.pos, temp.color)
            else:
                exit = False
                print("Q:Knight - W:Bishop - E:Rook - R:Queen")
                while not exit:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                self.pieces[index] = Knight(temp.pos, temp.color)
                                exit = True
                            elif event.key == pygame.K_w:
                                self.pieces[index] = Bishop(temp.pos, temp.color)
                                exit = True
                            elif event.key == pygame.K_e:
                                self.pieces[index] = Rook(temp.pos, temp.color)
                                exit = True
                            elif event.key == pygame.K_r:
                                self.pieces[index] = Queen(temp.pos, temp.color)
                                exit = True

    def KingMove(self, search: int, index: int, posLast: list) -> bool:
        diffx = self.pieces[index].pos[0] - posLast[0]
        diffy = self.pieces[index].pos[1] - posLast[1]

        if (not self.hasPieceMoved(index) and (diffx == -2 or diffx == 2) and 
        diffy == 0 and (self.pieces[index].pos[1] == 0 or self.pieces[index].pos[1] == 7)):
            return self.Castling(index, posLast, diffx)
        elif ((-1 == diffy or diffy == 1) or (-1 == diffx or diffx == 1)) and (diffx != 2 and diffx !=-2):
            return True
        return False

    def Castling(self, index: int, posLast: list, diffx: int) -> bool:
        if self.hasPieceMoved(index) or isinstance(self.pieces[index], emptyPiece):
            return False
        if self.pieces[index].color == 0: #white
            if diffx == 2: #KING SIDE
                return not self.hasPieceMoved(9)
            else: #QUEEN SIDE
                return not self.hasPieceMoved(8) and self.findPiece(1, 7) is None
        else: #BLACK
            if diffx == 2: #KING SIDE
                return not self.hasPieceMoved(25)
            else: #QUEEN SIDE
                return not self.hasPieceMoved(24) and self.findPiece(1, 0) is None

    def specialMover(self, search: int, index: int, posLast: list, genFlag: bool) -> Union[bool, None]:
        if isinstance(self.pieces[index],Pawn) and self.enPassant(search, index, posLast):
            self.clearSquare(self.findPiece(self.pieces[index].pos[0], posLast[1]))
        if isinstance(self.pieces[index],Pawn):
            self.promotePawn(index, genFlag)
                
        diffx = self.pieces[index].pos[0] - posLast[0]
        if isinstance(self.pieces[index], King) and self.KingMove(search, index, posLast):
            if diffx == 2 and self.pieces[index].color == 0:
                self.pieces[9].pos = (5,7)
            elif diffx == 2 and self.pieces[index].color == 1:
                self.pieces[25].pos = (5,0)
            elif diffx == -2 and self.pieces[index].color == 0:
                self.pieces[8].pos = (3,7)
            elif diffx == -2 and self.pieces[index].color == 1:
                self.pieces[24].pos = (3,0)

    #------------ CHECK METHODS ---------------
    def isKingInCheck(self, color: int) -> bool:
        pseudoLegalMoves = self.genColorPseudoMoves((color + 1) % 2)
        kingIndex = 15 if color == 0 else 31

        for i in range(len(pseudoLegalMoves)):
            if self.pieces[kingIndex].pos == pseudoLegalMoves[i]:
                return True
        return False

    def isCheckmate(self, color: int) -> bool:
        if self.isKingInCheck(color):
            return len(self.genColorLegalMoves(color)) == 0
        return False

    #------------ LEGAL MOVE CHECK METHODS ------------------
    def isLegalMove(self, index: int, search: int, posLast: list, posCurrent: list) -> bool:
        piecePseudoMoves = self.genPiecePseudoMoves(index, posLast)

        if posCurrent in piecePseudoMoves and posCurrent is not posLast:
            testerBoard = self.makeBoardCopy()
            testerBoard.pieces[index].pos = posCurrent
            testerBoard.clearSquare(search)
            testerBoard.specialMover(search, index, posLast, True)
            if testerBoard.isKingInCheck(testerBoard.movecount % 2):
                return False
            return True
        return False
    
    #------------ MOVE GENERATION METHODS ------------------
    def genPieceAllMoves(self, index: int, pos: list) -> list:
        temp = self.pieces[index]
        temp.pos = pos
        output = self.pieces[index].genMoves()
        return output
    
    def genPiecePseudoMoves(self, index: int, pos: list) -> list:
        return self.makeGenValid(self.genPieceAllMoves(index, pos), index, pos)

    def makeGenValid(self, moves: list, index: int, pos: list) -> list:
        output = []
        for i in range(len(moves)):
            search = self.findPiece(moves[i][0], moves[i][1])
            self.pieces[index].pos = (moves[i][0], moves[i][1])
            if (0 <= moves[i][0] < 8) and (0 <= moves[i][1] < 8) and self.isMovePseudoValid(search, index, pos):
                output.append(moves[i])
            self.pieces[index].pos = pos
        return output

    def genPieceLegalMoves(self, index: int, pos: list) -> list:
        pseudo = self.genPiecePseudoMoves(index, pos)
        output = []
        for i in range(len(pseudo)):
            if self.isLegalMove(index, self.findPiece(pseudo[i][0], pseudo[i][1]), pos, pseudo[i]):
                output.append(pseudo[i])
        return output

    def genColorPseudoMoves(self, color: int):
        inc = 0 if color == 0 else 16
        output = []
        for i in range(0,15):
            output = self.genPiecePseudoMoves(i+inc, self.pieces[i+inc].pos) + output
        return output

    def genColorLegalMoves(self, color: int):
        inc = 0 if color == 0 else 16
        output = []
        for i in range(16):
            output.append(self.genPieceLegalMoves(i+inc, self.pieces[i+inc].pos))
        return output

    def genCheckSquares(self) -> list:
        king = self.pieces[29] if self.movecount % 2 == 0 else self.pieces[31]
        tempKnight = Knight(king.pos, king.color)
        tempQueen = Queen(king.pos, king.color)
        self.pieces.append(tempKnight)
        self.pieces.append(tempQueen)
        output = self.genPiecePseudoMoves(32, king.pos) + self.genPiecePseudoMoves(33, king.pos)
        self.pieces.pop(32)
        self.pieces.pop(33)
        return output

    #----------- EVALUATE METHODS ---------------
    def makePos(self, index: int, posNew: list) -> list:
        tempBoard = self.makeBoardCopy()


        search = tempBoard.findPiece(posNew[0], posNew[1])
        tempBoard.clearSquare(search)
        posLast = tempBoard.pieces[index].pos
        tempBoard.pieces[index].pos = posNew
        tempBoard.specialMover(search, index, posLast, True)
        return tempBoard.pieces

    def evalPos(self, color: int, pieces: list) -> int:
        temp = self.makeBoardCopy()
        temp.pieces = pieces
        if temp.isCheckmate((color + 1) % 2):
            return math.inf

        inc = 0 if color == 0 else 16
        selfValue = 0
        oppValue = 0
        otherVal = 0
        for piece in pieces:
            if piece.color == color:
                selfValue += piece.val
            else:
                oppValue += piece.val
            otherVal += self.evalPiecePos(piece)
        
        if temp.isKingInCheck((color + 1) % 2):
            otherVal += 100
        
        return (selfValue - oppValue) + otherVal

    def evalPiecePos(self, piece: Piece) -> int:
        if isinstance(piece, Pawn):
            return self.evalPawnPos(piece)
        elif isinstance(piece, Knight):
            return self.evalKnightPos(piece)
        elif isinstance(piece, Bishop):
            return self.evalBishopPos(piece)
        elif isinstance(piece, Rook):
            return self.evalRookPos(piece)
        elif isinstance(piece, King):
            return self.evalKingPos(piece)
        else:
            return 0

    def evalPawnPos(self, piece: Piece) -> int:
        if piece.pos in ((3,3), (3,4), (4,3), (4,4)):
            return 75
        elif piece.pos in ((1,2), (1,5), (6,1), (6,5)):
            return 25
        return 0

    def evalKnightPos(self, piece: Piece) -> int:
        if piece.pos in ((3,3), (3,4), (4,3), (4,4)):
            return 50
        elif piece.pos in ((2,5), (5,5), (2,2), (5,2)):
            return 25
        return 0
    
    def evalBishopPos(self, piece: Piece) -> int:
        if piece.pos in ((1,1), (1,6), (6,6), (6,1)):
            return 50
        elif piece.pos in ((1,2), (1,5), (6,1), (6,5), (2,3), (2,4), (5,3), (5,4)):
            return 25
        return 0

    def evalRookPos(self, piece: Piece) -> int:
        if piece.pos in ((3,7), (4,7), (3,0), (4,0)):
            return 75
        elif piece.pos in ((3,6), (4,6), (3,1), (4,1), (2,7), (5,7), (2,0), (5,0)):
            return 50
        return 0

    def evalKingPos(self, piece: Piece) -> int:
        if piece.pos in ((0,7), (1,7), (6,7), (7,7), (0,0), (1,0), (6,0), (7,0)):
            return 100
        return 0

#FOR CONVERTING FENS STRING TO BOARD DATA STRUCTURE
def fenToPieces(fen: str) -> list:
    fenArr = fen.split("/")
    pieceArr = [emptyPiece()] * 32
    pieceStr = "PRNBQKprnbqk"
    lastNum = 0

    pW, pB, nW, nB, bW, bB, rW, rB = 0, 16, 10, 26, 12, 28, 8, 24

    for i in range(8):
        for j in range(len(fenArr[i])):
            if fenArr[i][j] in pieceStr:
                if fenArr[i][j] == 'P':
                    pieceArr[pW] = Pawn((lastNum, i), 0)
                    pW += 1
                elif fenArr[i][j] == 'p':
                    pieceArr[pB] = (Pawn((lastNum, i), 1))
                    pB += 1
                elif fenArr[i][j] == 'N':
                    pieceArr[nW] = Knight((lastNum, i), 0)
                    nW += 1
                elif fenArr[i][j] == 'n':
                    pieceArr[nB] = Knight((lastNum, i), 1)
                    nB += 1
                elif fenArr[i][j] == 'B':
                    pieceArr[bB] = Bishop((lastNum, i), 0)
                    bW += 1
                elif fenArr[i][j] == 'b':
                    pieceArr[bB] = Bishop((lastNum, i), 1)
                    bB += 1
                elif fenArr[i][j] == 'R':
                    pieceArr[rW] = Rook((lastNum, i), 0)
                    rW += 1
                elif fenArr[i][j] == 'r':
                    pieceArr[rB] = Rook((lastNum, i), 1)
                    rB += 1
                elif fenArr[i][j] == 'Q':
                    pieceArr[14] = Queen((lastNum, i), 0)
                elif fenArr[i][j] == 'q':
                    pieceArr[30] = Queen((lastNum, i), 0)
                elif fenArr[i][j] == 'K':
                    pieceArr[15] = King((lastNum, i), 0)
                elif fenArr[i][j] == 'k':
                    pieceArr[31] = King((lastNum, i), 1)
                lastNum += 1
            else: 
                lastNum += int(fenArr[i][j])
        lastNum = 0
    return pieceArr

def findInList(elem: Piece, color: int, lst: list):
    for item in lst:
        if isinstance(elem, item) and item.color == color:
            return item
    return emptyPiece()

def findMove(orig: list, new: list) -> list:
    for i in range(31):
        if orig[i].pos != new[i].pos:
            return (i, orig[i].pos, new[i].pos)
    return (-1,-1,-1)

class BoardTree:
    def __init__(self, board: Board, pieces: list, nodes: list):
        self.board = board
        self.pieces = pieces
        self.nodes = nodes

    def sizeAtDepth(self, depth: int, acc: int):
        if depth == 0:
            return 1

        if depth == acc:
            return 1
        else:
            size = 0
            for i in range(len(self.nodes)):
                size += self.nodes[i].sizeAtDepth(depth, acc+1)
            return size

    def minSearch(self, depth: int, color: int, alpha: int, beta: int):
        if depth == 0:
            return (-self.board.evalPos(color, self.pieces), [])
        
        bestMove = []
        for board in self.nodes:
            score = board.maxSearch(depth - 1, (color + 1) % 2, alpha, beta)
            if score[0] <= alpha:
                return (alpha, board.pieces)
            if score[0] < beta:
                beta = score[0]
                bestMove = board.pieces
        return (beta, bestMove)

    def maxSearch(self, depth: int, color: int, alpha: int, beta: int):
        if depth == 0:
            return (self.board.evalPos(color, self.pieces), [])
        
        bestMove = []
        for board in self.nodes:
            score = board.minSearch(depth - 1, (color + 1) % 2, alpha, beta)
            if score[0] >= beta:
                return (beta, board.pieces)
            if score[0] > alpha:
                alpha = score[0]
                bestMove = board.pieces
        return (alpha, bestMove)

    def printTree(self, depth, acc):
        color = (self.board.movecount + acc) % 2
        print("Depth: %s, Type: %s, Eval: %s" % (acc, type(self),self.board.evalPos(color, self.pieces)))

        if acc < depth:
            for i in range(len(self.nodes)):
                self.nodes[i].printTree(depth, acc + 1)

class EndGame:
    def __init__(self, pieces: list):
        self.pieces = pieces
    def sizeAtDepth(self, depth: int, acc: int):
        return 1
    def minSearch(self, depth: int, color: int, alpha: int, beta: int):
        return (-math.inf, self.pieces)
    def maxSearch(self, depth: int, color: int, alpha: int, beta: int):
        return (math.inf, self.pieces)
    def printTree(self, depth, acc):
        print("Depth: %s, Type: %s, Eval: %s" % (acc, type(self), math.inf))

class Leaf:
    def __init__(self):
        self.value = None
    def sizeAtDepth(self, depth: int, acc: int):
        return 0
    def minSearch(self, depth: int, color: int, alpha: int, beta: int):
        return (-math.inf, [])
    def maxSearch(self, depth: int, color: int, alpha: int, beta: int):
        return (math.inf, [])
    def printTree(self, depth, acc):
        color = (self.board.movecount + acc) % 2
        print("Depth: %s, Type: %s, Eval: %s" % (acc, type(self), -1))

        if acc < depth:
            for i in range(len(self.nodes)):
                self.nodes[i].printTree(depth, acc + 1)

class Bot:
    def __init__(self, board: Board):
        self.board = board.makeBoardCopy()

        self.evalTree = Leaf()

    def initBoardTree(self, pieces: list, depth: int, color: int):
        inc = 0 if color == 0 else 16
        nodes = []
        if depth > 0:
            temp = self.board.makeBoardCopy()
            temp.pieces = pieces
            moves = temp.genColorLegalMoves(color)
            for i in range(16):
                if len(moves[i]) != 0:
                    for j in range(len(moves[i])):
                        newBoard = temp.makePos(i+inc, moves[i][j])
                        nodes.append(self.initBoardTree(newBoard, depth - 1, (color + 1) % 2))
            if len(nodes) == 0:
                return EndGame(pieces)
            else:
                return BoardTree(temp, pieces, nodes)
                # return BoardTree(0, [], nodes) #For testing with less memory use
        else:
            nodes.append(Leaf())
            return BoardTree(self.board, pieces, nodes)
            # return BoardTree(0, [], nodes) #For testing with less memory use

    def endGame(self, moves: list):
        output = True
        for move in moves:
            output = output and (len(move) == 0)
        return output

    def MiniMax(self, depth: int) -> list:
        start = time.perf_counter()

        tree = self.initBoardTree(self.board.pieces, depth, self.board.movecount % 2)
        bestMove = tree.maxSearch(depth, self.board.movecount % 2, -math.inf, math.inf)

        end = time.perf_counter()

        print("Time: %s s" % (end - start))
        return bestMove

class Game:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.clicked = False
        self.exit = False
        self.genMoves = []

        self.board = Board(win)
        self.board.initBoard()
        self.board.initPieces()
        self.board.moves.append(self.board.pieces)

        self.bot = Bot(self.board)

    def run(self):
        index = None
        posLast = []
        while not self.exit:
            pos = pygame.mouse.get_pos()
            posx = int(pos[0] / 100)
            posy = int(pos[1] / 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.KEYDOWN:
                    self.keyHandler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = self.mouseHandler(index, posLast, posx, posy)
                    index = click[0]
                    posLast = click[1]
            self.onTick(index, posLast, pos)

    def keyHandler(self, event: pygame.event) -> None:
        if event.key == pygame.K_SPACE:
            bot = Bot(self.board)
            bestMove = bot.MiniMax(2)
            move = findMove(self.board.pieces, bestMove[1])
            self.board.pieces = bestMove[1]
            self.board.movecount += 1
            self.board.moves.append(Move(move[0], move[1], move[2]))
        elif event.key == pygame.K_LEFT:
            if len(self.board.moves) > 1:
                self.board.lastMove()
                self.board.movecount -= 1
        elif event.key == pygame.K_1:
            bot = Bot(self.board)
            d1 = bot.initBoardTree(self.board.pieces, 1, self.board.movecount % 2)
            depth = d1.sizeAtDepth(1,0)
            print (depth)
        elif event.key == pygame.K_2:
            bot = Bot(self.board)

            start = time.perf_counter()
            d2 = bot.initBoardTree(self.board.pieces, 2, self.board.movecount % 2)
            end = time.perf_counter()
            timeTaken = end - start
            print ("Time: %s" % timeTaken)

            depth = d2.sizeAtDepth(2,0)
            print ("Combinations: %s" % depth)
        elif event.key == pygame.K_3:
            bot = Bot(self.board)

            start = time.perf_counter()
            d3 = bot.initBoardTree(self.board.pieces, 3, self.board.movecount % 2)
            end = time.perf_counter()
            timeTaken = end - start
            print ("Time: %s" % timeTaken)

            depth = d3.sizeAtDepth(3,0)
            print ("Combinations: %s" % depth)
        elif event.key == pygame.K_4:
            bot = Bot(self.board)

            start = time.perf_counter()
            d4 = bot.initBoardTree(self.board.pieces, 4, self.board.movecount % 2)
            end = time.perf_counter()
            timeTaken = end - start
            print ("Time: %s" % timeTaken)

            depth = d4.sizeAtDepth(4,0)
            print ("Combinations: %s" % depth)
        elif event.key == pygame.K_5:
            bot = Bot(self.board)

            start = time.perf_counter()
            d5 = bot.initBoardTree(self.board.pieces, 5, self.board.movecount % 2)
            end = time.perf_counter()
            timeTaken = end - start
            print ("Time: %s" % timeTaken)

            depth = d5.sizeAtDepth(5,0)
            print ("Combinations: %s" % depth)
        elif event.key == pygame.K_b:
            bot = Bot(self.board)
            bestMove = bot.MiniMax(2)
            self.board.pieces = bestMove
            self.board.movecount += 1 
        elif event.key == pygame.K_r:
            self.board = Board(self.win)
            self.board.initPieces()
            self.board.moves = []
            self.board.movecount = 0
            self.board.moves.append(self.board.pieces)
        elif event.key == pygame.K_ESCAPE:
            self.exit = True
        elif event.key == pygame.K_f:
            pieceArr = fenToPieces("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8")
            self.board.pieces = pieceArr
        elif event.key == pygame.K_p:
            bot = Bot(self.board)
            tree = bot.initBoardTree(bot.board.pieces, 2, bot.board.movecount % 2)
            tree.printTree(2, 0)
        elif event.key == pygame.K_o:
            output = self.board.genColorLegalMoves(self.board.movecount % 2)
            total = 0
            for i in range(16):
                total += len(output[i])
            print(total)
        elif event.key == pygame.K_RETURN:
            output = self.board.genColorLegalMoves(self.board.movecount % 2)
            print(output)

    def mouseHandler(self, index: int, posLast: list, posx: int, posy: int) -> list:
        if self.clicked:
            search = self.board.findPiece(posx, posy)

            if self.board.isLegalMove(index, search, posLast, (posx, posy)):
                self.board.movePiece(search, index, posLast, (posx, posy))
                self.clicked = False

            else: #moves piece back to posLast if piece move not valid
                self.board.pieces[index].pos = posLast
                self.clicked = False
        else:
            index = self.board.findPiece(posx, posy)
            if index is not None and self.board.pieces[index].color == (self.board.movecount % 2):
                posLast = self.board.pieces[index].pos
                self.genMoves = self.board.genPieceLegalMoves(index, posLast)
                self.clicked = True

        return (index, posLast)

    def onTick(self, index: int, posLast: list, mousePos: list) -> None:
        self.board.initBoard()
        if self.clicked:
            self.board.drawLegalMoves(self.genMoves)
            self.board.pieces[index].pos = (mousePos[0] / 100 - 0.5, mousePos[1] / 100 - 0.5)
        if self.board.checkmate:
            self.exit = True
        self.board.drawBoard()    
        pygame.display.update()

def main():
    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Chess")
    chessGame = Game(win)
    chessGame.run()


main()
quit()
