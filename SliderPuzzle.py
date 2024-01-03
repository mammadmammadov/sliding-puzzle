'''
Created on Jan 19, 2022

@author: mammad
'''

import os 
import sys
import cfg
import random
import pygame



def isGameOver(board, size):
    assert isinstance(size, int)  # checking whether the size is integer
    numberOfCells = size * size
    for i in range(numberOfCells - 1):
        if board[i] != i:
            return False
    return True


def moveRight(board, blankCellIndex, numberOfColumns):
    if blankCellIndex % numberOfColumns == 0: 
        return blankCellIndex  # edges, can be shown on paper
    board[blankCellIndex - 1], board[blankCellIndex] = board[blankCellIndex], board[blankCellIndex - 1]
    return blankCellIndex - 1;


def moveLeft(board, blankCellIndex, numberOfColumns):
    if (blankCellIndex + 1) % numberOfColumns == 0: 
        return blankCellIndex  # edges, can be shown on paper
    board[blankCellIndex + 1], board[blankCellIndex] = board[blankCellIndex], board[blankCellIndex + 1]
    return blankCellIndex + 1;


def moveDown(board, blankCellIndex, numberOfColumns):
    if blankCellIndex < numberOfColumns:  # top row
        return blankCellIndex
    board[blankCellIndex - numberOfColumns], board[blankCellIndex] = board[blankCellIndex], board[blankCellIndex - numberOfColumns]
    return blankCellIndex - numberOfColumns


def moveUP(board, blankCellIndex, numberOfRows, numberOfColumns):
    if blankCellIndex >= (numberOfRows - 1) * numberOfColumns: return blankCellIndex  # bottom row
    board[blankCellIndex + numberOfColumns], board[blankCellIndex] = board[blankCellIndex], board[blankCellIndex + numberOfColumns]
    return blankCellIndex + numberOfColumns


def CreateBoard(numberOfRows, numberOfColumns, numberOfCells):
    board = []  # empty list
    
    for i in range(numberOfCells):
        board.append(i)
        
    blankCellIndex = numberOfCells - 1
    board[blankCellIndex] = -1
    
    # the code below shuffles the board with random positions
    
    for i in range(cfg.RANDOM_NUMBER):
        direction = random.randint(0, 3)
        
        if direction == 0:
            blankCellIndex = moveLeft(board, blankCellIndex, numberOfColumns)
        elif direction == 1:
            blankCellIndex = moveRight(board, blankCellIndex, numberOfColumns)
        elif direction == 2:
            blankCellIndex = moveUP(board, blankCellIndex, numberOfRows, numberOfColumns)
        elif direction == 3:
            blankCellIndex = moveDown(board, blankCellIndex, numberOfColumns)
    return board, blankCellIndex


def GetImagePath(rootDirectory):
    imageNames = os.listdir(rootDirectory)
    assert len(imageNames) > 0
    return os.path.join(rootDirectory, random.choice(imageNames))  # random.choice returns random element from a string, a range, a list, a tuple or any other kind of sequence

    
def ShowEndInterface(screen, width, height):
    screen.fill(cfg.BACKGROUND_COLOR)
    font = pygame.font.Font(cfg.FONT_PATH, width // 12)
    title = font.render('You Won!', True, (233, 150, 122))  # Pygame does not provide a direct way to write text onto a Surface object. The method render() must be used to create a Surface object from the text, which then can be blit to the screen.
    rectangle = title.get_rect()
    rectangle.midtop = (width / 1.8, height / 2.4)
    screen.blit(title, rectangle)  # adds objects to screen
    pygame.display.update()
    # code below helps to quit the game
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()


def ShowStartInterface(screen, width, height):
    screen.fill(cfg.BACKGROUND_COLOR)
    titleFont = pygame.font.Font(cfg.FONT_PATH, width // 10)
    contentFont = pygame.font.Font(cfg.FONT_PATH, width // 20)
    title = titleFont.render("Sliding Puzzle", True, cfg.RED)
    content_1 = contentFont.render("Choose your size for the puzzle.", True, cfg.BLUE)
    content_2 = contentFont.render("F - 2x2, B - 3x3, J - 4x4", True, cfg.BLUE)
    titleRectangle = title.get_rect()
    titleRectangle.midtop = (width / 2, height / 10)
    
    content_1_Rectangle = content_1.get_rect()
    content_1_Rectangle.midtop = (width / 2, height / 2.2)
    
    content_2_Rectangle = content_2.get_rect()
    content_2_Rectangle.midtop = (width / 2, height / 1.8)
    
    screen.blit(title, titleRectangle)
    screen.blit(content_1, content_1_Rectangle)
    screen.blit(content_2, content_2_Rectangle)
    
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('f'): return 2  # ord returns the value of the char
                elif event.key == ord('b'): return 3
                elif event.key == ord('j'): return 4
        pygame.display.update()

        
def main():
    pygame.init()  # initialization in main function
    
    game_image_used = pygame.image.load(GetImagePath(cfg.PICTURE_ROOT_DIRECTORY))
    game_image_used = pygame.transform.scale(game_image_used, cfg.WINDOW_SIZE)  # adjusting the size of the picture to the screen
    game_image_used_rectangle = game_image_used.get_rect()
    
    screen = pygame.display.set_mode(cfg.WINDOW_SIZE)
    pygame.display.set_caption('Slide Puzzle')
    
    size = ShowStartInterface(screen, game_image_used_rectangle.width, game_image_used_rectangle.height)
    assert isinstance(size, int)
    numberOfRows, numberOfColumns = size, size
    numberOfCells = size * size

    cellWidth = game_image_used_rectangle.width // numberOfColumns
    cellHeight = game_image_used_rectangle.height // numberOfRows
    
    while True:
        board, blankCellIndex = CreateBoard(numberOfRows, numberOfColumns, numberOfCells)
        if not isGameOver(board, size):
            break
    is_running = True
    
    while is_running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    blankCellIndex = moveLeft(board, blankCellIndex, numberOfColumns)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    blankCellIndex = moveRight(board, blankCellIndex, numberOfColumns)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    blankCellIndex = moveUP(board, blankCellIndex, numberOfRows, numberOfColumns)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    blankCellIndex = moveDown(board, blankCellIndex, numberOfColumns) 
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                x, y= pygame.mouse.get_pos()
                x_position = x//cellWidth
                y_position = y//cellHeight        
                index = x_position + y_position*numberOfColumns  #can be proved on paper with mathematics
                if index == blankCellIndex - 1:
                    blankCellIndex = moveRight(board, blankCellIndex, numberOfColumns)
                elif index == blankCellIndex + 1:
                    blankCellIndex = moveLeft(board, blankCellIndex, numberOfColumns)
                elif index == blankCellIndex + numberOfColumns:
                    blankCellIndex = moveUP(board, blankCellIndex, numberOfRows, numberOfColumns)
                elif index == blankCellIndex - numberOfColumns:
                    blankCellIndex = moveDown(board, blankCellIndex, numberOfColumns)
                  
        if isGameOver(board, size):
            board[blankCellIndex] = numberOfCells - 1
            is_running = False  
        
        screen.fill(cfg.BACKGROUND_COLOR)
        for i in range(numberOfCells):
            if board[i] == -1:
                continue
            x_position = i // numberOfColumns
            y_position = i % numberOfColumns
            
            rectangle = pygame.Rect(y_position*cellWidth, x_position*cellHeight, cellWidth, cellHeight)
            imageArea = pygame.Rect((board[i]%numberOfColumns)*cellWidth, (board[i]//numberOfColumns)*cellHeight, cellWidth, cellHeight)             
            
            screen.blit(game_image_used, rectangle, imageArea)
            
        for i in range(numberOfColumns+1):
            pygame.draw.line(screen, cfg.BLACK, (i*cellWidth, 0), (i*cellWidth, game_image_used_rectangle.height)) #line(surface, color, start_pos, end_pos) -> Rect
        for i in range(numberOfRows+1):
            pygame.draw.line(screen, cfg.BLACK, (0, i*cellHeight), (game_image_used_rectangle.width, i*cellHeight))
                
        pygame.display.update()
    ShowEndInterface(screen, game_image_used_rectangle.width, game_image_used_rectangle.height)
       
if __name__ == '__main__':
    main()
