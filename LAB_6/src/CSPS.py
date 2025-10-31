from src.CSPclass import CSP
from src.utils import *

def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)

# true if two cells in same subgroup
# else is false
def same_block(cell1, cell2):
    # convert rows 'A' -> 'I' to nums 0 -> 8
    row1 = ord(cell1[0]) - ord('A')
    row2 = ord(cell2[0]) - ord('A')
    
    # convert columns 1 -> 9 to numbers 0 -> 8
    col1 = int(cell1[1]) - 1
    col2 = int(cell2[1]) - 1
    
    # each block is 3 x 3 so we get the block a board[row][col] is in
    block_row1 = row1 // 3
    block_row2 = row2 // 3
    block_col1 = col1 // 3
    block_col2 = col2 // 3
    
    # true if they are in same block
    return (block_row1 == block_row2) and (block_col1 == block_col2)


def same_asterisk(cell1, cell2):
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
    
    if cell1 in ast_cells:
        if cell2 in ast_cells:
            return True
    return False




def SudokuCSP(board):
    
    ROWS = len(board)
    COLS = len(board[0])
        
    var1 = list("ABCDEFGHI")
    var2 = range(1, 10)
    sudokuNeighbors = {}

    # get neighbors for each cell 
    for r1 in var1:
        for c1 in var2:
            key = r1 + str(c1)
            sudokuNeighbors[key] = []

            for r2 in var1:
                for c2 in var2:
                    other = r2 + str(c2)
                    if other == key:
                        continue
                    # takes constraint that they are same row OR col OR subgroup (same_block()) OR in asterisk
                    same_row = r1 == r2
                    same_col = c1 == c2
                    same_blk = same_block(key, other)
                    same_ast = same_asterisk(key, other)
                    if same_row or same_col or same_blk or same_ast:
                        sudokuNeighbors[key].append(other)
                
                
    # create dictionary of filled cells algorithm
    # filled={'A3':3, 'B1':9,'C3':1}
    filled = {}
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != 0:
                # add number to key if it exists
                # if key doesnt exist, add it
                # one value per key
                cell_name = var1[row] + str(col + 1)
                filled[cell_name] = board[row][col]
                print(f"Filled {cell_name} = {board[row][col]}")
            
    
    # creates updated domains for each cell based off whether or not its filled or not
    # filled cells have domain of 1 as themselves
    # non-filled cells have domain [1..9]
    sudokuDomains = {}
    for var in sudokuNeighbors.keys():
        if var in filled:
            sudokuDomains[var] = [filled[var]]
        else:
            sudokuDomains[var] = [num for num in range(1, 10)]
         
    for key in sudokuDomains.keys():
        print(f"{key}: {sudokuDomains[key]}")

        
    # create constrains that x != y for x, X, y, Y
    sudokuConstraints1 = lambda X, x, Y, y: x!=y
    
    # resolve with AC3
    return CSP(variables=sudokuNeighbors.keys(), domains=sudokuDomains,neighbors=sudokuNeighbors, constraints=sudokuConstraints1)