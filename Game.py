
board = [' '] * 9

def at(x, y, b = None):
    if b == None:
        return board[x + 3 * y]
    else:
        return b[x + 3 * y]

ONGOING = 0
O_WON = 1
X_WON = 2
DRAW = 3

def printBoard(board):
    for y in range(3):
        print()
        for x in range(3):
            if at(x, y) == ' ':
                print('.', end='')
            else:
                print(at(x, y), end='')
    print()

def gameState(board):

    def checkRow(col):
        for x in range(3):
            for y in range(3):
                if at(x, y, board) != col:
                    break
            else:
                return True
        return False
    def checkCol(col):
        for y in range(3):
            for x in range(3):
                if at(x, y, board) != col:
                    break
            else:
                return True
        return False
    def checkDia(col):
        for off in range(3):
            if at(off, off, board) != col:
                break
        else:
            return True
        for off in range(3):
            if at(2 - off, off, board) != col:
                break
        else:
            return True
        return False

    if checkCol('X') or checkRow('X') or checkDia('X'):
        return X_WON
    
    if checkCol('O') or checkRow('O') or checkDia('O'):
        return O_WON

    for i in range(9):
        if board[i] == ' ':
            break
    else:
        return DRAW

    return ONGOING

states = 0

def minimax(board, depth, alpha, beta, maximizing):
    state = gameState(board)
    if state != ONGOING:
        global states
        states += 1
        if state == DRAW:
            return 0

        if state == X_WON: # TODO Correct way arround?
            return 10 + depth
        if state == O_WON:
            return -10 + depth
        
    if maximizing:

        maxval = float("-inf")

        for i in range(9):
            if board[i] != ' ':
                continue

            board[i] = 'X'
            val = minimax(board, depth + 1, alpha, beta, not maximizing)
            board[i] = ' '
            maxval = max(val, maxval)
            alpha = max(alpha, val)
            if beta <= alpha:
                break

        return maxval
    else:
        minval = float("inf")

        for i in range(9):
            if board[i] != ' ':
                continue

            board[i] = 'O'
            val = minimax(board, depth + 1, alpha, beta, not maximizing)
            board[i] = ' '
            minval = min(val, minval)
            beta = min(beta, val)
            if beta <= alpha:
                break

        return minval

assert gameState(['X', 'O', ' ',
                  ' ', ' ', ' ',
                  ' ', ' ', ' ',]) == ONGOING
assert gameState(['O', 'O', 'X',
                  'X', 'X', 'O',
                  'O', 'X', 'X',]) == DRAW
assert gameState(['X', 'O', ' ',
                  'X', 'O', ' ',
                  'X', ' ', ' ',]) == X_WON
assert gameState(['X', 'O', ' ',
                  'X', 'O', ' ',
                  ' ', 'O', ' ',]) == O_WON

assert gameState(['O', 'O', 'X',
                  'O', 'X', ' ',
                  'X', ' ', ' ',]) == X_WON

state = ONGOING
turn = True

while state == ONGOING:

    if turn:
        played = False
        while not played:
            try:
                user = int(input('Where do you want to move to: ')) - 1
            except :
                continue
            if user < 0 or user >= 9 or board[user] != ' ':
                print('Invalid Move, enter again!')
                continue
            board[user] = 'O'
            played = True
    else:
        move = 0
        bestval = float("-inf")

        for i in range(9):
            if board[i] != ' ':
                continue

            board[i] = 'X'
            val = minimax(board, 0, float("-inf"), float("inf"), False)
            board[i] = ' '
            if val > bestval:
                bestval = val
                move = i

        print()
        print("Evaluated", states, "different states!")
        board[move] = 'X'

    state = gameState(board)
    turn = not turn
    printBoard(board)

if state == O_WON:
    print("Game Over: Player O Won!")
elif state == X_WON:
    print("Game Over: Player X Won!")
elif state == DRAW:
    print("Game Over: It's a Draw!")
