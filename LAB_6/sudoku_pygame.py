import pygame
import sys
import time
from src.CSPclass import CSP
from src.CSPclass import CSPBasic
from src.CSPS import SudokuCSP
from src.algorithms import AC3, backtracking_search
import copy



pygame.init()

PADDING = 60
WIDTH, HEIGHT = 750, 750 + PADDING

ROWS, COLS = 9, 9
CELL_SIZE = WIDTH // COLS
# black
LINE_COLOR = (0, 0, 0)
# white
BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_COLOR_ASTERISKS = (255, 192, 203) #pink
# for each sub-section of cells
BOLD_LINE_WIDTH = 4
# for each cell inside sub-section
THIN_LINE_WIDTH = 1

FONT_STEPS = pygame.font.SysFont('arial', 30)
FONT_NUMS = pygame.font.SysFont('arial', 70)
FONT_DOMAINS = pygame.font.SysFont('arial', 20)

steps = 0

GLOBAL_MOUSE_X = 0
GLOBAL_MOUSE_Y = 0

# 1, 2, 3
# 1 displays original board
# 2 displays ARC domain result board
# 3 displays completely solved board
STATE_SELECTOR = 1


# create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asterisk Sudoku")


board_og = [
    [0,1,0,0,0,0,0,6,0],
    [3,0,9,0,0,0,1,0,5],
    [0,8,0,3,0,5,0,7,0],
    [0,0,2,0,7,0,8,0,0],
    [0,0,0,6,0,8,0,0,0],
    [0,0,8,0,9,0,2,0,0],
    [0,2,0,4,0,1,0,9,0],
    [9,0,4,0,0,0,6,0,1],
    [0,3,0,0,0,0,0,8,0],
]



def event_handler(board_sol):
    global STATE_SELECTOR
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if STATE_SELECTOR == 0:
                    draw_board(board_og)
                    
                elif STATE_SELECTOR == 1:
                    draw_board(board_sol)
                    
                pygame.display.flip()
                
                global steps
                steps += 1
                STATE_SELECTOR = (STATE_SELECTOR + 1) % 2

def mouse_hover_info(saved_domain_state):
    if STATE_SELECTOR != 1:
        return
    global GLOBAL_MOUSE_X
    global GLOBAL_MOUSE_Y
    m_posX, m_posY = pygame.mouse.get_pos()
    if GLOBAL_MOUSE_X != int(m_posX) or GLOBAL_MOUSE_Y != int(m_posY):
        screen.fill(BACKGROUND_COLOR)
        draw_board(board_og)
    print(f"Mouse: ({m_posX},{m_posY})")
    cell_x = None
    cell_y = None
    gap_x = WIDTH // COLS
    cell_x = m_posX // gap_x + 1
    
    gap_y = (HEIGHT - PADDING) // ROWS
    cell_y = m_posY // gap_y
    
    if (not (1 <= cell_x <= COLS) or not (1 <= cell_y <= ROWS)):
        return
    
    num_alpha = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "F": 6,
        "G": 7,
        "H": 8,
        "I": 9
    }
    # keep cell_x as integer
    # convert cell_y to uppercase char
    cell_letter = [k for k, v in num_alpha.items() if v == cell_y][0]
    true_cell = f"{cell_letter}{cell_x}"
    if true_cell in saved_domain_state:
        val = saved_domain_state[true_cell]
        text = FONT_DOMAINS.render(str(val), True, (0, 0, 0))
        # use cell size and row number to get position on vanvas of number to place
        text_rec = text.get_rect(center=(
            (cell_x - 1) * CELL_SIZE + CELL_SIZE // 2,
            (cell_y - 1) * CELL_SIZE + CELL_SIZE // 2 + (PADDING)
        ))
        # destination.blit(source, position)
        screen.blit(text, text_rec)
        


def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    
    # draw step counter global
    steps_surface = FONT_STEPS.render(f"STEP: {steps}", True, (0,0,0))
    steps_rect = steps_surface.get_rect(center=(WIDTH//2, PADDING - 20))
    screen.blit(steps_surface, steps_rect)
    

    # draw grid lines
    for i in range(ROWS + 1):
        # very third line is bold
        line_width = None
        if i % 3 == 0:
            line_width = BOLD_LINE_WIDTH
        else:
            line_width = THIN_LINE_WIDTH
        assert line_width is not None, "Line must have value that is not None"
        
        pygame.draw.line(screen, LINE_COLOR, (0, PADDING + i * CELL_SIZE), (WIDTH, PADDING + i * CELL_SIZE), line_width)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, PADDING), (i * CELL_SIZE, HEIGHT + PADDING), line_width)
        
        
    # color asterisk cells in pink
    for row in range(ROWS):
        letter = chr(ord('A') + row)
        for col in range(COLS):
            cell_col = str(col + 1)
            cell = letter + cell_col
            ast_cells = [
                'B5',
                'C3',
                'C7',
                'E2',
                'E5',
                'E8',
                'G3',
                'G7',
                'H5'
            ]
            if cell in ast_cells:
                rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE + PADDING, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BACKGROUND_COLOR_ASTERISKS, rect)
        
    # draw numbers from board onto grid
    for row in range(ROWS):
        for col in range(COLS):
            num = board[row][col]
            # leave zeros blank for now
            if num != 0:
                # render(string_to_print, bool: antialias doesnt matter , color (rgb))
                text = FONT_NUMS.render(str(num), True, (0, 0, 0))
                # use cell size and row number to get position on vanvas of number to place
                text_rec = text.get_rect(center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + PADDING))
                # destination.blit(source, position)
                screen.blit(text, text_rec)
    
    #mouse_hover_info(saved_domain_state)
    
                
    
saved_domain_state = None

def main():
    clock = pygame.time.Clock()
    
    sudoku_csp = SudokuCSP(board_og)

    result, checks = AC3(sudoku_csp)
    print("bool: ", result)
    print("checks: ", checks)
    for key in sudoku_csp.curr_domains.keys():
        print(f"{key}: {sudoku_csp.curr_domains[key]}")
        
    # save this state in local dict
    global saved_domain_state
    saved_domain_state = copy.deepcopy(sudoku_csp.curr_domains)
    
    board_sol = copy.deepcopy(board_og)
    if result == True:
        # returns full solution after AC3 runs for checks
        sol = backtracking_search(sudoku_csp)
        if sol:
            print("Solution: ", sol)
            # updates matrix grid according to solution
            for cell_name, val in sol.items():
                row = ord(cell_name[0]) - ord('A')
                col = int(cell_name[1]) - 1
                board_sol[row][col] = val
        else:
            print("No solution found")
            return
    else:
        print("AC3 does not check successfully")
        return
    
    if sol is not None:
        for key, val in sol.items():
            print(f"{key}: {val}")
    else:
        print("Sol is None")
        return

    draw_board(board_og)
    
    while True:
        event_handler(board_sol)
        mouse_hover_info(saved_domain_state)
        pygame.display.flip()
        clock.tick(60)



main()
